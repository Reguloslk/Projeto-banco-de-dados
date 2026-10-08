# BibliotecaFácil

Sistema web de empréstimo da biblioteca escolar. A bibliotecária entra no balcão, consulta o acervo, cadastra livro e aluno, empresta, devolve e lista atrasos. O prazo padrão é de 7 dias. Aluno em atraso ou livro sem estoque não gera empréstimo.

## Login de demonstração

- E-mail: `biblioteca@escola.br`
- Senha: `1234`

## Funcionalidades

- Login do balcão
- Cadastro de livro e de aluno
- Consulta do acervo
- Empréstimo com recibo
- Devolução
- Lista de atrasos
- Testes da regra de negócio

## Bibliotecas

| Nome | Versão | Uso |
|---|---|---|
| Python | 3.12 | Linguagem |
| Flask | 3.0.3 | Rotas e telas |
| Jinja2 | incluso no Flask | HTML |
| Bootstrap | 5.3.3 | Formulário no Chrome e no celular |
| gunicorn | 22.0.0 | Publicação no Render |
| pytest | 8.3.3 | Testes |
| sqlite3 | incluso no Python | Banco local |

Documentação oficial do Flask: https://flask.palletsprojects.com/

## Pastas e arquivos

```text
biblioteca_facil/
├── main.py            sobe o servidor
├── models.py          classes (POO)
├── views.py           telas e rotas
├── controller.py      regra de empréstimo
├── database.py        SQLite
├── requirements.txt
├── README.md
├── templates/         HTML
├── tests/             pytest
└── docs/prints/       prints do sistema
```

A tela não decide a regra. O serviço não escreve SQL. O banco não valida atraso.

## Como rodar

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest -v
python main.py
```

Abra http://127.0.0.1:8080

## Publicação no Render

1. Repositório público no GitHub, com estes arquivos na raiz.
2. Build Command: `pip install -r requirements.txt`
3. Start Command: `gunicorn main:app`

## POO

- Encapsulamento: `disponiveis` sai só por propriedade.
- Herança: `Aluno` e `Bibliotecaria` herdam `Pessoa`.
- Polimorfismo: `papel()` e `validar()`.
- Abstração: `Pessoa` e `Validador` não são instanciados.

## Prints

Login, acervo, empréstimo com atraso e resultado do pytest estão em `docs/prints/`.
