import os
import json
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'chave_secreta'
app.config['UPLOAD_FOLDER'] = 'static/images'
db = SQLAlchemy(app)

# Criar o banco de dados
with app.app_context():
     db.create_all()

    

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)

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
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    itens = db.Column(db.Text, nullable=False)
    total = db.Column(db.Float, nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    tipo_entrega = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Recebido')

    cliente = db.relationship('Usuario', backref=db.backref('Pedido', lazy=True))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        user = Usuario.query.filter_by(usuario=usuario).first()
        
        if user and check_password_hash(user.senha, senha):
            session['usuario'] = user.usuario
            session['usuario_id'] = user.id  # 🔹 Salva o ID também
            return redirect(url_for('opcoes'))
        else:
            return 'Usuário ou senha incorretos'
        
# Busca todos os produtos para mostrar no rodapé
    produtos = Produto.query.all()
    return render_template('login.html', produtos=produtos)    

@app.route('/opcoes', methods=['GET', 'POST'])
def opcoes():
      if 'usuario' not in session:
            return redirect(url_for('login.html'))
      return render_template('dashboard.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        usuario = request.form['usuario']
        senha = generate_password_hash(request.form['senha'])
        
        novo_usuario = Usuario(nome=nome, telefone=telefone, endereco=endereco, usuario=usuario, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    return render_template('cadastro_cliente.html'  )

@app.route('/menu')
def menu():
    produtos = Produto.query.all()
    if 'usuario' not in session:
        return redirect(url_for('login.html'))
    return render_template('menu.html', produtos=produtos)

@app.route('/pedidos')
def pedidos():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    cliente_id = session['usuario_id']
    nome_usuario = session.get('usuario')  # pega o nome do usuário armazenado na sessão
    pedidos = Pedido.query.filter_by(cliente_id=cliente_id).order_by(Pedido.id.desc()).all()

    # Converte os itens de cada pedido de JSON string para lista de dicionários
    for pedido in pedidos:
        try:
            pedido.itens = json.loads(pedido.itens)
        except:
            pedido.itens = []

    return render_template('pedidos.html', pedidos=pedidos, nome=nome_usuario)

@app.route('/cadastro_p')
def cadastro_p():
    return render_template('cadastro_produtos.html')

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
    
    return redirect(url_for('cadastro_p'))

@app.route('/finalizar_pedido', methods=['POST'])
def finalizar_pedido():
    data = request.get_json()
    cliente_id = session.get('usuario_id')

    if not cliente_id:
        return jsonify({'success': False, 'message': 'Usuário não autenticado'})

    novo_pedido = Pedido(
        cliente_id=cliente_id,
        itens=json.dumps(data['itens']),
        total=data['total'],
        endereco=data['endereco'],
        tipo_entrega=data['tipo_entrega'],
        status='Recebido'
    )
    db.session.add(novo_pedido)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Pedido salvo com sucesso'})



if __name__ == '__main__':
    with app.app_context():
         db.create_all()
    app.run(debug=True)
