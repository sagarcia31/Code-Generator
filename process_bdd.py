import spacy

nlp = spacy.load('pt_core_news_sm')

def infer_type(attribute):
    # Inferir o tipo de dado baseado no nome do atributo
    if 'nome' in attribute.lower() or 'descrição' in attribute.lower() or 'endereço' in attribute.lower():
        return 'String(255)'
    elif 'quantidade' in attribute.lower() or 'idade' in attribute.lower() or 'id' in attribute.lower():
        return 'Integer'
    elif 'preço' in attribute.lower() or 'salário' in attribute.lower() or 'valor' in attribute.lower():
        return 'Float'
    elif 'data' in attribute.lower() or 'criado' in attribute.lower() or 'modificado' in attribute.lower():
        return 'DateTime'
    else:
        return 'String(255)'  # Tipo padrão

def extract_properties_from_bdd(bdd_scenario):
    doc = nlp(bdd_scenario)
    
    properties = {}

    for sent in doc.sents:
        # Verificar se a sentença define propriedades, por exemplo, "Given que o produto tem um nome, preço e quantidade definidos"
        if "Given" in sent.text or "Dado" in sent.text:
            # Extrair possíveis propriedades e seus tipos
            for token in sent:
                if token.text.lower() in ['nome', 'preço', 'quantidade']:
                    prop_name = token.text.lower()
                    prop_type = infer_type(prop_name)
                    properties[prop_name] = prop_type

    return properties

def process_bdd(bdd_scenario):
    doc = nlp(bdd_scenario)

    conditions = []
    action = ""
    expected_result = ""

    for sent in doc.sents:
        if "Given" in sent.text or "Dado" in sent.text:
            conditions.append(sent.text.strip())
        elif "When" in sent.text or "Quando" in sent.text:
            action = sent.text.strip()
        elif "Then" in sent.text or "Então" in sent.text:
            expected_result = sent.text.strip()

    # Extração das propriedades
    properties = extract_properties_from_bdd(bdd_scenario)

    return {
        "conditions": conditions,
        "action": action,
        "expected_result": expected_result,
        "properties": properties
    }