import spacy
from spacy.training import Example
import random

# Carregar um modelo vazio
nlp = spacy.blank("pt")

# Criar o componente NER (Reconhecimento de Entidades Nomeadas)
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner", last=True)
else:
    ner = nlp.get_pipe("ner")

# Definir rótulos (labels) de entidades
ner.add_label("MODEL_NAME")
ner.add_label("PROPERTY")
ner.add_label("ACTOR")
ner.add_label("ACTION")
ner.add_label("LOCATION")
ner.add_label("RESULT")
ner.add_label("OUTCOME")

# Adicionar uma extensão personalizada 'tipo' para spans
spacy.tokens.Span.set_extension("tipo", default=None)

# Função para adicionar spans ao doc com tipo
def add_custom_span(doc, start, end, label, tipo=None):
    span = doc.char_span(start, end, label=label)
    if span:
        span._.tipo = tipo  # Definir o tipo como um atributo personalizado
        doc.ents = list(doc.ents) + [span]

# Função para verificar sobreposição de entidades
def entidades_validas(annotations):
    valid_annotations = []
    occupied_indices = set()
    
    for start, end, label, tipo in annotations:
        if not any(i in occupied_indices for i in range(start, end)):  # Verificar se há sobreposição
            valid_annotations.append((start, end, label, tipo))
            occupied_indices.update(range(start, end))  # Marcar esses índices como ocupados
    
    return valid_annotations

# Função para inferir o tipo de dado da propriedade
def infer_type(property_name):
    string_properties = ["nome", "descrição", "endereço", "alcunha", "apelido", "titulo"]
    integer_properties = ["quantidade", "idade", "id", "número"]
    float_properties = ["preço", "valor", "salário", "custo"]
    datetime_properties = ["data", "criado", "modificado"]

    if any(prop in property_name for prop in string_properties):
        return "String"
    elif any(prop in property_name for prop in integer_properties):
        return "Integer"
    elif any(prop in property_name for prop in float_properties):
        return "Float"
    elif any(prop in property_name for prop in datetime_properties):
        return "DateTime"
    else:
        return "String"  # Tipo padrão

# Listas de elementos variáveis para cenários BDD
modelos = ["produto", "categoria", "pedido", "fornecedor", "item"]
propriedades = ["nome", "preço", "quantidade", "descrição", "valor", "data"]
atores = ["usuário", "cliente", "administrador", "gerente"]
acoes = ["entra", "acessa", "visualiza"]
locais = ["pagina inicial", "carrinho", "catálogo", "dashboard"]
resultados = ["lista", "detalhes", "resumo"]
consequencias = ["deve ser exibida", "deve ser atualizada", "deve ser mostrada"]

# Função para gerar um cenário BDD com tipos de propriedades inferidos
def gerar_bdd_story_com_tipo():
    modelo = random.choice(modelos)
    props = random.sample(propriedades, 3)
    ator = random.choice(atores)
    acao = random.choice(acoes)
    local = random.choice(locais)
    resultado = random.choice(resultados)
    consequencia = random.choice(consequencias)
    
    # Frases BDD
    dado = f"Dado que o {modelo} tem um {props[0]}, {props[1]} e {props[2]} definidos"
    quando = f"Quando o {ator} {acao} na {local} pela primeira vez"
    entao = f"Então a {resultado} com os {modelo}s {consequencia}"
    
    # Inferir os tipos das propriedades
    tipo_prop_1 = infer_type(props[0])
    tipo_prop_2 = infer_type(props[1])
    tipo_prop_3 = infer_type(props[2])
    
    # Índices para as anotações
    start_model_name = dado.index(modelo)
    end_model_name = start_model_name + len(modelo)
    
    start_prop_1 = dado.index(props[0])
    end_prop_1 = start_prop_1 + len(props[0])
    
    start_prop_2 = dado.index(props[1])
    end_prop_2 = start_prop_2 + len(props[1])
    
    start_prop_3 = dado.index(props[2])
    end_prop_3 = start_prop_3 + len(props[2])
    
    start_actor = quando.index(ator)
    end_actor = start_actor + len(ator)
    
    start_action = quando.index(acao)
    end_action = start_action + len(acao)
    
    start_location = quando.index(local)
    end_location = start_location + len(local)
    
    start_result = entao.index(resultado)
    end_result = start_result + len(resultado)
    
    start_outcome = entao.index(consequencia)
    end_outcome = start_outcome + len(consequencia)
    
    # Anotações
    annotations = [
        (start_model_name, end_model_name, "MODEL_NAME", None),
        (start_prop_1, end_prop_1, "PROPERTY", tipo_prop_1),
        (start_prop_2, end_prop_2, "PROPERTY", tipo_prop_2),
        (start_prop_3, end_prop_3, "PROPERTY", tipo_prop_3),
        (start_actor, end_actor, "ACTOR", None),
        (start_action, end_action, "ACTION", None),
        (start_location, end_location, "LOCATION", None),
        (start_result, end_result, "RESULT", None),
        (start_outcome, end_outcome, "OUTCOME", None)
    ]
    
    # Remover sobreposições de entidades
    annotations = entidades_validas(annotations)
    
    return (dado, quando, entao, annotations)

# Gerar 100 variações de cenários BDD
dataset_bdd_com_tipo = [gerar_bdd_story_com_tipo() for _ in range(100)]

# Preparar os dados de treinamento no formato correto
TRAIN_DATA_BDD = []
for dado, quando, entao, annotations in dataset_bdd_com_tipo:
    texto_bdd = f"{dado}. {quando}. {entao}."
    doc = nlp.make_doc(texto_bdd)

    # Adicionar spans personalizados
    for start, end, label, tipo in annotations:
        add_custom_span(doc, start, end, label, tipo)
    
    example = Example.from_dict(doc, {"entities": [(span.start_char, span.end_char, span.label_) for span in doc.ents]})
    TRAIN_DATA_BDD.append(example)

# Treinamento
optimizer = nlp.begin_training()

# Treinar o modelo por 30 iterações
for i in range(30):
    random.shuffle(TRAIN_DATA_BDD)
    losses = {}
    for example in TRAIN_DATA_BDD:
        nlp.update([example], drop=0.5, losses=losses)
    print(f"Iteração {i + 1}, perdas: {losses}")

# Salvar o modelo treinado
nlp.to_disk("./trained_models/bdd_model")
