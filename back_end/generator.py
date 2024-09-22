from jinja2 import Environment, FileSystemLoader
import os

def generate_code(template_path, **context):
    template_dir = os.path.dirname(template_path)
    template_name = os.path.basename(template_path)

    template_env = Environment(loader=FileSystemLoader(searchpath=template_dir))
    template = template_env.get_template(template_name)

    return template.render(context)

def generate_model(template_path, entity_name, properties):
    """
    Gera o código do Model.
    
    :param template_path: Caminho do template do model.
    :param entity_name: Nome da entidade.
    :param properties: Propriedades da entidade.
    :return: Código gerado do model.
    """
    return generate_code(template_path, entity_name=entity_name, properties=properties)

def generate_controller(template_path, entity_name, entity_var, properties, bdd_data):
    """
    Gera o código do Controller.
    
    :param template_path: Caminho do template do controller.
    :param entity_name: Nome da entidade.
    :param entity_var: Nome da entidade em formato de variável (minúsculo).
    :param properties: Propriedades da entidade.
    :param bdd_data: Dados extraídos do BDD.
    :return: Código gerado do controller.
    """
    return generate_code(
        template_path,
        entity_name=entity_name,
        entity_var=entity_var,
        properties=properties,
        bdd_conditions=bdd_data['conditions'],
        bdd_action=bdd_data['action'],
        bdd_expected_result=bdd_data['expected_result']
    )

def generate_repository(template_path, entity_name, entity_var):
    """
    Gera o código do Repository a partir do template.

    :param template_path: Caminho do template do repository.
    :param entity_name: Nome da entidade.
    :param entity_var: Nome da entidade em formato de variável (minúsculo).
    :return: Código gerado do repository.
    """
    return generate_code(template_path, entity_name=entity_name, entity_var=entity_var)

def generate_service(template_path, entity_name, entity_var):
    """
    Gera o código do Service a partir do template.

    :param template_path: Caminho do template do service.
    :param entity_name: Nome da entidade.
    :param entity_var: Nome da entidade em formato de variável (minúsculo).
    :return: Código gerado do service.
    """
    return generate_code(template_path, entity_name=entity_name, entity_var=entity_var)

def generate_routes(template_path, entity_name, entity_var):
    """
    Gera o código das Rotas a partir do template.

    :param template_path: Caminho do template das rotas.
    :param entity_name: Nome da entidade.
    :param entity_var: Nome da entidade em formato de variável (minúsculo).
    :return: Código gerado das rotas.
    """
    return generate_code(template_path, entity_name=entity_name, entity_var=entity_var)