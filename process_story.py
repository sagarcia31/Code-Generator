import spacy

# Carregar o modelo do spaCy
nlp = spacy.load('pt_core_news_sm')

def process_user_story(user_story):
    doc = nlp(user_story)

    # Inicializar variáveis
    model_name = ""
    action_name = ""
    method = ""

    # Detectar entidades e ações
    for ent in doc.ents:
        if ent.label_ == "ORG":  # Supondo que o modelo seja identificado como uma organização
            model_name = ent.text.capitalize()
        elif ent.label_ == "MISC":  # Supondo que ações sejam rotuladas como MISC
            action_name = ent.text.lower().replace(" ", "_")

    # Lógica simples para determinar o método de CRUD
    if "adicionar" in user_story.lower() or "criar" in user_story.lower():
        method = "create"
    elif "atualizar" in user_story.lower() or "editar" in user_story.lower():
        method = "update"
    elif "remover" in user_story.lower() or "deletar" in user_story.lower():
        method = "delete"
    elif "listar" in user_story.lower():
        method = "list"

    # Se a entidade do modelo não foi identificada corretamente, defina um padrão
    if not model_name:
        model_name = "Produto"  # Modelo padrão

    if not action_name:
        action_name = f"{method}_{model_name.lower()}"  # Nome da ação padrão

    return {
        "model_name": model_name,
        "action_name": action_name,
        "method": method,
        "model_instance": model_name.lower()
    }