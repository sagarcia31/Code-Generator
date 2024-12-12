import spacy
from spacy.training import Example
import random

# Carregar um modelo vazio
nlp = spacy.blank("pt")

# Criar o componente NER
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner", last=True)
else:
    ner = nlp.get_pipe("ner")

# Definir rótulos (labels) de entidades
ner.add_label("SUBJECT")
ner.add_label("ACTION")
ner.add_label("ENTITY")
ner.add_label("GOAL")
ner.add_label("METHOD")

# Dados de treino
TRAIN_DATA = [
    ("Como um usuário, eu quero adicionar um produto ao carrinho, para efetuar uma compra", {
        "entities": [(8, 14, "SUBJECT"), (20, 28, "ACTION"), (33, 40, "ENTITY"), (50, 67, "GOAL")]
    }),
    ("Como um administrador, eu quero atualizar as informações do pedido, para manter o sistema atualizado", {
        "entities": [(8, 21, "SUBJECT"), (25, 34, "ACTION"), (39, 50, "ENTITY"), (56, 78, "GOAL")]
    }),
    ("Como um administrador, eu quero remover um produto do estoque, para manter o estoque atualizado.", {
        "entities": [(8, 21, "SUBJECT"), (25, 31, "ACTION"), (33, 40, "ENTITY"), (46, 73, "GOAL")]
    }),
    ("Como um usuário, eu quero visualizar os pedidos feitos, para monitoramento posterior.", {
        "entities": [(8, 15, "SUBJECT"), (26, 36, "ACTION"), (40, 47, "ENTITY"), (61, 84, "GOAL")]
    })
]

# Preparar o treinamento
optimizer = nlp.begin_training()

# Treinamento
for i in range(300):  # Treinar por 30 iterações
    random.shuffle(TRAIN_DATA)
    losses = {}
    for text, annotations in TRAIN_DATA:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        nlp.update([example], drop=0.5, losses=losses)
    print(f"Iteração {i + 1}, perdas: {losses}")

# Salvar o modelo treinado
nlp.to_disk("./trained_models/user_story_model")