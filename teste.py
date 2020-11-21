from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

#CONFIGURANDO FLASK E O BANCO
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)
#----------------------------------------------------------------CLASSE USUÁIO--------------------------------------------------------------------
class Pessoa(db.Model):
    #CRIAÇÃO DA TABELA DO BANCO
    __tablename='cliente'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String)
    telefone = db.Column(db.String)
    cpf = db.Column(db.String)
    email = db.Column(db.String)

    #CONSTRUTOR
    def __init__(self,nome,telefone,cpf,email):
        self.nome = nome
        self.telefone = telefone
        self.cpf = cpf
        self.email = email

db.create_all()

#ROTA DA PAGINA INDEX
@app.route('/')
def index():
    return render_template('index.html')

#ROTA DA  PAGINA DO CADASTRO
@app.route('/cadastrar')
def cadastrar():
    return render_template('cadastro.html')

#ROTA DO METODO DE CADASTRAR
@app.route('/cadastro', methods=['GET', 'POST'])
#METODO DE CADASTRAR
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        cpf = request.form.get('cpf')
        email = request.form.get('email')

        if nome and telefone and cpf and email:
            p = Pessoa(nome, telefone, cpf, email)
            db.session.add(p)
            db.session.commit()

        return redirect(url_for('index'))

#ROTA DA PAGINA DE LISTA
@app.route('/lista')
#METODO DE LISTAR
def lista():
    pessoas = Pessoa.query.all()
    return render_template('lista.html', pessoas=pessoas)

#excluir pelo ID
@app.route('/excluir/<int:id>')
def excluir(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()
    db.session.delete(pessoa)
    db.session.commit()
    #apos excluir vai voltar para pagina de listar
    pessoas = Pessoa.query.all()
    return render_template('lista.html', pessoas=pessoas)

#ATUALIZAR pelo ID recebendo um get do parametro e retornando um post
@app.route('/atualizar/<int:id>', methods=['GET', 'POST'])
def atualizar(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        cpf = request.form.get('cpf')
        email = request.form.get('email')

        if nome and telefone and cpf and email:
            pessoa.nome = nome
            pessoa.telefone = telefone
            pessoa.cpf = cpf
            pessoa.email = email

            db.session.commit()

            return redirect(url_for('lista'))

    return render_template('atualizar.html',pessoa=pessoa)

#inicia o aplicativo
if __name__ == '__main__':
    app.run(debug=True)
