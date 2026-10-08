"""Persistência SQLite. Só grava e lê."""

import os
import sqlite3
from datetime import date, datetime

from models import Aluno, Emprestimo, Livro


def _iso(valor):
    if valor is None:
        return None
    if isinstance(valor, date):
        return valor.isoformat()
    return valor


def _data(valor):
    if not valor:
        return None
    return datetime.strptime(valor, "%Y-%m-%d").date()


class Banco:
    def __init__(self, caminho=None):
        padrao = "/tmp/biblioteca.db" if os.environ.get("RENDER") else "biblioteca.db"
        self._caminho = caminho or os.environ.get("DATABASE_PATH", padrao)
        self._criar()
        self._popular()

    def _con(self):
        con = sqlite3.connect(self._caminho)
        con.execute("PRAGMA foreign_keys = ON")
        return con

    def _criar(self):
        with self._con() as con:
            con.execute(
                """CREATE TABLE IF NOT EXISTS livros (
                    isbn TEXT PRIMARY KEY,
                    titulo TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    quantidade INTEGER NOT NULL,
                    disponiveis INTEGER NOT NULL
                )"""
            )
            con.execute(
                """CREATE TABLE IF NOT EXISTS alunos (
                    matricula TEXT PRIMARY KEY,
                    nome TEXT NOT NULL,
                    turma TEXT NOT NULL
                )"""
            )
            con.execute(
                """CREATE TABLE IF NOT EXISTS emprestimos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    matricula TEXT NOT NULL,
                    isbn TEXT NOT NULL,
                    retirada TEXT NOT NULL,
                    prevista TEXT NOT NULL,
                    devolvido_em TEXT,
                    FOREIGN KEY (matricula) REFERENCES alunos(matricula),
                    FOREIGN KEY (isbn) REFERENCES livros(isbn)
                )"""
            )
            con.execute(
                """CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL UNIQUE,
                    senha TEXT NOT NULL
                )"""
            )

    def _popular(self):
        with self._con() as con:
            existe = con.execute("SELECT COUNT(*) FROM livros").fetchone()[0]
            if existe:
                return
            con.execute(
                "INSERT INTO usuarios (email, senha) VALUES (?, ?)",
                ("biblioteca@escola.br", "1234"),
            )
            livros = [
                ("9780000000011", "Dom Casmurro", "Machado de Assis", 2, 2),
                ("9780000000012", "O Pequeno Príncipe", "Antoine de Saint-Exupéry", 1, 1),
                ("9780000000013", "Capitães da Areia", "Jorge Amado", 1, 0),
            ]
            con.executemany("INSERT INTO livros VALUES (?, ?, ?, ?, ?)", livros)
            alunos = [
                ("2026001", "Lia Souza", "2A"),
                ("2026002", "Rafael Lima", "2B"),
            ]
            con.executemany("INSERT INTO alunos VALUES (?, ?, ?)", alunos)

    def autenticar(self, email, senha):
        with self._con() as con:
            linha = con.execute(
                "SELECT email FROM usuarios WHERE email = ? AND senha = ?",
                (email, senha),
            ).fetchone()
        return linha is not None

    def listar_livros(self):
        with self._con() as con:
            return con.execute(
                "SELECT titulo, autor, isbn, disponiveis FROM livros ORDER BY titulo"
            ).fetchall()

    def buscar_livro(self, isbn):
        with self._con() as con:
            linha = con.execute(
                "SELECT titulo, autor, isbn, quantidade, disponiveis FROM livros WHERE isbn = ?",
                (isbn,),
            ).fetchone()
        if not linha:
            return None
        return Livro(linha[0], linha[1], linha[2], linha[3], linha[4])

    def buscar_aluno(self, matricula):
        with self._con() as con:
            linha = con.execute(
                "SELECT nome, turma, matricula FROM alunos WHERE matricula = ?",
                (matricula,),
            ).fetchone()
        if not linha:
            return None
        return Aluno(linha[0], linha[1], linha[2])

    def salvar_livro(self, livro):
        with self._con() as con:
            con.execute(
                "INSERT INTO livros VALUES (?, ?, ?, ?, ?)",
                (livro.isbn, livro.titulo, livro.autor, livro.quantidade, livro.disponiveis),
            )

    def salvar_aluno(self, aluno):
        with self._con() as con:
            con.execute(
                "INSERT INTO alunos VALUES (?, ?, ?)",
                (aluno.matricula, aluno.nome, aluno.turma),
            )

    def atualizar_disponiveis(self, isbn, disponiveis):
        with self._con() as con:
            con.execute(
                "UPDATE livros SET disponiveis = ? WHERE isbn = ?",
                (disponiveis, isbn),
            )

    def emprestimos_abertos(self, matricula):
        with self._con() as con:
            linhas = con.execute(
                """SELECT e.id, e.matricula, e.isbn, l.titulo, e.retirada, e.prevista, e.devolvido_em
                   FROM emprestimos e JOIN livros l ON l.isbn = e.isbn
                   WHERE e.matricula = ? AND e.devolvido_em IS NULL""",
                (matricula,),
            ).fetchall()
        return linhas

    def buscar_emprestimo(self, id_):
        with self._con() as con:
            linha = con.execute(
                """SELECT id, matricula, isbn, retirada, prevista, devolvido_em
                   FROM emprestimos WHERE id = ?""",
                (id_,),
            ).fetchone()
        if not linha:
            return None
        return Emprestimo(
            matricula=linha[1],
            isbn=linha[2],
            retirada=_data(linha[3]),
            prevista=_data(linha[4]),
            devolvido_em=_data(linha[5]),
            id_=linha[0],
        )

    def salvar_emprestimo(self, emprestimo):
        with self._con() as con:
            con.execute(
                """INSERT INTO emprestimos (matricula, isbn, retirada, prevista, devolvido_em)
                   VALUES (?, ?, ?, ?, ?)""",
                (
                    emprestimo.matricula,
                    emprestimo.isbn,
                    _iso(emprestimo.retirada),
                    _iso(emprestimo.prevista),
                    _iso(emprestimo.devolvido_em),
                ),
            )

    def encerrar_emprestimo(self, id_, hoje):
        with self._con() as con:
            con.execute(
                "UPDATE emprestimos SET devolvido_em = ? WHERE id = ?",
                (_iso(hoje), id_),
            )

    def listar_atrasos(self, hoje):
        with self._con() as con:
            return con.execute(
                """SELECT a.nome, a.matricula, l.titulo, e.prevista
                   FROM emprestimos e
                   JOIN alunos a ON a.matricula = e.matricula
                   JOIN livros l ON l.isbn = e.isbn
                   WHERE e.devolvido_em IS NULL AND e.prevista < ?
                   ORDER BY e.prevista""",
                (_iso(hoje),),
            ).fetchall()
