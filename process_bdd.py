import spacy

# Carregar o modelo treinado de BDD
nlp = spacy.load('./bdd_model')  # Carregar o modelo treinado para BDD

# Adicionar o sentencizer à pipeline, caso ele não esteja presente
if 'sentencizer' not in nlp.pipe_names:
    nlp.add_pipe('sentencizer')

# Função para processar o cenário BDD usando o modelo treinado
def process_bdd(bdd_scenario):
    # Processa o cenário BDD com o modelo treinado
    doc = nlp(bdd_scenario)

    conditions = []
    action = ""
    expected_result = ""
    properties = []
    actors = []
    locations = []
    outcomes = []
    model_names = []

    for sent in doc.sents:
        # Detecta o "Given", "When" e "Then" no texto BDD
        if "Given" in sent.text or "Dado" in sent.text:
            conditions.append(sent.text.strip())
        elif "When" in sent.text or "Quando" in sent.text:
            action = sent.text.strip()
        elif "Then" in sent.text or "Então" in sent.text:
            expected_result = sent.text.strip()

        # Extração das entidades diretamente do modelo treinado
        for ent in sent.ents:
            if ent.label_ == "PROPERTY":
                properties.append({
                    'name': ent.text.lower(),
                    'type': ent.label_  # O modelo já fornece o tipo
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