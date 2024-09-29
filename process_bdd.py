import spacy

# Registrar a extensão 'tipo' se ainda não foi registrada
if not spacy.tokens.Span.has_extension("tipo"):
    spacy.tokens.Span.set_extension("tipo", default=None)

# Carregar o modelo treinado de BDD
nlp = spacy.load('trained_models/bdd_model')

# Verificar se o sentencizer está na pipeline e adicionar se não estiver
if 'sentencizer' not in nlp.pipe_names:
    nlp.add_pipe('sentencizer')

# Função para processar o cenário BDD usando o modelo treinado
def process_bdd(bdd_scenario):
    # Processa o cenário BDD com o modelo treinado
    doc = nlp(bdd_scenario)

    # Exibir todas as entidades detectadas pelo modelo
    print("Entidades detectadas:")
    for ent in doc.ents:
        print(f"Texto: {ent.text}, Label: {ent.label_}, Tipo: {ent._.get('tipo')}")

    conditions = []
    action = ""
    expected_result = ""
    properties = []
    actors = []
    locations = []
    outcomes = []
    model_names = []

    # Verifica cada sentença no documento
    for sent in doc.sents:
        # Detecta o "Given", "When" e "Then" no texto BDD
        if "Given" in sent.text or "Dado" in sent.text:
            conditions.append(sent.text.strip())
        elif "When" in sent.text or "Quando" in sent.text:
            action = sent.text.strip()
        elif "Then" in sent.text or "Então" in sent.text:
            expected_result = sent.text.strip()

        # Extração das entidades diretamente do modelo treinado
        for ent in doc.ents:
            if ent.label_ == "PROPERTY":
                # Acessar o tipo da propriedade através da extensão
                tipo = ent._.get("tipo") or "String"  # Valor padrão "String" caso o tipo não esteja definido
                properties.append({
                    'name': ent.text,
                    'type': tipo
                })
            elif ent.label_ == "ACTOR":
                actors.append(ent.text)
            elif ent.label_ == "ACTION":
                action = ent.text
            elif ent.label_ == "LOCATION":
                locations.append(ent.text)
            elif ent.label_ == "OUTCOME":
                outcomes.append(ent.text)
            elif ent.label_ == "MODEL_NAME":
                model_names.append(ent.text)

    return {
        "conditions": conditions,
        "action": action,
        "expected_result": expected_result,
        "properties": properties,
        "actors": actors,
        "locations": locations,
        "outcomes": outcomes,
        "model_names": model_names
    }

# Exemplo de uso da função com um cenário BDD
bdd_scenario = """
       Dado que o produto tem um nome, preço e quantidade definidos. 
       Quando o usuário entra na página pela primeira vez. 
       Então a lista com os produtos deve ser exibida.
    """
resultado = process_bdd(bdd_scenario)
print(resultado)
