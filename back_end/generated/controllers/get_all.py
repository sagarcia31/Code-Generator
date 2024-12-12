from flask import Blueprint, request, jsonify

produto_blueprint = Blueprint('produto', __name__)

get_all

# Serviço injetado aqui
produto_service = ProdutoService(ProdutoRepository(db))