# Documentação técnica — BibliotecaFácil

Controle de empréstimo da biblioteca escolar.
Repositório: https://github.com/Reguloslk/Projeto-banco-de-dados

## 1. Modelagem do banco

| Tabela | Chave primária | Chave estrangeira |
|---|---|---|
| alunos | matricula | — |
| livros | isbn | — |
| emprestimos | id | matricula aponta para alunos; isbn aponta para livros |
| usuarios | id | — |

Um aluno tem vários empréstimos. Um livro tem vários empréstimos.
SGBD: SQLite. Arquivo local: biblioteca.db.

## 2. Classes

Pessoa é abstrata. Aluno e Bibliotecaria herdam Pessoa.
Livro protege o estoque. Emprestimo guarda as datas.
ValidadorEstoque e ValidadorAtraso usam o mesmo validar().
EmprestimoService aplica a regra e não grava SQL.

## 3. Casos de uso

Ator: bibliotecária. Login, cadastrar livro, cadastrar aluno, consultar, emprestar, devolver e listar atrasos. O aluno não entra no sistema.

## 4. Arquitetura

views.py recebe o formulário. controller.py aplica a regra. models.py guarda as classes. database.py grava no SQLite. main.py sobe o servidor.

## 5. Bibliotecas

Python 3.12, Flask 3.0.3, Jinja2 incluso no Flask, Bootstrap 5.3.3, gunicorn 22.0.0, pytest 8.3.3, sqlite3 incluso no Python.

## 6. Execução

pip install -r requirements.txt
pytest -v
python main.py

Login: biblioteca@escola.br / 1234

Render: Build pip install -r requirements.txt. Start gunicorn main:app.

## 7. Referências

https://flask.palletsprojects.com/
https://jinja.palletsprojects.com/
https://getbootstrap.com/docs/5.3/
https://docs.pytest.org/
https://www.sqlite.org/docs.html
https://render.com/docs
