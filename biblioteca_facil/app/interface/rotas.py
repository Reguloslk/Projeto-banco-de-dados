"""Interface web. Só recebe o formulário e chama o serviço."""

from datetime import date

from flask import Flask, redirect, render_template, request

from app.dominio.classes import Aluno, Livro
from app.negocio.servico import EmprestimoService
from app.persistencia.banco import Banco

app = Flask(__name__, template_folder="../templates")
banco = Banco()
servico = EmprestimoService()


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/acervo")
def acervo():
    return render_template("acervo.html", livros=banco.listar_livros())


@app.route("/emprestar", methods=["GET", "POST"])
def emprestar():
    mensagem = ""
    if request.method == "POST":
        matricula = request.form["matricula"]
        isbn = request.form["isbn"]
        linha = banco.buscar_livro(isbn)
        if not linha:
            mensagem = "Livro nao encontrado"
        else:
            livro = Livro(linha[0], linha[1], linha[2], linha[3])
            livro._disponiveis = linha[4]
            abertos = banco.emprestimos_abertos(matricula)
            atrasado = any(prevista < date.today() for _, _, _, prevista, _ in abertos)
            try:
                emprestimo = servico.emprestar(atrasado, livro, matricula, date.today())
                banco.salvar_emprestimo(emprestimo)
                banco.atualizar_disponiveis(isbn, livro.disponiveis)
                return render_template(
                    "recibo.html",
                    matricula=matricula,
                    titulo=livro.titulo,
                    prevista=emprestimo.prevista.strftime("%d/%m/%Y"),
                )
            except ValueError as erro:
                mensagem = str(erro)
    return render_template("emprestimo.html", mensagem=mensagem)


if __name__ == "__main__":
    app.run(debug=True)
