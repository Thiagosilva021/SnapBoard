from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, length, ValidationError, Optional
from flask_login import current_user
from snapboard.models import Usuario


class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')

class FormCriarConta(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Nome de Usuário', validators=[DataRequired(), length(2, 50)])
    senha = PasswordField('Senha', validators=[DataRequired(), length(6, 100)])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    submit = SubmitField('Criar Conta')

    # Validação personalizada para verificar se o email já está em uso
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Este email já está em uso. Por favor, escolha outro.')

    # Validação personalizada para verificar se o nome de usuário já está em uso.
    # Sem isso, um username repetido só falhava na hora do db.session.commit()
    # (IntegrityError não tratada -> erro 500 em vez de mensagem amigável).
    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError('Este nome de usuário já está em uso. Por favor, escolha outro.')

class FormFoto(FlaskForm):
    foto = FileField('Foto', validators=[
        FileRequired(message='Selecione uma imagem.'),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Apenas imagens JPG ou PNG!')
    ])
    submit = SubmitField('Enviar Foto')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(), length(2, 50)])
    bio = TextAreaField('Bio', validators=[Optional(), length(max=280)])
    foto_perfil = FileField('Foto de perfil', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Apenas imagens JPG ou PNG!')
    ])
    submit = SubmitField('Salvar alterações')

    # Ignora o próprio usuário na checagem de duplicidade — sem isso,
    # salvar o perfil sem mudar o username sempre acusaria "já em uso".
    def validate_username(self, username):
        if username.data == current_user.username:
            return
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError('Este nome de usuário já está em uso. Por favor, escolha outro.')


class FormAlterarSenha(FlaskForm):
    senha_atual = PasswordField('Senha atual', validators=[DataRequired()])
    nova_senha = PasswordField('Nova senha', validators=[DataRequired(), length(6, 100)])
    confirmar_nova_senha = PasswordField(
        'Confirmar nova senha',
        validators=[DataRequired(), EqualTo('nova_senha', message='As senhas não coincidem.')]
    )
    submit = SubmitField('Alterar senha')