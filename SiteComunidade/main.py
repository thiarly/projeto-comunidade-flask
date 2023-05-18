from flask import Flask, render_template, url_for
from forms import FormLogin, FormCriarConta

app = Flask(__name__)


lista_usuario = ['Thiarly', 'Luca', 'Laila', 'Clara']

app.config['SECRET_KEY'] = '6e9142134c8c3b306eef0ce3c1d5d585'

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
    # criar função if para verificar o botao login

    # criar função if para verificar o botão criarconta

    
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)

if __name__ == '__main__':
    app.run(debug=True)
