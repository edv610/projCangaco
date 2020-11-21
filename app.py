from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

#CONFIGURANDO FLASK E O BANCO
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)
#----------------------------------------------------------------CLASSE USUÁIO--------------------------------------------------------------------
class Usuario(db.Model):
    #CRIAÇÃO DA TABELA DO BANCO
    __tablename='usuario'
    _idUsuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String)
    senha = db.Column(db.String)
    adm = db.Column(db.Boolean)

    #CONSTRUTOR
    def __init__(self,email,senha,adm):
        self.email = email
        self.senha = senha
        self.adm = adm
db.create_all()
#ROTA DA PAGINA INDEX
