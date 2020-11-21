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
    id_Usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String)
    senha = db.Column(db.String)
    adm = db.Column(db.String)

    #CONSTRUTOR
    def __init__(self,email,senha,adm):
        self.email = email
        self.senha = senha
        self.adm = adm

db.create_all()

#ROTA DA PAGINA INDEX
@app.route('/')
def index():
    return render_template('index.html')

#ROTA DA PAGINA USUÁRIO
@app.route('/usuario')
def usuario():
    return render_template('usuario.html')

#ROTA DA  PAGINA DO CADASTRO
@app.route('/cadastrarUsuario')
def cadastrarUsuario():
    return render_template('cadastroUsuario.html')

#ROTA DO METODO DE CADASTRAR
@app.route('/cadastrarUsuario', methods=['GET', 'POST'])
#METODO DE CADASTRAR
def cadastroUsuario():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        adm = request.form.get('adm')

        if email and senha and adm:
            u = Usuario(email, senha, adm)
            db.session.add(u)
            db.session.commit()

        return redirect(url_for('usuario'))

#ROTA DA PAGINA DE LISTA
@app.route('/listaUsuario')
#METODO DE LISTAR
def listaUsuario():
    usuarios = Usuario.query.all()
    return render_template('listaUsuario.html', usuarios=usuarios)

#excluir pelo ID
@app.route('/excluirUsuario/<int:id>')
def excluirUsuario(id):
    usuario = Usuario.query.filter_by(id_Usuario =id).first()
    db.session.delete(usuario)
    db.session.commit()
    #apos excluir vai voltar para pagina de listar
    usuarios = usuario.query.all()
    return render_template('listaUsuario.html', usuarios=usuarios)

#ATUALIZAR pelo ID recebendo um get do parametro e retornando um post
@app.route('/atualizarUsuario/<int:id>', methods=['GET', 'POST'])
def atualizarUsuario(id):
    usuario = Usuario.query.filter_by(id_Usuario=id).first()
    
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        adm = request.form.get('adm')


        if email and senha and adm:
            usuario.email = email
            usuario.senha = senha
            usuario.adm = adm

            db.session.commit()

            return redirect(url_for('listaUsuario'))

    return render_template('atualizarUsuario.html',usuario=usuario)
#----------------------------------------------------------------CLASSE PRODUTO--------------------------------------------------------------------
























#inicia o aplicativo
if __name__ == '__main__':
    app.run(debug=True)