from flask import render_template, url_for, flash, redirect, current_app, request, send_from_directory
from snapboard import app, db, bcrypt
from snapboard.forms import FormLogin, FormCriarConta, FormFoto
from snapboard.models import Usuario, Postagem, Curtida
from flask_login import login_required, login_user, logout_user, current_user
import uuid
import os
from werkzeug.utils import secure_filename
from PIL import Image

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
    return render_template('login.html')

@app.route("/perfil/<int:id_usuario>", methods=['GET', 'POST'])   # <int:> em vez de string livre
@login_required
def perfil(id_usuario):
    if id_usuario == current_user.id:
        form = FormFoto()
        if form.validate_on_submit():
            arquivo = form.foto.data

            # valida que o conteúdo enviado é realmente uma imagem (não só a extensão)
            try:
                Image.open(arquivo.stream).verify()
                arquivo.stream.seek(0)
            except Exception:
                flash('O arquivo enviado não é uma imagem válida.', 'danger')
                return redirect(url_for('perfil', id_usuario=current_user.id))

            extensao = secure_filename(arquivo.filename).rsplit('.', 1)[-1].lower()
            nome_unico = f"{uuid.uuid4().hex}.{extensao}"   # elimina colisão entre usuários
            caminho = os.path.join(current_app.config['UPLOAD_FOLDER'], nome_unico)

            try:
                arquivo.save(caminho)
                foto = Postagem(imagem=nome_unico, id_usuario=current_user.id)
                db.session.add(foto)
                db.session.commit()
            except Exception:
                db.session.rollback()
                flash('Não foi possível salvar sua foto. Tente novamente.', 'danger')
                return redirect(url_for('perfil', id_usuario=current_user.id))

            return redirect(url_for('perfil', id_usuario=current_user.id))
        return render_template('perfil.html', usuario=current_user, form=form)
    else:
        usuario = Usuario.query.get_or_404(id_usuario)   # get_or_404 em vez de get
        return render_template('perfil.html', usuario=usuario, form=None)

@app.route("/feed")
@login_required
def feed():
    pagina = request.args.get('pagina', 1, type=int)
    paginacao = (
        Postagem.query
        .order_by(Postagem.data_criacao.desc())
        .paginate(page=pagina, per_page=20, error_out=False)
    )
    return render_template('feed.html', fotos=paginacao.items, paginacao=paginacao)

@app.route('/excluir_postagem/<int:id>', methods=['POST'])
@login_required
def excluir_postagem(id):
    postagem = Postagem.query.get_or_404(id)

    if postagem.usuario.id != current_user.id:
        flash('Você não pode excluir esta postagem.', 'danger')
        return redirect(url_for('perfil', id_usuario=current_user.id))

    caminho_imagem = os.path.join(current_app.config['UPLOAD_FOLDER'], postagem.imagem)

    try:
        db.session.delete(postagem)
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash('Não foi possível excluir a postagem. Tente novamente.', 'danger')
        return redirect(url_for('perfil', id_usuario=current_user.id))

    # só remove o arquivo físico DEPOIS de confirmar a exclusão no banco
    if os.path.exists(caminho_imagem):
        os.remove(caminho_imagem)

    flash('Postagem excluída com sucesso!', 'success')
    return redirect(url_for('perfil', id_usuario=current_user.id))

@app.route('/baixar_imagem/<int:id>')
@login_required
def baixar_imagem(id):

    postagem = Postagem.query.get_or_404(id)# validar se a postagem existe

    # Apenas o dono da postagem pode baixar
    if postagem.usuario_id != current_user.id:
        flash('Você não pode baixar esta imagem.', 'danger')
        return redirect(
            url_for('perfil', id_usuario=current_user.id)
        )

    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'],
        postagem.imagem,
        as_attachment=True
    )

@app.route('/curtir/<int:id>', methods=['POST'])
@login_required
def curtir(id):
    postagem = Postagem.query.get_or_404(id)# validar se a postagem existe
    curtida = Curtida.query.filter_by(usuario_id=current_user.id, postagem_id=id).first()

    if not curtida:
        try:
            db.session.add(Curtida(usuario_id=current_user.id, postagem_id=id))
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash('Não foi possível curtir a postagem. Tente novamente.', 'danger')
    else:
        try:
            db.session.delete(curtida)
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash('Não foi possível remover a curtida. Tente novamente.', 'danger')

    return redirect(url_for('feed'))

@app.route('/pesquisar', methods=['GET', 'POST'])
@login_required
def pesquisar():
    if request.method == 'POST': # verifica se o método é POST
        termo = request.form.get('termo') # pega o termo de pesquisa do formulário
        if termo:
            resultados = Usuario.query.filter(Usuario.username.ilike(f'%{termo}%')).all() # busca usuários cujo username contenha o termo, ignorando maiúsculas/minúsculas
            return render_template('perfil.search', resultados=resultados, termo=termo) # renderiza a página de pesquisa com os resultados 
    return render_template('perfil.search', resultados=[], termo='')
