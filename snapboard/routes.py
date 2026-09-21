from flask import render_template, url_for, flash, redirect, current_app, request, send_from_directory
from snapboard import app, db, bcrypt
from snapboard.forms import FormLogin, FormCriarConta, FormFoto, FormEditarPerfil, FormAlterarSenha
from snapboard.models import Usuario, Postagem, Curtida, Seguidor
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy.orm import joinedload
import uuid
import os
from werkzeug.utils import secure_filename
from PIL import Image

def validar_e_salvar_imagem(arquivo, pasta_destino):
    """Confere que o arquivo enviado é realmente uma imagem (não só a
    extensão) e salva com um nome único. Levanta ValueError com uma
    mensagem amigável se o arquivo não for válido."""
    try:
        Image.open(arquivo.stream).verify()
        arquivo.stream.seek(0)
    except Exception:
        raise ValueError('O arquivo enviado não é uma imagem válida.')

    extensao = secure_filename(arquivo.filename).rsplit('.', 1)[-1].lower()
    nome_unico = f"{uuid.uuid4().hex}.{extensao}"   # elimina colisão entre usuários
    caminho = os.path.join(pasta_destino, nome_unico)

    try:
        arquivo.save(caminho)
    except Exception:
        raise ValueError('Não foi possível salvar o arquivo. Tente novamente.')

    return nome_unico

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
    return redirect(url_for('login'))

@app.route("/perfil/<int:id_usuario>", methods=['GET', 'POST'])   # <int:> em vez de string livre
@login_required
def perfil(id_usuario):
    if id_usuario == current_user.id:
        form = FormFoto()
        if form.validate_on_submit():
            arquivo = form.foto.data

            try:
                nome_unico = validar_e_salvar_imagem(arquivo, current_app.config['UPLOAD_FOLDER'])
            except ValueError as erro:
                flash(str(erro), 'danger')
                return redirect(url_for('perfil', id_usuario=current_user.id))

            try:
                foto = Postagem(imagem=nome_unico, id_usuario=current_user.id)
                db.session.add(foto)
                db.session.commit()
            except Exception:
                db.session.rollback()
                flash('Não foi possível salvar sua foto. Tente novamente.', 'danger')
                return redirect(url_for('perfil', id_usuario=current_user.id))

            return redirect(url_for('perfil', id_usuario=current_user.id))
        return render_template(
            'perfil.html', usuario=current_user, form=form, segue=False,
            contagem_seguidores=current_user.seguidores.count(),
            contagem_seguindo=current_user.seguindo.count(),
        )
    else:
        usuario = Usuario.query.get_or_404(id_usuario)   # get_or_404 em vez de get
        return render_template(
            'perfil.html', usuario=usuario, form=None,
            segue=current_user.segue(usuario),
            contagem_seguidores=usuario.seguidores.count(),
            contagem_seguindo=usuario.seguindo.count(),
        )

