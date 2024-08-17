from jinja2 import Environment, FileSystemLoader
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')

def generate_model(entity_name, properties):
    template_env = Environment(loader=FileSystemLoader(searchpath=template_dir))
    template = template_env.get_template('model.py.hbs')
    return template.render(entity_name=entity_name, properties=properties)

def generate_controller(action_name, entity_name, entity_var, properties):
    template_env = Environment(loader=FileSystemLoader(searchpath=template_dir))
    template = template_env.get_template('controller.py.hbs')
    return template.render(action_name=action_name, entity_name=entity_name, entity_var=entity_var, properties=properties)

def generate_routes(entity_name):
    template_env = Environment(loader=FileSystemLoader(searchpath=template_dir))
    template = template_env.get_template('routes.py.hbs')
    return template.render(entity_name=entity_name)