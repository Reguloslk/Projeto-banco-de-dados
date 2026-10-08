# Documentação técnica — BibliotecaFácil

Controle de empréstimo da biblioteca escolar.
Repositório: https://github.com/Reguloslk/Projeto-banco-de-dados
Data: 08/10/2026.

## 1. Modelagem do banco

Entidades: aluno, livro, empréstimo e usuário.

| Tabela | Chave primária | Chave estrangeira |
|---|---|---|
| alunos | matricula | — |
| livros | isbn | — |
| emprestimos | id | matricula → alunos, isbn → livros |
| usuarios | id | — |

Um aluno tem vários empréstimos. Um livro tem vários empréstimos. O usuário só autentica o balcão.

SGBD: SQLite. No computador o arquivo é `biblioteca.db`. No Render o mesmo código grava em `/tmp/biblioteca.db`, porque o disco da instância gratuita é temporário.

```sql
CREATE TABLE alunos (
  matricula TEXT PRIMARY KEY,
  nome TEXT NOT NULL,
  turma TEXT NOT NULL
);
CREATE TABLE livros (
  isbn TEXT PRIMARY KEY,
  titulo TEXT NOT NULL,
  autor TEXT NOT NULL,
  quantidade INTEGER NOT NULL,
  disponiveis INTEGER NOT NULL
);
CREATE TABLE emprestimos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  matricula TEXT NOT NULL,
  isbn TEXT NOT NULL,
  retirada TEXT NOT NULL,
  prevista TEXT NOT NULL,
  devolvido_em TEXT,
  FOREIGN KEY (matricula) REFERENCES alunos(matricula),
  FOREIGN KEY (isbn) REFERENCES livros(isbn)
);
CREATE TABLE usuarios (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL UNIQUE,
  senha TEXT NOT NULL
);
```

## 2. Diagrama de classes

- `Pessoa` é abstrata. `Aluno` e `Bibliotecaria` herdam `Pessoa` e implementam `papel()`.
- `Livro` guarda título, autor, ISBN, quantidade e disponíveis. `pode_emprestar()`, `baixar_exemplar()` e `devolver_exemplar()` protegem o estoque.
- `Emprestimo` guarda matrícula, ISBN e datas. `esta_aberto()`, `esta_atrasado()` e `encerrar()`.
- `Validador` é abstrato. `ValidadorEstoque` e `ValidadorAtraso` implementam o mesmo `validar()`.
- `EmprestimoService` só aplica a regra. Não grava SQL.

Relação: Livro 1 — * Empréstimo * — 1 Aluno.

## 3. Casos de uso

Ator único: bibliotecária.

- Login
- Cadastrar livro
- Cadastrar aluno
- Consultar acervo
- Emprestar
- Devolver
- Listar atrasos

O aluno não entra no sistema. Ele é dado do empréstimo. Sem login, as outras telas não abrem.

## 4. Arquitetura

Três responsabilidades, em arquivos separados:

| Arquivo | Papel |
|---|---|
| views.py | Recebe o formulário e devolve HTML |
| controller.py | Regra de empréstimo e devolução |
| models.py | Classes de domínio |
| database.py | SQLite: grava e lê |
| main.py | Sobe o servidor |

A tela não decide a regra. O serviço não escreve SQL. O banco não valida atraso.

## 5. Bibliotecas

| Nome | Versão | Uso |
|---|---|---|
| Python | 3.12 | Linguagem |
| Flask | 3.0.3 | Rotas e telas |
| Jinja2 | incluso no Flask 3.0.3 | HTML |
| Bootstrap | 5.3.3 | Formulário no Chrome e no celular |
| gunicorn | 22.0.0 | Publicação |
| pytest | 8.3.3 | Testes |
| sqlite3 | incluso no Python | Banco |

## 6. Pastas

```text
main.py
models.py
views.py
controller.py
database.py
requirements.txt
README.md
DOCUMENTACAO.md
templates/
tests/test_emprestimo.py
```

## 7. Execução

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest -v
python main.py
```

Abra http://127.0.0.1:8080

Login de demonstração: `biblioteca@escola.br` / `1234`

No Render: Build `pip install -r requirements.txt`. Start `gunicorn main:app`.

## 8. Regras testadas

- Empréstimo com estoque baixa 1 exemplar e marca prazo de 7 dias.
- Sem exemplar, nada é gravado.
- Aluno em atraso não retira outro livro.
- Herança: aluno e bibliotecária respondem papéis diferentes.

## 9. Referências

- Flask: https://flask.palletsprojects.com/
- Jinja2: https://jinja.palletsprojects.com/
- Bootstrap 5.3: https://getbootstrap.com/docs/5.3/
- pytest: https://docs.pytest.org/
- SQLite: https://www.sqlite.org/docs.html
- Render: https://render.com/docs
