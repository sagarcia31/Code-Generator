import json
import os
from back_end.generator import generate_model, generate_controller, generate_repository, generate_routes
from front_end.generator import generate_component, generate_service, generate_routes as generate_fe_routes
from process_story import process_user_story
from process_bdd import process_bdd
from figma_integration.extract_design import extract_design_from_figma, map_figma_to_component

def load_template_mapping():
    with open('config/template_mapping.json', 'r') as f:
        return json.load(f)

def orchestrate_generation(user_story, bdd_scenario, tech_stack, figma_file_key=None, figma_access_token=None):
    template_mapping = load_template_mapping()

    story_data = process_user_story(user_story)
    bdd_data = process_bdd(bdd_scenario)

    if figma_file_key and figma_access_token:
        try:
            figma_data = extract_design_from_figma(figma_file_key, figma_access_token)
            figma_components = map_figma_to_component(figma_data)
        except Exception as e:
            print(f"Falha ao integrar com Figma: {e}")
            figma_components = {}

    entity_name = story_data['model_name']
    action_name = story_data['method']
    entity_var = story_data['model_instance']
    properties = bdd_data['properties']

    backend_templates = template_mapping['backend'][tech_stack['backend']]
    frontend_templates = template_mapping['frontend'][tech_stack['frontend']]

    model_code = generate_model(backend_templates['model'], entity_name, properties)
    controller_code = generate_controller(backend_templates['controller'], entity_name, entity_var, properties, bdd_data)
    repository_code= generate_repository(backend_templates['repository'], entity_name, entity_var)
    routes_code = generate_routes(backend_templates['routes'], entity_name, entity_var)
    service_code = generate_service(backend_templates['service'], entity_name, properties)

    generated_backend_base_dir = 'back_end/generated/'
    backend_models = generated_backend_base_dir + 'models'
    backend_controllers = generated_backend_base_dir + 'controllers'
    backend_repositories = generated_backend_base_dir + 'repositories'
    backend_routes = generated_backend_base_dir + 'routes'
    backend_services = generated_backend_base_dir + 'services'
    
    os.makedirs(backend_models, exist_ok=True)
    os.makedirs(backend_controllers, exist_ok=True)
    os.makedirs(backend_routes, exist_ok=True)
    os.makedirs(backend_repositories, exist_ok=True)
    os.makedirs(backend_services, exist_ok=True)

    with open(f'{backend_models}/{entity_name.lower()}.py', 'w') as f:
        f.write(model_code)
    with open(f'{backend_controllers}/{action_name}.py', 'w') as f:
        f.write(controller_code)
    with open(f'{backend_repositories}/{action_name}.py', 'w') as f:
        f.write(repository_code)
    with open(f'{backend_routes}/{action_name}.py', 'w') as f:
        f.write(routes_code)
    with open(f'{backend_services}/{action_name}.py', 'w') as f:
        f.write(service_code)

    # Reativar a geração de front-end se necessário

    print(f"Código gerado com sucesso para a entidade {entity_name}!")

if __name__ == "__main__":
    user_story = "Como um usuário, eu quero visualizar uma lista de produtos para que eu possa escolher um produto"
    bdd_scenario = """
       Dado que o produto tem um nome, preço e quantidade definidos. 
       Quando o usuário entra na página pela primeira vez. 
       Então a lista com os produtos deve ser exibida.
    """
    tech_stack = {"backend": "flask", "frontend": "react"}
    orchestrate_generation(user_story, bdd_scenario, tech_stack)