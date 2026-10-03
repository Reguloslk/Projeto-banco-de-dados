"""Classes de domínio. Atributo interno fica protegido; a regra usa método."""

from abc import ABC, abstractmethod
from datetime import date


class Pessoa(ABC):
    def __init__(self, nome):
        self._nome = nome

    @property
    def nome(self):
        return self._nome

    @abstractmethod
    def papel(self):
        pass


class Aluno(Pessoa):
    def __init__(self, nome, turma, matricula):
        super().__init__(nome)
        self._turma = turma
        self._matricula = matricula

    @property
    def turma(self):
        return self._turma

    @property
    def matricula(self):
        return self._matricula

    def papel(self):
        return "aluno"


class Bibliotecaria(Pessoa):
    def __init__(self, nome, email):
        super().__init__(nome)
        self._email = email

    @property
    def email(self):
        return self._email

    def papel(self):
        return "bibliotecaria"


class Livro:
    def __init__(self, titulo, autor, isbn, quantidade):
        self._titulo = titulo
        self._autor = autor
        self._isbn = isbn
        self._quantidade = quantidade
        self._disponiveis = quantidade

    @property
    def titulo(self):
        return self._titulo

    @property
    def autor(self):
        return self._autor

    @property
    def isbn(self):
        return self._isbn

    @property
    def disponiveis(self):
        return self._disponiveis

    def pode_emprestar(self):
        return self._disponiveis > 0

    def baixar_exemplar(self):
        if not self.pode_emprestar():
            raise ValueError("Sem exemplar disponivel")
        self._disponiveis -= 1

    def devolver_exemplar(self):
        self._disponiveis += 1


class Emprestimo:
    def __init__(self, matricula, isbn, retirada, prevista, devolvido_em=None):
        self._matricula = matricula
        self._isbn = isbn
        self._retirada = retirada
        self._prevista = prevista
        self._devolvido_em = devolvido_em

    @property
    def matricula(self):
        return self._matricula

    @property
    def isbn(self):
        return self._isbn

    @property
    def prevista(self):
        return self._prevista

    @property
    def devolvido_em(self):
        return self._devolvido_em

    def esta_aberto(self):
        return self._devolvido_em is None

    def esta_atrasado(self, hoje):
        return self.esta_aberto() and self._prevista < hoje

    def encerrar(self, hoje):
        self._devolvido_em = hoje


class Validador(ABC):
    @abstractmethod
    def validar(self, aluno_atrasado, livro):
        pass


class ValidadorEstoque(Validador):
    def validar(self, aluno_atrasado, livro):
        if not livro.pode_emprestar():
            raise ValueError("Sem exemplar disponivel")


class ValidadorAtraso(Validador):
    def validar(self, aluno_atrasado, livro):
        if aluno_atrasado:
            raise ValueError("Aluno em atraso")
