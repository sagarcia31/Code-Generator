from jinja2 import Environment, FileSystemLoader
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')

def generate_component(entity_name):
    template_env = Environment(loader=FileSystemLoader(searchpath=template_dir))
    template = template_env.get_template('component.js.hbs')
    return template.render(entity_name=entity_name)

def generate_service(entity_name):
    template_env = Environment(loader=FileSystemLoader(searchpath=template_dir))
    template = template_env.get_template('service.js.hbs')
    return template.render(entity_name=entity_name)

def generate_routes(entity_name):
    template_env = Environment(loader=FileSystemLoader(searchpath=template_dir))
    template = template_env.get_template('routes.js.hbs')
    return template.render(entity_name=entity_name)