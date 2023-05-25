from flask import render_template, url_for, request, flash, redirect
from comunidadeintergard.forms import FormCriarConta, FormLogin
from comunidadeintergard.models import Post, Usuario
from comunidadeintergard import app, database, bcrypt
from flask_login import login_user

lista_usuario = ['Thiarly', 'Luca', 'Laila', 'Clara']

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/contato")
def contato():
    return render_template('contato.html')

@app.route("/usuarios")
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
            return redirect(url_for('home'))
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
