# BibliotecaFácil — apresentação (8 slides)

## Slide 1 — Capa

BibliotecaFácil. Empréstimo da biblioteca da escola.
Repositório: https://github.com/Reguloslk/Projeto-banco-de-dados

## Slide 2 — Problema

A bibliotecária anotava o empréstimo no papel. Estoque e atraso se perdiam. O sistema guarda isso no banco.

## Slide 3 — O que faz

Login do balcão, acervo, cadastro de livro e aluno, empréstimo com recibo, devolução e lista de atrasos.

## Slide 4 — Regras

- Só empresta se houver exemplar.
- Aluno em atraso não retira outro livro.
- O prazo é de 7 dias.
- Matrícula e ISBN não se repetem.

## Slide 5 — Arquivos

- `views.py` — telas
- `controller.py` — regra
- `models.py` — classes
- `database.py` — SQLite
- `main.py` — sobe o servidor

## Slide 6 — Banco

Tabelas: alunos, livros, emprestimos e usuarios. Chave primária em cada uma. Empréstimo aponta para aluno e para livro.

## Slide 7 — Orientação a objetos

Encapsulamento no estoque. Herança de Pessoa para Aluno e Bibliotecaria. Polimorfismo em papel() e validar(). Abstracao em Pessoa e Validador.

## Slide 8 — Como ver

Login: biblioteca@escola.br / 1234
Teste: `pytest -v`
Publicação no Render, comando: `gunicorn main:app`
