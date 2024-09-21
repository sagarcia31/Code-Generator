from .models import Produto

class ProdutoRepository:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        return Produto.query.all()

    def get_by_id(self, id):
        return Produto.query.get(id)

    def create(self, data):
        new_produto = Produto(**data)
        self.db.session.add(new_produto)
        self.db.session.commit()
        return new_produto

    def delete(self, id):
        produto = self.get_by_id(id)
        if produto:
            self.db.session.delete(produto)
            self.db.session.commit()
            return True
        return False