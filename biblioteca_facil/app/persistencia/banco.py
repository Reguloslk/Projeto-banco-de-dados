"""Persistência. Só grava e lê. Não decide regra de empréstimo."""

import sqlite3
from datetime import date, datetime


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
    def __init__(self, caminho="biblioteca.db"):
        self._caminho = caminho
        self._criar()

    def _con(self):
        return sqlite3.connect(self._caminho)

    def _criar(self):
        with self._con() as con:
            con.execute(
                """CREATE TABLE IF NOT EXISTS livros (
                    isbn TEXT PRIMARY KEY, titulo TEXT, autor TEXT,
                    quantidade INTEGER, disponiveis INTEGER)"""
            )
            con.execute(
                """CREATE TABLE IF NOT EXISTS alunos (
                    matricula TEXT PRIMARY KEY, nome TEXT, turma TEXT)"""
            )
            con.execute(
                """CREATE TABLE IF NOT EXISTS emprestimos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    matricula TEXT, isbn TEXT, retirada TEXT,
                    prevista TEXT, devolvido_em TEXT)"""
            )

    def salvar_livro(self, livro):
        with self._con() as con:
            con.execute(
                "INSERT INTO livros VALUES (?, ?, ?, ?, ?)",
                (livro.isbn, livro.titulo, livro.autor, livro._quantidade, livro.disponiveis),
            )

    def salvar_aluno(self, aluno):
        with self._con() as con:
            con.execute(
                "INSERT INTO alunos VALUES (?, ?, ?)",
                (aluno.matricula, aluno.nome, aluno.turma),
            )

    def listar_livros(self):
        with self._con() as con:
            return con.execute(
                "SELECT titulo, autor, isbn, disponiveis FROM livros"
            ).fetchall()

    def buscar_livro(self, isbn):
        with self._con() as con:
            return con.execute(
                "SELECT titulo, autor, isbn, quantidade, disponiveis FROM livros WHERE isbn = ?",
                (isbn,),
            ).fetchone()

    def atualizar_disponiveis(self, isbn, disponiveis):
        with self._con() as con:
            con.execute(
                "UPDATE livros SET disponiveis = ? WHERE isbn = ?",
                (disponiveis, isbn),
            )

    def emprestimos_abertos(self, matricula):
        with self._con() as con:
            linhas = con.execute(
                """SELECT matricula, isbn, retirada, prevista, devolvido_em
                   FROM emprestimos WHERE matricula = ? AND devolvido_em IS NULL""",
                (matricula,),
            ).fetchall()
        return [
            (m, isbn, _data(r), _data(p), _data(d))
            for m, isbn, r, p, d in linhas
        ]

    def salvar_emprestimo(self, emprestimo):
        with self._con() as con:
            con.execute(
                "INSERT INTO emprestimos (matricula, isbn, retirada, prevista, devolvido_em) VALUES (?, ?, ?, ?, ?)",
                (
                    emprestimo.matricula,
                    emprestimo.isbn,
                    _iso(emprestimo._retirada),
                    _iso(emprestimo.prevista),
                    _iso(emprestimo.devolvido_em),
                ),
            )
