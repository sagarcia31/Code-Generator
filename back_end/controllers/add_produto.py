from flask import request, jsonify
from .models import Produto, db

def add_produto():
    data = request.get_json()
    new_produto = Produto(
        
        name=data['name'],
        
        price=data['price'],
        
        quantity=data['quantity'],
        
    )
    db.session.add(new_produto)
    db.session.commit()
    return jsonify({'message': 'Produto adicionado com sucesso!'}), 201