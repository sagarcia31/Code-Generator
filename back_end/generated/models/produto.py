

    
        
    

    

    

    

    
        
    

    
        
    

    

    

    

    



from sqlalchemy import Column, String(255), Float, Integer

from .db import db

class Produto(db.Model):
    
    scenario = Column(String(255))
    
    produtos = Column(String(255))
    
    produto = Column(String(255))
    
    nome = Column(String(255))
    
    preço = Column(Float)
    
    quantidade = Column(Integer)
    
    lista = Column(String(255))
    
    produtos = Column(String(255))
    
    lista = Column(String(255))
    
    produtos = Column(String(255))
    