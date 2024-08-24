import requests

def extract_design_from_figma(figma_file_key, figma_access_token):
    url = f'https://api.figma.com/v1/files/{figma_file_key}'
    headers = {
        'X-Figma-Token': figma_access_token
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # Aqui você pode processar os componentes extraídos conforme necessário
        return data
    else:
        raise Exception(f'Failed to fetch Figma design: {response.status_code}')

def map_figma_to_component(figma_data):
    components = figma_data['document']['children']
    mapped_components = {}
    for component in components:
        if component['type'] == 'COMPONENT':
            component_name = component['name']
            # Exemplo simples: cria uma tag HTML básica para o componente
            mapped_components[component_name] = f"<div>{component['name']}</div>"
    return mapped_components