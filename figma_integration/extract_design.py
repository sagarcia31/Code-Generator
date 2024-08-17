import requests

def extract_design_from_figma(figma_file_key, figma_access_token):
    url = f"https://api.figma.com/v1/files/{figma_file_key}"

    headers = {
        "X-Figma-Token": figma_access_token
    }

    try:
        response = requests.get(url, headers=headers)
        
        # Verificar o código de status HTTP
        if response.status_code != 200:
            print(f"Erro na requisição à API do Figma: {response.status_code}")
            print("Mensagem de erro:", response.text)
            return []  # Retorna uma lista vazia ou lida com o erro de outra forma
        
        data = response.json()

        # Verificar se a chave 'document' está presente no JSON retornado
        if 'document' not in data:
            print("A resposta da API não contém a chave 'document'.")
            return []

        # Processar dados do Figma para extrair nomes de campos, etc.
        components = []
        for component in data['document']['children']:
            components.append({
                'name': component['name'],
                'type': component['type'],
                'properties': component.get('properties', {})
            })

        return components

    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ou na requisição à API do Figma: {e}")
        return []
    except ValueError:
        print("Erro ao tentar decodificar a resposta JSON.")
        return []
    except KeyError as e:
        print(f"Chave não encontrada: {e}")
        return []
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return []