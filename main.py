"""Ponto de entrada da aplicação BibliotecaFácil."""

import os

from views import app

if __name__ == "__main__":
    porta = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=porta, debug=False)
