from datetime import date

import pytest

from app.dominio.classes import Aluno, Bibliotecaria, Livro
from app.negocio.servico import EmprestimoService


def test_heranca_e_polimorfismo_de_papel():
    pessoas = [Aluno("Lia", "2A", "2026001"), Bibliotecaria("Ana", "biblioteca@escola.br")]
    assert [pessoa.papel() for pessoa in pessoas] == ["aluno", "bibliotecaria"]


def test_empresta_e_baixa_um_exemplar():
    livro = Livro("Dom Casmurro", "Machado de Assis", "9780000000011", 2)
    emprestimo = EmprestimoService().emprestar(False, livro, "2026001", date(2026, 10, 3))
    assert livro.disponiveis == 1
    assert emprestimo.prevista == date(2026, 10, 10)


def test_nao_empresta_sem_exemplar():
    livro = Livro("Capitaes da Areia", "Jorge Amado", "9780000000012", 0)
    with pytest.raises(ValueError, match="Sem exemplar"):
        EmprestimoService().emprestar(False, livro, "2026001", date(2026, 10, 3))


def test_nao_empresta_aluno_em_atraso():
    livro = Livro("Dom Casmurro", "Machado de Assis", "9780000000011", 2)
    with pytest.raises(ValueError, match="atraso"):
        EmprestimoService().emprestar(True, livro, "2026001", date(2026, 10, 3))
    assert livro.disponiveis == 2


def test_encapsulamento_nao_expoe_alteracao_direta_pelo_nome_publico():
    livro = Livro("O Pequeno Principe", "Saint-Exupery", "9780000000013", 1)
    assert livro.disponiveis == 1
    livro.baixar_exemplar()
    assert livro.disponiveis == 0
