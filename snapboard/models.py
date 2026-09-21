from snapboard import db, login_manager
from datetime import datetime, UTC
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(280), nullable=True)
    foto_perfil = db.Column(db.String(200), nullable=True)
    fotos = db.relationship(
        'Postagem', backref='usuario', cascade='all, delete-orphan',
        lazy=True, order_by='Postagem.data_criacao.desc()'
    )

    def segue(self, outro_usuario):
        """True se este usuário já segue 'outro_usuario'."""
        if outro_usuario is None or outro_usuario.id == self.id:
            return False
        return self.seguindo.filter_by(id_seguido=outro_usuario.id).first() is not None

class Postagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imagem = db.Column(db.String(200), default='default.jpg')
    data_criacao = db.Column(db.DateTime, nullable=False, index=True, default=lambda: datetime.now(UTC)) # Use uma lambda para garantir que o horário UTC seja definido no momento da criação do objeto.
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

class Curtida(db.Model):
    __table_args__ = (
        db.UniqueConstraint('id_usuario', 'id_postagem', name='uq_curtida_usuario_postagem'),
    )

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE'), nullable=False)
    id_postagem = db.Column(db.Integer, db.ForeignKey('postagem.id', ondelete='CASCADE'), nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC)) # Use uma lambda para garantir que o horário UTC seja definido no momento da criação do objeto.

    usuario = db.relationship('Usuario', backref=db.backref('curtidas', cascade='all, delete-orphan'))
    postagem = db.relationship('Postagem', backref=db.backref('curtidas', cascade='all, delete-orphan'))

class Seguidor(db.Model):
    """Relacionamento 'segue': id_seguidor SEGUE id_seguido."""

    __table_args__ = (
        # Impede duplicar o mesmo relacionamento (seguir a mesma pessoa duas vezes)
        db.UniqueConstraint('id_seguidor', 'id_seguido', name='uq_seguidor_seguido'),
        # Impede um usuário seguir a si mesmo, garantido no nível do banco
        db.CheckConstraint('id_seguidor != id_seguido', name='ck_nao_seguir_a_si_mesmo'),
    )

    id = db.Column(db.Integer, primary_key=True)
    id_seguidor = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE'), nullable=False)
    id_seguido = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE'), nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False, index=True, default=lambda: datetime.now(UTC))

    # lazy='dynamic' permite contar (.count()) e filtrar sem carregar tudo pra memória
    seguidor = db.relationship(
        'Usuario', foreign_keys=[id_seguidor],
        backref=db.backref('seguindo', lazy='dynamic', cascade='all, delete-orphan')
    )
    seguido = db.relationship(
        'Usuario', foreign_keys=[id_seguido],
        backref=db.backref('seguidores', lazy='dynamic', cascade='all, delete-orphan')
    )