import spacy

# Carregar o modelo do spaCy
nlp = spacy.load('en_core_web_sm')

def infer_type(attribute):
    # Lógica mais complexa para inferir tipos, incluindo contexto
    if attribute.lower() in ['name', 'description', 'email', 'address']:
        return 'String(255)'
    elif attribute.lower() in ['quantity', 'age', 'id']:
        return 'Integer'
    elif attribute.lower() in ['price', 'salary', 'cost', 'value']:
        return 'Float'
    elif attribute.lower() in ['date', 'created', 'modified', 'birthday']:
        return 'DateTime'
    else:
        return 'String(255)'

def extract_properties(text):
    doc = nlp(text)
    properties = {}
    
    for ent in doc.ents:
        if ent.label_ in ['ORG', 'PRODUCT', 'PERSON', 'GPE']:  # Ajuste para tipos relevantes
            prop_type = infer_type(ent.text)
            properties[ent.text.lower()] = prop_type

    return properties