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



#inicia o aplicativo
if __name__ == '__main__':
    app.run(debug=True)
