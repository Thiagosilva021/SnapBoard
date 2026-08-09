from snapboard import db, login_manager
from datetime import datetime, UTC
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    fotos = db.relationship('Postagem', backref='usuario', lazy=True)

class Postagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imagem = db.Column(db.String(200), default='default.jpg')
    data_criacao = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC)) # Use uma lambda para garantir que o horário UTC seja definido no momento da criação do objeto.
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
