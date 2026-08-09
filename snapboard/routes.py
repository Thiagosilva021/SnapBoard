from flask import render_template, url_for, flash, redirect
from snapboard import app, db, bcrypt
from snapboard.forms import FormLogin, FormCriarConta, FormFoto
from snapboard.models import Usuario, Postagem
from flask_login import login_required, login_user, logout_user, current_user
import os
from werkzeug.utils import secure_filename

@app.route("/")
def homepage():
    return render_template('homepage.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = FormLogin()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data):
            login_user(usuario, remember=True)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('perfil', id_usuario=usuario.id))
        else:
            flash('Falha no login. Verifique seu email e senha.', 'danger')
    return render_template('login.html', form=form)

@app.route("/criarconta", methods=['GET', 'POST'])
def criar_conta():
    form = FormCriarConta()
    if form.validate_on_submit():
        senha = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        usuario = Usuario(username=form.username.data, email=form.email.data, senha=senha)
        db.session.add(usuario)
        db.session.commit()
        flash('Conta criada com sucesso! Você já pode fazer login.', 'success')
        login_user(usuario, remember=True)  # Loga o usuário após criar a conta
        return redirect(url_for('perfil', id_usuario=usuario.id))
    return render_template('criar_conta.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('homepage'))

@app.route("/perfil/<id_usuario>", methods=['GET', 'POST'])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        # Renderiza o perfil do usuário logado
        form = FormFoto()
        if form.validate_on_submit():

            # Aqui você pode adicionar a lógica para salvar a foto enviada
            arquivo = form.foto.data
            nome_seguro = secure_filename(arquivo.filename)

            #salvar o arquivo na pasta posts
            caminho = os.path.join((os.path.abspath(os.path.dirname(__file__))), app.config['UPLOAD_FOLDER'], nome_seguro)
            arquivo.save(caminho)

            # registrar a postagem no banco de dados
            foto = Postagem(imagem=nome_seguro, id_usuario=current_user.id)
            db.session.add(foto)
            db.session.commit()
            return redirect(url_for('perfil', id_usuario=current_user.id))
        return render_template('perfil.html', usuario=current_user, form=form)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template('perfil.html', usuario=usuario, form=None)

@app.route("/feed")
@login_required
def feed():
    fotos = Postagem.query.order_by(Postagem.data_criacao.desc()).all()
    return render_template('feed.html', fotos=fotos)
