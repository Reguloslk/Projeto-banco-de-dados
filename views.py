"""Interface web. Recebe o formulário e devolve HTML."""

from datetime import date
from functools import wraps
import sqlite3

from flask import Flask, redirect, render_template, request, session, url_for

from controller import EmprestimoService
from database import Banco
from models import Aluno, Livro

app = Flask(__name__)
app.secret_key = "biblioteca-facil-escola"
banco = Banco()
servico = EmprestimoService()


def precisa_login(funcao):
    @wraps(funcao)
    def envolta(*args, **kwargs):
        if not session.get("logado"):
            return redirect(url_for("login"))
        return funcao(*args, **kwargs)

    return envolta


@app.errorhandler(Exception)
def erro_geral(erro):
    if isinstance(erro, (ValueError, sqlite3.Error)):
        return render_template("erro.html", mensagem=str(erro)), 400
    app.logger.exception(erro)
    return render_template("erro.html", mensagem="Não foi possível concluir a operação."), 500


@app.route("/", methods=["GET", "POST"])
def login():
    mensagem = ""
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")
        try:
            if banco.autenticar(email, senha):
                session["logado"] = True
                return redirect(url_for("acervo"))
            mensagem = "E-mail ou senha inválidos."
        except sqlite3.Error:
            mensagem = "Não foi possível acessar o banco."
    return render_template("login.html", mensagem=mensagem)


@app.route("/sair")
def sair():
    session.clear()
    return redirect(url_for("login"))


@app.route("/acervo")
@precisa_login
def acervo():
    try:
        livros = banco.listar_livros()
    except sqlite3.Error:
        livros = []
    return render_template("acervo.html", livros=livros)


@app.route("/livros/novo", methods=["GET", "POST"])
@precisa_login
def novo_livro():
    mensagem = ""
    if request.method == "POST":
        try:
            quantidade = int(request.form.get("quantidade", "0"))
            if quantidade < 1:
                raise ValueError("A quantidade deve ser maior que zero.")
            livro = Livro(
                request.form.get("titulo", "").strip(),
                request.form.get("autor", "").strip(),
                request.form.get("isbn", "").strip(),
                quantidade,
            )
            if not livro.titulo or not livro.autor or not livro.isbn:
                raise ValueError("Preencha título, autor e ISBN.")
            banco.salvar_livro(livro)
            return redirect(url_for("acervo"))
        except (ValueError, sqlite3.IntegrityError) as erro:
            mensagem = str(erro) if isinstance(erro, ValueError) else "ISBN já cadastrado."
    return render_template("novo_livro.html", mensagem=mensagem)


@app.route("/alunos/novo", methods=["GET", "POST"])
@precisa_login
def novo_aluno():
    mensagem = ""
    if request.method == "POST":
        try:
            aluno = Aluno(
                request.form.get("nome", "").strip(),
                request.form.get("turma", "").strip(),
                request.form.get("matricula", "").strip(),
            )
            if not aluno.nome or not aluno.turma or not aluno.matricula:
                raise ValueError("Preencha nome, turma e matrícula.")
            banco.salvar_aluno(aluno)
            return redirect(url_for("acervo"))
        except (ValueError, sqlite3.IntegrityError) as erro:
            mensagem = str(erro) if isinstance(erro, ValueError) else "Matrícula já cadastrada."
    return render_template("novo_aluno.html", mensagem=mensagem)


@app.route("/emprestar", methods=["GET", "POST"])
@precisa_login
def emprestar():
    mensagem = ""
    if request.method == "POST":
        matricula = request.form.get("matricula", "").strip()
        isbn = request.form.get("isbn", "").strip()
        try:
            aluno = banco.buscar_aluno(matricula)
            livro = banco.buscar_livro(isbn)
            if not aluno:
                raise ValueError("Aluno não encontrado.")
            if not livro:
                raise ValueError("Livro não encontrado.")
            abertos = banco.emprestimos_abertos(matricula)
            atrasado = any(_data_aberta(item[5]) < date.today() for item in abertos)
            emprestimo = servico.emprestar(atrasado, livro, matricula, date.today())
            banco.salvar_emprestimo(emprestimo)
            banco.atualizar_disponiveis(isbn, livro.disponiveis)
            return render_template(
                "recibo.html",
                matricula=matricula,
                aluno=aluno.nome,
                titulo=livro.titulo,
                prevista=emprestimo.prevista.strftime("%d/%m/%Y"),
            )
        except ValueError as erro:
            mensagem = str(erro)
        except sqlite3.Error:
            mensagem = "Não foi possível gravar o empréstimo."
    return render_template("emprestimo.html", mensagem=mensagem)


@app.route("/devolver", methods=["GET", "POST"])
@precisa_login
def devolver():
    mensagem = ""
    abertos = []
    matricula = request.form.get("matricula") or request.args.get("matricula", "")
    if matricula:
        try:
            abertos = banco.emprestimos_abertos(matricula)
            if request.method == "POST" and request.form.get("emprestimo_id"):
                emprestimo = banco.buscar_emprestimo(int(request.form["emprestimo_id"]))
                livro = banco.buscar_livro(emprestimo.isbn) if emprestimo else None
                if not emprestimo or not livro:
                    raise ValueError("Empréstimo não encontrado.")
                servico.devolver(emprestimo, livro, date.today())
                banco.encerrar_emprestimo(emprestimo.id, date.today())
                banco.atualizar_disponiveis(livro.isbn, livro.disponiveis)
                mensagem = "Devolvido. O exemplar voltou ao acervo."
                abertos = banco.emprestimos_abertos(matricula)
        except ValueError as erro:
            mensagem = str(erro)
        except sqlite3.Error:
            mensagem = "Não foi possível registrar a devolução."
    return render_template(
        "devolucao.html",
        mensagem=mensagem,
        abertos=abertos,
        matricula=matricula,
        ok="Devolvido" in mensagem,
    )


@app.route("/atrasos")
@precisa_login
def atrasos():
    try:
        lista = banco.listar_atrasos(date.today())
    except sqlite3.Error:
        lista = []
    return render_template("atrasos.html", atrasos=lista)


def _data_aberta(texto):
    from datetime import datetime

    return datetime.strptime(texto, "%Y-%m-%d").date()
