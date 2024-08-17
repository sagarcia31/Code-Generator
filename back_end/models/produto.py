from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(255))
    
    price = db.Column(db.Float)
    
    quantity = db.Column(db.Integer)
    

    def __init__(self, name, price, quantity, ):
        
        self.name = name
        
        self.price = price
        
        self.quantity = quantity
        