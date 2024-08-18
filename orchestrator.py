import json
import os
from back_end.generator import generate_model, generate_controller, generate_routes
from front_end.generator import generate_component, generate_service, generate_routes as generate_fe_routes
from process_story import process_user_story
from process_bdd import process_bdd

def load_template_mapping():
    with open('config/template_mapping.json', 'r') as f:
        return json.load(f)

def orchestrate_generation(user_story, bdd_scenario, tech_stack):
    # Carregar mapeamento de templates
    template_mapping = load_template_mapping()

    # Processa a história de usuário e o BDD
    story_data = process_user_story(user_story)
    bdd_data = process_bdd(bdd_scenario)

    # Extração das informações processadas
    entity_name = story_data['model_name']
    action_name = story_data['method']
    entity_var = story_data['model_instance']
    properties = bdd_data['properties']

    # Selecionar templates baseados no mapeamento
    backend_templates = template_mapping['backend'][tech_stack['backend']]
    frontend_templates = template_mapping['frontend'][tech_stack['frontend']]
    
    model_template = backend_templates['model']
    controller_template = backend_templates[action_name]
    backend_routes_template = backend_templates['routes']

    component_template = frontend_templates[action_name]
    frontend_routes_template = frontend_templates['routes']

    # Geração do back-end
    model_code = generate_model(model_template, entity_name, properties)
    controller_code = generate_controller(controller_template, entity_name, entity_var, properties, bdd_data)
    back_end_routes = generate_routes(backend_routes_template, entity_name)

    # Criar diretórios se não existirem
    os.makedirs('back_end/models', exist_ok=True)
    os.makedirs('back_end/controllers', exist_ok=True)
    os.makedirs('back_end/routes', exist_ok=True)

    # Escrever os arquivos gerados para o back-end
    with open(f'back_end/models/{entity_name.lower()}.py', 'w') as f:
        f.write(model_code)
    with open(f'back_end/controllers/{action_name}.py', 'w') as f:
        f.write(controller_code)
    with open(f'back_end/routes/{entity_name.lower()}.py', 'w') as f:
        f.write(back_end_routes)

    # Geração do front-end
    component_code = generate_component(component_template, entity_name, properties, bdd_data)
    service_code = generate_service(frontend_templates['service'], entity_name, properties)
    front_end_routes = generate_fe_routes(frontend_routes_template, entity_name)

    # Criar diretórios para o front-end se não existirem
    os.makedirs('front_end/src/components', exist_ok=True)
    os.makedirs('front_end/src/services', exist_ok=True)

    # Escrever os arquivos gerados para o front-end
    with open(f'front_end/src/components/List{entity_name}.js', 'w') as f:
        f.write(component_code)
    with open(f'front_end/src/services/{entity_name.lower()}.js', 'w') as f:
        f.write(service_code)
    with open(f'front_end/src/routes.js', 'w') as f:
        f.write(front_end_routes)

    print(f"Código gerado com sucesso para a entidade {entity_name}!")

if __name__ == "__main__":
    user_story = "Como um usuário, eu quero visualizar uma lista de produtos para que eu possa escolher um produto"
    bdd_scenario = """
    Scenario: Exibir lista de produtos
        Given que o produto tem um nome, preço e quantidade definidos
        When o usuário entra na pagina pela primeira vez
        Then a lista com os produtos deve ser exibida
        And a lista de produtos deve exibir no máximo 100 itens por página

    Scenario: Carregando a lista de produtos
        Given que estou carregando a lista de produtos
        When a lista ainda não foi carregada
        Then uma tela com um loading circular aparece
        And após a lista ser carregada o loading desaparece
    """
    
    tech_stack = {
        "backend": "flask",
        "frontend": "react"
    }

    orchestrate_generation(user_story, bdd_scenario, tech_stack)