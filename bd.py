from app import app, db, Produto, Pedido, Usuario
with app.app_context():
    produtos = Produto.query.all()
    for p in produtos:
        print(p.nome)
    pedidos = Pedido.query.all()
    for e in pedidos:
        print(e.cliente_id)
    usuarios = Usuario.query.all()
    for u in usuarios:
        print(u.id, u.nome)        
#produtos = Produto.query.all()
#pedidos = Pedido.query.all()
#print(produtos)