@produto_blueprint.route('/produto', methods=['POST'])
def create_produto():
    data = request.json
    return jsonify(produto_service.create(data))