from flask import Blueprint, request, jsonify

produto_blueprint = Blueprint('produto', __name__)

@produto_blueprint.route('/produto', methods=['GET'])
def get_produto():
    return jsonify(produto_service.get_all())

@produto_blueprint.route('/produto/<id>', methods=['GET'])
def get_produto_by_id(id):
    return jsonify(produto_service.get_by_id(id))

@produto_blueprint.route('/produto', methods=['POST'])
def create_produto():
    data = request.json
    return jsonify(produto_service.create(data))

@produto_blueprint.route('/produto/<id>', methods=['DELETE'])
def delete_produto(id):
    return jsonify(produto_service.delete(id))