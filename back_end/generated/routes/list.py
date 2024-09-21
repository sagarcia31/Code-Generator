from .controllers.ProdutoController import produto_blueprint

def register_produto_routes(app):
    app.register_blueprint(produto_blueprint)