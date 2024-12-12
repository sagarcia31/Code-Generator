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

# Componentes para gerar user stories
subjects = ["usuário", "administrador", "cliente", "gerente", "visitante", "membro", "funcionário", "analista", "supervisor", "desenvolvedor"]
actions = ["adicionar", "criar", "inserir", "atualizar", "editar", "modificar",
           "remover", "deletar", "excluir", "listar", "visualizar", "consultar", "gerar", "administrar", "automatizar"]
entities = ["produto", "pedido", "item", "estoque", "informações do pedido",
            "detalhes do produto", "usuário", "perfil", "relatório", "categoria",
            "registro", "dados", "documento", "fatura", "transação"]
goals = ["efetuar uma compra", "manter o sistema atualizado", "monitorar o estoque",
         "decidir a compra", "gerar relatórios", "melhorar a experiência do usuário",
         "facilitar a gestão de dados", "aumentar as vendas", "otimizar processos",
         "garantir a segurança dos dados", "automatizar tarefas", "reduzir custos",
         "melhorar a eficiência", "aumentar a produtividade", "satisfazer o cliente"]

def gerar_train_data(num_examples=1000):
    train_data = []
    for _ in range(num_examples):
        subject = random.choice(subjects)
        action = random.choice(actions)
        entity = random.choice(entities)
        goal = random.choice(goals)

        user_story = f"Como um {subject}, eu quero {action} um {entity}, para {goal}."

        # Identificar os índices das entidades no texto
        start_subject = user_story.find(subject)
        end_subject = start_subject + len(subject)

        start_action = user_story.find(action)
        end_action = start_action + len(action)

        start_entity = user_story.find(entity, end_action)
        end_entity = start_entity + len(entity)

        start_goal = user_story.find(goal, end_entity)
        end_goal = start_goal + len(goal)

        entities_anotadas = [
            (start_subject, end_subject, "SUBJECT"),
            (start_action, end_action, "ACTION"),
            (start_entity, end_entity, "ENTITY"),
            (start_goal, end_goal, "GOAL")
        ]

        train_data.append((user_story, {"entities": entities_anotadas}))
    return train_data

# Gerar 1000 exemplos
TRAIN_DATA = gerar_train_data(1000)

# Preparar o treinamento
optimizer = nlp.begin_training()

# Treinamento
for i in range(300):  # Ajuste o número de iterações conforme necessário
    random.shuffle(TRAIN_DATA)
    losses = {}
    for texto, anotacoes in TRAIN_DATA:
        doc = nlp.make_doc(texto)
        exemplo = Example.from_dict(doc, anotacoes)
        nlp.update([exemplo], drop=0.5, losses=losses)
    print(f"Iteração {i + 1}, perdas: {losses}")

# Salvar o modelo treinado
nlp.to_disk("./trained_models/user_story_model")