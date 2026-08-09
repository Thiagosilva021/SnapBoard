from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, length, ValidationError
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

class FormFoto(FlaskForm):
    foto = FileField('Foto', validators=[
        FileRequired(message='Selecione uma imagem.'),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Apenas imagens JPG ou PNG!')
    ])
    submit = SubmitField('Enviar Foto')