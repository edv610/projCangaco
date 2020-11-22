from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

#CONFIGURANDO FLASK E O BANCO
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)
#----------------------------------------------------------------CLASSE PRODUTO--------------------------------------------------------------------
class Produto(db.Model):
    #CRIAÇÃO DA TABELA DO BANCO
    __tablename='produto'
    _codProduto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomeProduto = db.Column(db.String)
    valorProduto = db.Column(db.Float)
    qntEstoque = db.Column(db.Integer)

    #CONSTRUTOR
    def _init_(self,nomeProduto,valorProduto,qntEstoque):
        self.nomeProduto = nomeProduto
        self.valorProduto = valorProduto
        self.qntEstoque = qntEstoque

db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

#ROTA DA  PAGINA DO CADASTRO
@app.route('/produto/cadastrar')
def cadastrarProdutos():
    return render_template('cadastroProdutos.html')

#ROTA DO METODO DE CADASTRAR
@app.route('/produto/cadastro', methods=['GET', 'POST'])
#METODO DE CADASTRAR
def cadastroProdutos():
    if request.method == 'POST':
        nomeProduto = request.form['nomeProduto']
        valorProduto = request.form['valorProduto']
        qntEstoque = request.form['qntEstoque']

        if nomeProduto and valorProduto and qntEstoque:
            p = Produto(nomeProduto = nomeProduto, valorProduto = valorProduto, qntEstoque = qntEstoque)
            db.session.add(p)
            db.session.commit()

        return redirect(url_for('index'))

#ROTA DA PAGINA DE LISTA
@app.route('/produtos')
#METODO DE LISTAR
def listarProdutos():
    produtos = Produto.query.all()
    return render_template('listaProdutos.html', produtos=produtos)

#excluir pelo ID
@app.route('/produtos/excluir/<int:codProduto>')
def excluirProdutos(codProduto):
    produto = Produto.query.filter_by(_codProduto=codProduto).first()
    db.session.delete(produto)
    db.session.commit()
    #apos excluir vai voltar para pagina de listar
    produtos = Produto.query.all()
    return render_template('listaProdutos.html', produtos=produtos)

#ATUALIZAR pelo ID recebendo um get do parametro e retornando um post
@app.route('/produtos/atualizar/<int:codProduto>', methods=['GET', 'POST'])
def atualizarProdutos(codProduto):
    produto = Produto.query.filter_by(_codProduto=codProduto).first()
    
    if request.method == 'POST':
        nomeP = request.form.get('nomeProduto')
        valorP = request.form.get('valorProduto')
        qntEstoqueP = request.form.get('qntEstoque')

        if nomeP and valorP and qntEstoqueP:
            produto.nomeProduto = nomeP
            produto.valorProduto = valorP
            produto.qntEstoque = qntEstoqueP

            db.session.commit()

            return redirect(url_for('listarProdutos'))

    return render_template('atualizarProdutos.html',produto=produto)


#------------------------------------------------------------------- CLASSE FORNECEDOR -----------------------------------------------------
class Fornecedor(db.Model):
    #CRIAÇÃO DA TABELA DO BANCO
    __tablename='fornecedor'
    _codFornecedor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomeFornecedor = db.Column(db.String)
    telefoneFornecedor = db.Column(db.String)
    cpf_cnpjFornecedor = db.Column(db.String)
    tipoFornecedor = db.Column(db.String)

    #CONSTRUTOR
    def _init_(self,nome,telefone,cpf,email):
        self.nomeFornecedor = nomeFornecedor
        self.telefone = telefone
        self.cpf_cnpjFornecedor = cpf_cnpjFornecedor
        self.tipoFornecedor = tipoFornecedor

db.create_all()
#ROTA DA  PAGINA DO CADASTRO
@app.route('/fornecedor/cadastrar')
def cadastrarFornecedores():
    return render_template('cadastroFornecedores.html')

