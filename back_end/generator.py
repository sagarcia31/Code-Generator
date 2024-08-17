from jinja2 import Environment, FileSystemLoader
import os

def generate_code(template_path, **context):
    template_dir = os.path.dirname(template_path)
    template_name = os.path.basename(template_path)

    template_env = Environment(loader=FileSystemLoader(searchpath=template_dir))
    template = template_env.get_template(template_name)

    return template.render(context)

def generate_model(template_path, entity_name, properties):
    return generate_code(template_path, entity_name=entity_name, properties=properties)

def generate_controller(template_path, entity_name, entity_var, properties, bdd_data):
    return generate_code(
        template_path,
        entity_name=entity_name,
        entity_var=entity_var,
        properties=properties,
        bdd_conditions=bdd_data['conditions'],
        bdd_action=bdd_data['action'],
        bdd_expected_result=bdd_data['expected_result']
    )

def generate_routes(template_path, entity_name):
    return generate_code(template_path, entity_name=entity_name)