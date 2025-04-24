import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/images'

db = SQLAlchemy(app)

# Modelo para armazenar os produtos
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    imagem = db.Column(db.String(100), nullable=False)

# Modelo para armazenar pedidos
class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itens = db.Column(db.Text, nullable=False)
    total = db.Column(db.Float, nullable=False)
    endereco = db.Column(db.String(200), nullable=True)
    tipo_entrega = db.Column(db.String(50), nullable=False)

# Criar o banco de dados
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    produtos = Produto.query.all()
    return render_template('index.html', produtos=produtos)

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    descricao = request.form['descricao']
    preco = float(request.form['preco'])
    imagem = request.files['imagem']

    if imagem:
        filename = secure_filename(imagem.filename)
        upload_folder = app.config['UPLOAD_FOLDER']
        # 🔹 Criar a pasta 'static/images' se não existir
        os.makedirs(upload_folder, exist_ok=True)
        imagem_path = os.path.join(upload_folder, filename)
        imagem.save(imagem_path)

        novo_produto = Produto(nome=nome, descricao=descricao, preco=preco, imagem=filename)
        db.session.add(novo_produto)
        db.session.commit()
    
    return redirect(url_for('cadastro'))

@app.route('/finalizar_pedido', methods=['POST'])
def finalizar_pedido():
    itens = request.form['itens']
    total = float(request.form['total'])
    endereco = request.form.get('endereco', '')
    tipo_entrega = request.form['tipo_entrega']

    pedido = Pedido(itens=itens, total=total, endereco=endereco, tipo_entrega=tipo_entrega)
    db.session.add(pedido)
    db.session.commit()
    
    return "Pedido cadastrado com sucesso!"

if __name__ == '__main__':
    app.run(debug=True)
