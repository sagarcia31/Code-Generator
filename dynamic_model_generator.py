from jinja2 import Template

def generate_dynamic_model(entity_name, properties):
    # Criar o código do modelo dinamicamente
    model_template = """
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class {{ entity_name }}(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    {% for prop, dtype in properties.items() %}
    {{ prop }} = db.Column(db.{{ dtype }})
    {% endfor %}

    def __init__(self, {% for prop in properties.keys() %}{{ prop }}, {% endfor %}):
        {% for prop in properties.keys() %}
        self.{{ prop }} = {{ prop }}
        {% endfor %}
    """
    
    template = Template(model_template)
    return template.render(entity_name=entity_name, properties=properties)