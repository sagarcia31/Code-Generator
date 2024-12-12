import spacy

# Carregar o modelo do spaCy
nlp = spacy.load('trained_models/user_story_model')

def process_user_story(user_story):
    doc = nlp(user_story)

    # Inicializar variáveis
    subject = ""
    action = ""
    entity = ""
    goal = ""
    method = ""

    # Detectar entidades e ações
    for ent in doc.ents:
        if ent.label_ == "SUBJECT":
            subject = ent.text
        elif ent.label_ == "ACTION":
            action = ent.text.lower().replace(" ", "_")
        elif ent.label_ == "ENTITY":
            entity = ent.text
        elif ent.label_ == "GOAL":
            goal = ent.text

        # Lógica para determinar o método de CRUD com base na ação
    if "adicionar" in action or "criar" in action or "inserir" in action:
        method = "create"
    elif "atualizar" in action or "editar" in action or "modificar" in action:
        method = "update"
    elif "remover" in action or "deletar" in action or "excluir" in action:
        method = "delete"
    elif "listar" in action or "visualizar" in action or "consultar" in action:
        method = "get_all"

    # Se a entidade do modelo não foi identificada corretamente, defina um padrão
    if not entity:
        entity = "Produto"  # Entidade padrão

    return {
        "subject": subject,
        "action": action,
        "entity": entity,
        "goal": goal,
        "method": method
    }

# Exemplo de uso da função com uma user story
user_story = "Como um usuário, eu quero adicionar um produto ao carrinho, para efetuar uma compra"
resultado = process_user_story(user_story)
print(resultado)