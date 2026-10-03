"""Regra de negócio. Não lê formulário e não escreve SQL."""

from datetime import timedelta

from app.dominio.classes import Emprestimo, ValidadorAtraso, ValidadorEstoque

PRAZO_DIAS = 7


class EmprestimoService:
    def __init__(self, validadores=None):
        self._validadores = validadores or [ValidadorEstoque(), ValidadorAtraso()]

    def emprestar(self, aluno_atrasado, livro, matricula, hoje):
        for validador in self._validadores:
            validador.validar(aluno_atrasado, livro)
        livro.baixar_exemplar()
        return Emprestimo(
            matricula=matricula,
            isbn=livro.isbn,
            retirada=hoje,
            prevista=hoje + timedelta(days=PRAZO_DIAS),
        )

    def devolver(self, emprestimo, livro, hoje):
        emprestimo.encerrar(hoje)
        livro.devolver_exemplar()
        return emprestimo
