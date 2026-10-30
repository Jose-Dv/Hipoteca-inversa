"""Servidor local de la aplicación web. Ejecutar con: python app.py"""

import sys

sys.path.append("src")

from flask import Flask

from view.web import vista_hipoteca

app = Flask(__name__)
app.register_blueprint(vista_hipoteca.vista)

if __name__ == "__main__":
    app.run(debug=True)
