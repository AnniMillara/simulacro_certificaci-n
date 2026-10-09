from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "ʕ•ᴥ•ʔ"
bcrypt = Bcrypt(app)

# Importar controladores (registran las rutas)
from flask_app.controllers import usuarios, peluches