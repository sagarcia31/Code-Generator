import spacy
from spacy.training import Example
import random

# Carregar um modelo pré-treinado (como ponto de partida)
nlp = spacy.blank("pt")  

# Criar o componente NER
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner", last=True)
else:
    ner = nlp.get_pipe("ner")

ner.add_label("MODEL_NAME")
ner.add_label("ACTION_NAME")
ner.add_label("METHOD")

# Dados de treino (incluindo método HTTP no texto)
TRAIN_DATA = [
    ("Como um usuário, eu quero adicionar um produto ao carrinho. POST", {
        "entities": [(33, 40, "MODEL_NAME"), (20, 28, "ACTION_NAME"), (49, 53, "METHOD")]
    }),
    ("Como um administrador, eu quero atualizar as informações do pedido. PUT", {
        "entities": [(44, 50, "MODEL_NAME"), (25, 34, "ACTION_NAME"), (60, 63, "METHOD")]
    }),
    ("Como um administrador, eu quero remover um produto do estoque. DELETE", {
        "entities": [(38, 45, "MODEL_NAME"), (25, 31, "ACTION_NAME"), (56, 62, "METHOD")]
    }),
    ("Como um usuário, eu quero visualizar os pedidos feitos. GET", {
        "entities": [(37, 44, "MODEL_NAME"), (25, 35, "ACTION_NAME"), (52, 55, "METHOD")]
    })
]

# Preparar o treinamento
optimizer = nlp.begin_training()

# Treinamento
for i in range(30):  # Treinar por 30 iterações
    random.shuffle(TRAIN_DATA)
    losses = {}
    for text, annotations in TRAIN_DATA:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        nlp.update([example], drop=0.5, losses=losses)
    print(f"Iteração {i + 1}, perdas: {losses}")

# Salvar o modelo treinado
nlp.to_disk("./user_story_model")