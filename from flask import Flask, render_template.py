from flask import Flask, render_template, request, jsonify
import sqlite3
import qrcode
import os

app = Flask(__name__)

# Configuração do Banco de Dados
def init_db():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        phone TEXT,
                        address TEXT,
                        cep TEXT,
                        total_price REAL,
                        status TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Página Inicial
@app.route('/cardapio')
def index():
    menu = [
        {"id": 1, "name": "Pizza de Calabresa", "price": 30.0, "image": "static/images/pizza.jpg"},
        {"id": 2, "name": "Hambúrguer Artesanal", "price": 25.0, "image": "static/images/hamburguer.jpg"},
        {"id": 3, "name": "Salada Caesar", "price": 20.0, "image": "static/images/salada.jpg"},
        {"id": 4, "name": "Sushi Combo", "price": 40.0, "image": "static/images/sushi.jpg"},
        {"id": 5, "name": "Lasanha Bolonhesa", "price": 35.0, "image": "static/images/lasanha.jpg"},
        {"id": 6, "name": "Suco Natural", "price": 8.0, "image": "static/images/suco.jpg"}
    ]
    return render_template('index.html', menu=menu)

# Rota para calcular o preço final
@app.route('/calculate_price', methods=['POST'])
def calculate_price():
    data = request.json
    items = data.get('items', [])
    delivery = data.get('delivery', False)
    cep = data.get('cep', '')
    
    base_price = sum(item['price'] * item['quantity'] for item in items)
    delivery_fee = 0
    
    if delivery and cep:
        distance_km = calculate_distance(cep)
        delivery_fee = distance_km * 1  # R$1 por km
    
    total_price = base_price + delivery_fee
    return jsonify({'total_price': total_price, 'delivery_fee': delivery_fee})

# Simulação de cálculo de distância
# (Em um projeto real, usaria uma API como Google Maps)
def calculate_distance(cep):
    return 5  # Supondo sempre 5 km para teste

# Gerar QR Code para pagamento
@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.json
    pix_key = "suachavepix@banco.com"
    total_price = data.get('total_price', 0)
    
    pix_code = f'00020126330014BR.GOV.BCB.PIX0114{pix_key}5204000053039865802BR5925Restaurante Exemplo6009SAO PAULO6304ABCD'
    
    qr = qrcode.make(pix_code)
    qr_path = os.path.join('static', 'qrcode.png')
    qr.save(qr_path)
    
    return jsonify({'qr_code': qr_path})

if __name__ == '__main__':
    app.run(debug=True)
