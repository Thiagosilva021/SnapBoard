from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
import sys

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Falha rápido e com mensagem clara se faltar configuração essencial,
# em vez de deixar o erro aparecer só quando um usuário acessar um formulário.
if not app.config['SQLALCHEMY_DATABASE_URI'] or not app.config['SECRET_KEY']:
    sys.exit(
        'ERRO: defina SQLALCHEMY_DATABASE_URI e SECRET_KEY no arquivo .env '
        'antes de iniciar a aplicação.'
    )

# Caminho único e absoluto para os uploads (elimina a duplicação com excluir_postagem)
app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'posts')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Limite de tamanho de upload (5 MB por requisição)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # antes: 'homepage'
login_manager.login_message = 'Faça login para acessar esta página.'
login_manager.login_message_category = 'info'

from snapboard import models
from snapboard import routes