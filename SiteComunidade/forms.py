from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtform.validators import DataRequired, Length, Email, EqField

class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqField('senha')])
    botao_sumit_criarconta = SubmitField('Criar Conta')


class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email])
    senha = PasswordField('Senha', validators=[DataRequired(), length(6, 20)])
    botao_sumit_login = SubmitField('Fazer Login')