@app.route('/seguir/<int:id_usuario>', methods=['POST'])
@login_required
def seguir(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    eh_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if usuario.id == current_user.id:
        if eh_ajax:
            return {'sucesso': False, 'mensagem': 'Você não pode seguir a si mesmo.'}, 400
        flash('Você não pode seguir a si mesmo.', 'danger')
        return redirect(url_for('perfil', id_usuario=id_usuario))

    relacao = Seguidor.query.filter_by(id_seguidor=current_user.id, id_seguido=usuario.id).first()

    if not relacao:
        try:
            db.session.add(Seguidor(id_seguidor=current_user.id, id_seguido=usuario.id))
            db.session.commit()
            seguindo_agora = True
        except Exception:
            db.session.rollback()
            if eh_ajax:
                return {'sucesso': False, 'mensagem': 'Não foi possível seguir.'}, 500
            flash('Não foi possível seguir. Tente novamente.', 'danger')
            return redirect(url_for('perfil', id_usuario=id_usuario))
    else:
        try:
            db.session.delete(relacao)
            db.session.commit()
            seguindo_agora = False
        except Exception:
            db.session.rollback()
            if eh_ajax:
                return {'sucesso': False, 'mensagem': 'Não foi possível deixar de seguir.'}, 500
            flash('Não foi possível deixar de seguir. Tente novamente.', 'danger')
            return redirect(url_for('perfil', id_usuario=id_usuario))

    if eh_ajax:
        return {
            'sucesso': True,
            'seguindo': seguindo_agora,
            'total_seguidores': usuario.seguidores.count(),
        }

    return redirect(url_for('perfil', id_usuario=id_usuario))

@app.route('/perfil/<int:id_usuario>/seguidores')
@login_required
def lista_seguidores(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    pessoas = [r.seguidor for r in usuario.seguidores.order_by(Seguidor.data_criacao.desc()).all()]
    ids_que_sigo = {r.id_seguido for r in current_user.seguindo.all()}
    return render_template(
        'lista_usuarios.html', usuario_perfil=usuario, titulo='Seguidores',
        pessoas=pessoas, ids_que_sigo=ids_que_sigo
    )

@app.route('/perfil/<int:id_usuario>/seguindo')
@login_required
def lista_seguindo(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    pessoas = [r.seguido for r in usuario.seguindo.order_by(Seguidor.data_criacao.desc()).all()]
    ids_que_sigo = {r.id_seguido for r in current_user.seguindo.all()}
    return render_template(
        'lista_usuarios.html', usuario_perfil=usuario, titulo='Seguindo',
        pessoas=pessoas, ids_que_sigo=ids_que_sigo
    )

@app.route("/perfil/editar", methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil(obj=current_user)
    form_senha = FormAlterarSenha()

    if form.validate_on_submit():
        if form.foto_perfil.data:
            try:
                nome_unico = validar_e_salvar_imagem(form.foto_perfil.data, current_app.config['AVATAR_FOLDER'])
            except ValueError as erro:
                flash(str(erro), 'danger')
                return redirect(url_for('editar_perfil'))

            avatar_antigo = current_user.foto_perfil
            current_user.foto_perfil = nome_unico

            # só remove o avatar antigo depois de confirmar que o novo foi salvo
            if avatar_antigo:
                caminho_antigo = os.path.join(current_app.config['AVATAR_FOLDER'], avatar_antigo)
                if os.path.exists(caminho_antigo):
                    os.remove(caminho_antigo)

        current_user.username = form.username.data
        current_user.bio = form.bio.data

        try:
            db.session.commit()
            flash('Perfil atualizado com sucesso!', 'success')
        except Exception:
            db.session.rollback()
            flash('Não foi possível salvar as alterações. Tente novamente.', 'danger')

        return redirect(url_for('perfil', id_usuario=current_user.id))

    return render_template('editar_perfil.html', form=form, form_senha=form_senha)

@app.route("/perfil/alterar-senha", methods=['POST'])
@login_required
def alterar_senha():
    form = FormEditarPerfil(obj=current_user)  # só pra re-renderizar a página em caso de erro
    form_senha = FormAlterarSenha()

    if form_senha.validate_on_submit():
        if not bcrypt.check_password_hash(current_user.senha, form_senha.senha_atual.data):
            flash('Senha atual incorreta.', 'danger')
        else:
            current_user.senha = bcrypt.generate_password_hash(form_senha.nova_senha.data).decode('utf-8')
            try:
                db.session.commit()
                flash('Senha alterada com sucesso!', 'success')
                return redirect(url_for('perfil', id_usuario=current_user.id))
            except Exception:
                db.session.rollback()
                flash('Não foi possível alterar a senha. Tente novamente.', 'danger')

    return render_template('editar_perfil.html', form=form, form_senha=form_senha)

@app.route("/feed")
@login_required
def feed():
    pagina = request.args.get('pagina', 1, type=int)
    termo = request.args.get('q', '', type=str).strip()

    consulta = Postagem.query.options(joinedload(Postagem.usuario))  # evita 1 query extra por postagem (N+1)

    if termo:
        # Filtra no banco (antes o filtro só acontecia no JS, em cima dos
        # 20 posts já carregados na página — resultados em outras páginas
        # de paginação nunca eram encontrados).
        consulta = consulta.join(Usuario).filter(Usuario.username.ilike(f'%{termo}%'))

    paginacao = (
        consulta
        .order_by(Postagem.data_criacao.desc())
        .paginate(page=pagina, per_page=20, error_out=False)
    )

    usuario_encontrado = None
    if termo and paginacao.total == 0:
        # O termo pesquisado pode ser de um usuário que existe mas ainda
        # não publicou nada — nesse caso não há post pra filtrar, mas
        # ainda faz sentido levar direto para o perfil dele.
        usuario_encontrado = Usuario.query.filter(Usuario.username.ilike(f'%{termo}%')).first()

    # ids das postagens que o usuário atual já curtiu, pra pintar o
    # coração certo sem precisar de uma query por postagem (N+1).
    ids_pagina = [p.id for p in paginacao.items]
    curtidas_usuario = set()
    if ids_pagina:
        curtidas_usuario = {
            c.id_postagem for c in Curtida.query.filter(
                Curtida.id_usuario == current_user.id,
                Curtida.id_postagem.in_(ids_pagina)
            ).all()
        }

    return render_template(
        'feed.html',
        fotos=paginacao.items,
        paginacao=paginacao,
        termo_pesquisa=termo,
        usuario_encontrado=usuario_encontrado,
        curtidas_usuario=curtidas_usuario,
    )

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
    # NOTA: o feed atual linka a imagem/download direto para
    # /static/posts/<arquivo>, que o Flask serve publicamente e sem
    # autenticação — essa rota (restrita ao dono) hoje não é chamada
    # por nenhum template. Ficou assim por decisão consciente de manter
    # o comportamento atual sem mexer no front-end; ver relatório.

    postagem = Postagem.query.get_or_404(id)# validar se a postagem existe

    # Apenas o dono da postagem pode baixar por esta rota.
    # (nome do campo corrigido: o model usa id_usuario, não usuario_id —
    # antes disso a checagem sempre lançava AttributeError)
    if postagem.id_usuario != current_user.id:
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
    curtida = Curtida.query.filter_by(id_usuario=current_user.id, id_postagem=id).first()
    eh_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if not curtida:
        try:
            db.session.add(Curtida(id_usuario=current_user.id, id_postagem=id))
            db.session.commit()
            curtiu_agora = True
        except Exception:
            db.session.rollback()
            if eh_ajax:
                return {'sucesso': False, 'mensagem': 'Não foi possível curtir a postagem.'}, 500
            flash('Não foi possível curtir a postagem. Tente novamente.', 'danger')
            return redirect(url_for('feed'))
    else:
        try:
            db.session.delete(curtida)
            db.session.commit()
            curtiu_agora = False
        except Exception:
            db.session.rollback()
            if eh_ajax:
                return {'sucesso': False, 'mensagem': 'Não foi possível remover a curtida.'}, 500
            flash('Não foi possível remover a curtida. Tente novamente.', 'danger')
            return redirect(url_for('feed'))

    if eh_ajax:
        return {'sucesso': True, 'curtiu': curtiu_agora, 'total': len(postagem.curtidas)}

    return redirect(url_for('feed'))

@app.route('/pesquisar', methods=['GET', 'POST'])
@login_required
def pesquisar():
    # Corrigido: antes chamava render_template('perfil.search', ...), um
    # nome de template inexistente — toda requisição a /pesquisar
    # derrubava a aplicação com TemplateNotFound. O front-end atual já
    # resolve a busca via /feed?q=termo, então esta rota agora só
    # redireciona para lá em vez de duplicar essa lógica com uma tela
    # própria (que também não existe hoje).
    termo = request.form.get('termo') or request.args.get('termo', '')
    return redirect(url_for('feed', q=termo) if termo else url_for('feed'))


# =====================================================
# TRATAMENTO DE ERROS
# Antes, qualquer 404/403/500 mostrava a página padrão
# do Flask/Werkzeug. Estas páginas usam o mesmo visual
# do restante do site (base.css / auth.css).
# =====================================================

@app.errorhandler(404)
def erro_404(erro):
    return render_template('erro.html', codigo=404,
                            titulo='Página não encontrada',
                            mensagem='O que você procurava não existe ou foi removido.'), 404

@app.errorhandler(403)
def erro_403(erro):
    return render_template('erro.html', codigo=403,
                            titulo='Acesso não autorizado',
                            mensagem='Você não tem permissão para acessar este recurso.'), 403

@app.errorhandler(413)
def erro_413(erro):
    return render_template('erro.html', codigo=413,
                            titulo='Arquivo muito grande',
                            mensagem='O arquivo enviado passa do limite de 5 MB. Escolha uma imagem menor.'), 413

@app.errorhandler(500)
def erro_500(erro):
    db.session.rollback()  # garante que uma transação quebrada não vaze para a próxima requisição
    return render_template('erro.html', codigo=500,
                            titulo='Algo deu errado',
                            mensagem='Ocorreu um erro interno. Já estamos cientes do problema.'), 500
