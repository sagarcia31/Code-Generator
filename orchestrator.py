import os
from back_end.generator import generate_model, generate_controller, generate_routes
from front_end.generator import generate_component, generate_service, generate_routes as generate_fe_routes
from process_story import process_user_story
from process_bdd import process_bdd

def orchestrate_generation(user_story, bdd_scenario):
    # Processa a história de usuário
    story_data = process_user_story(user_story)
    
    # Processa o cenário BDD
    bdd_data = process_bdd(bdd_scenario)

    # Extração das informações processadas
    entity_name = story_data['model_name']
    action_name = story_data['action_name']
    entity_var = story_data['model_instance']
    properties = bdd_data['properties']

    # Geração do back-end
    model_code = generate_model(entity_name, properties)
    controller_code = generate_controller(action_name, entity_name, entity_var, properties, bdd_data)
    back_end_routes = generate_routes(entity_name)

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
    component_code = generate_component(entity_name)
    service_code = generate_service(entity_name)
    front_end_routes = generate_fe_routes(entity_name)

    # Criar diretórios para o front-end se não existirem
    os.makedirs('front_end/src/components', exist_ok=True)
    os.makedirs('front_end/src/services', exist_ok=True)

    # Escrever os arquivos gerados para o front-end
    with open(f'front_end/src/components/Add{entity_name}.js', 'w') as f:
        f.write(component_code)
    with open(f'front_end/src/services/{entity_name.lower()}.js', 'w') as f:
        f.write(service_code)
    with open(f'front_end/src/routes.js', 'w') as f:
        f.write(front_end_routes)

    print(f"Código gerado com sucesso para a entidade {entity_name}!")

if __name__ == "__main__":
    user_story = "Como um usuário, eu quero adicionar um produto para que eu possa gerenciar meu inventário."
    bdd_scenario = """
        Given que o produto tem um nome, preço e quantidade definidos
        When o usuário adiciona o produto ao inventário
        Then o produto deve ser salvo no sistema
        And o sistema deve exibir uma mensagem de sucesso
    """
    
    orchestrate_generation(user_story, bdd_scenario)