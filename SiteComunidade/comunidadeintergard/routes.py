from flask import render_template, url_for, request, flash, redirect
from comunidadeintergard.forms import FormCriarConta, FormLogin, FormEditarPerfil
from comunidadeintergard.models import Post, Usuario
from comunidadeintergard import app, database, bcrypt
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image

lista_usuario = ['Thiarly', 'Luca', 'Laila', 'Clara']

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/contato")
def contato():
    return render_template('contato.html')

@app.route("/usuarios")
@login_required
def usuarios():
    return render_template('usuarios.html', lista_usuario=lista_usuario)

@app.route("/login&contato", methods=["GET", "POST"])
def login():
    form_login = FormLogin()  # Instância do formulário FormLogin
    form_criarconta = FormCriarConta()  # Instância do formulário FormCriarConta
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('contato'))
        else: 
            flash('Falha no login, E-mail ou Senha incorretos', 'alert-danger')
    
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
         senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
         usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
         database.session.add(usuario)
         database.session.commit()
        
         flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
         return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Logout feito com sucesso', 'alert-success')
    return redirect(url_for('home'))
    
@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)

@app.route('/post/criar')
@login_required
def criar_post():
    return render_template('criarpost.html')

def salvar_imagem(imagem):
    codigo = secrets.token_hex(6)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (600, 600)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo

@app.route('/editar/perfil', methods=["GET", "POST"])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
            
        database.session.commit()
        flash('Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)




   