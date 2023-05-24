from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeintergard.models import Usuario

class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6, max=20)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        check_email = Usuario.query.filter_by(email=email.data).first()
        if check_email:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail.')
    
    def validate_username(self, username):
        check_username = Usuario.query.filter_by(username=username.data).first()
        if check_username:
            raise ValidationError('Usuário já cadastrado. Cadastra-se com outro usuário.')
class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6, max=20)])
    lembrar_dados = BooleanField('Lembrar')
    botao_submit_login = SubmitField('Fazer Login')
