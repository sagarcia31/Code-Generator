# 🚀 Dynamic Code Generator

🎉 Dynamic Code Generator é um projeto que automatiza a criação de código back-end e front-end a partir de templates, utilizando user stories e BDD. Este gerador facilita a construção de APIs e interfaces modernas, poupando tempo e esforço no desenvolvimento de projetos.

## 📝 Funcionalidades

• 🛠 Geração Automática de Código: Crie modelos, controladores, rotas, componentes e serviços de forma automatizada.
• 🔄 Suporte para BDD: Integre cenários BDD para garantir que seu código siga práticas de desenvolvimento orientado a comportamento.
• 💻 Geração de Front-End: Crie componentes React, serviços e rotas automaticamente a partir de templates.
• ⚙️ Geração de Back-End: Geração de modelos, controladores e rotas para APIs Flask com suporte a SQLAlchemy.
• 🎨 Integração com Figma (opcional): Extraia design do Figma e integre diretamente na geração de código.

  ## 📁 Estrutura do Projeto

    auto_generator/
    ├── back_end/
    │   ├── templates/
    │   │   ├── model.py.hbs
    │   │   ├── controller.py.hbs
    │   │   └── routes.py.hbs
    │   └── generator.py
    ├── front_end/
    │   ├── templates/
    │   │   ├── component.js.hbs
    │   │   ├── service.js.hbs
    │   │   └── routes.js.hbs
    │   └── generator.py
    ├── figma_integration/
    │   └── extract_design.py
    └── orchestrator.py

  ## 🚀 Como Usar

    `git clone https://github.com/seu-usuario/dynamic-code-generator.git
    `cd dynamic-code-generator

  ## Exemplo de uso

```python
user_story = "Como um usuário, eu quero adicionar um produto para que eu possa gerenciar meu inventário."
bdd_scenario = """
Feature: Gerenciamento de Produtos

Scenario: Adicionar um novo produto ao inventário
    Given que o produto tem um nome, preço e quantidade definidos
    When o usuário adiciona o produto ao inventário
    Then o produto deve ser salvo no sistema
    And o sistema deve exibir uma mensagem de sucesso
"""

orchestrate_generation(user_story, bdd_scenario)
```

    