#ROTA DO METODO DE CADASTRAR
@app.route('/fornecedor/cadastro', methods=['GET', 'POST'])
#METODO DE CADASTRAR
def cadastroFornecedores():
    if request.method == 'POST':
        nomeFornecedor = request.form['nomeFornecedor']
        telefoneFornecedor = request.form['telefoneFornecedor']
        cpf_cnpjFornecedor = request.form['cpf_cnpjFornecedor']
        tipoFornecedor = request.form['tipoFornecedor']

        if nomeFornecedor and telefoneFornecedor and cpf_cnpjFornecedor and tipoFornecedor:
            f = Fornecedor(nomeFornecedor = nomeFornecedor, telefoneFornecedor = telefoneFornecedor, cpf_cnpjFornecedor = cpf_cnpjFornecedor, tipoFornecedor=tipoFornecedor)
            db.session.add(f)
            db.session.commit()

        return redirect(url_for('index'))

#ROTA DA PAGINA DE LISTA
@app.route('/fornecedores')
#METODO DE LISTAR
def listarFornecedores():
    fornecedores = Fornecedor.query.all()
    return render_template('listaFornecedores.html', fornecedores=fornecedores)

#excluir pelo ID
@app.route('/fornecedores/excluir/<int:codFornecedor>')
def excluirFornecedores(codFornecedor):
    fornecedor = Fornecedor.query.filter_by(_codFornecedor=codFornecedor).first()
    db.session.delete(fornecedor)
    db.session.commit()
    #apos excluir vai voltar para pagina de listar
    fornecedores = Fornecedor.query.all()
    return render_template('listaFornecedores.html', fornecedores=fornecedores)

#ATUALIZAR pelo ID recebendo um get do parametro e retornando um post
@app.route('/fornecedores/atualizar/<int:codFornecedor>', methods=['GET', 'POST'])
def atualizarFornecedores(codFornecedor):
    fornecedor = Fornecedor.query.filter_by(_codFornecedor=codFornecedor).first()
    
    if request.method == 'POST':
        nomeF = request.form['nomeFornecedor']
        telefoneF = request.form['telefoneFornecedor']
        cpf_cnpjF = request.form['cpf_cnpjFornecedor']
        tipoF = request.form['tipoFornecedor']

        if nomeF and telefoneF and cpf_cnpjF:
            fornecedor.nomeFornecedor = nomeF
            fornecedor.telefoneFornecedor = telefoneF
            fornecedor.cpf_cnpjFornecedor = cpf_cnpjF
            fornecedor.tipoFornecedor = tipoF

            db.session.commit()

            return redirect(url_for('listarFornecedores'))

    return render_template('atualizarFornecedores.html',fornecedor=fornecedor)

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
        adm = 'False' if request.form.get('adm') is None else 'True'

        if email and senha and adm:
            u = Usuario(email, senha, adm)
            db.session.add(u)
            db.session.commit()

        return redirect(url_for('index'))

#ROTA DA PAGINA DE LISTA
@app.route('/listaUsuario')
#METODO DE LISTAR
def listaUsuario():
    usuarios = Usuario.query.all()
    return render_template('listaUsuario.html', usuarios=usuarios)

#excluir pelo ID
@app.route('/excluirUsuario/<int:id_Usuario>')
def excluirUsuario(id_Usuario):
    usuario = Usuario.query.filter_by(id_Usuario =id_Usuario).first()
    db.session.delete(usuario)
    db.session.commit()
    #apos excluir vai voltar para pagina de listar
    usuarios = usuario.query.all()
    return render_template('listaUsuario.html', usuarios=usuarios)

#ATUALIZAR pelo ID recebendo um get do parametro e retornando um post
@app.route('/atualizarUsuario/<int:id_Usuario>', methods=['GET', 'POST'])
def atualizarUsuario(id_Usuario):
    usuario = Usuario.query.filter_by(id_Usuario=id_Usuario).first()
    
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        adm = 'False' if request.form.get('adm') is None else 'True'


        if email and senha and adm:
            usuario.email = email
            usuario.senha = senha
            usuario.adm = adm

            db.session.commit()

            return redirect(url_for('listaUsuario'))

    return render_template('atualizarUsuario.html',usuario=usuario)



#inicia o aplicativo
if __name__ == '__main__':
    app.run(debug=True)
