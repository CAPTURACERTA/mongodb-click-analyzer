# MongoDB Click Analyzer

Projeto pequeno de aprendizado e portfólio criado para praticar MongoDB, Python, modelagem simples de dados, geração de dados fake, consultas analíticas e organização básica de um projeto com testes.

A aplicação simula um fluxo simples de e-commerce: cria usuários e produtos, gera eventos de clique e consulta quais produtos e dispositivos tiveram mais interações.

## Objetivos do projeto

- Praticar operações com MongoDB usando `pymongo`.
- Entender uma estrutura mínima de projeto Python separada por responsabilidades.
- Simular dados de usuários, produtos e cliques com `faker`.
- Criar consultas analíticas com aggregation pipelines.
- Escrever testes automatizados para serviços, geração de dados e consultas.

## Tecnologias

- Python 3.12+
- MongoDB local
- PyMongo
- Faker
- Pytest
- uv

## Estrutura

```text
.
├── main.py                 # Demonstra o fluxo completo do projeto
├── src/
│   ├── analytics.py        # Consultas analíticas sobre cliques
│   ├── click_service.py    # Geração e persistência de cliques
│   ├── config.py           # Configuração de conexão com MongoDB
│   ├── database.py         # Conexão, seed inicial e helpers de banco
│   ├── models.py           # Modelos e enums do domínio
│   └── seed.py             # Geração de usuários e produtos fake
└── tests/                  # Testes automatizados
```

## Como executar

Pré-requisitos:

- Python 3.12+
- MongoDB rodando localmente em `mongodb://localhost:27017/`
- `uv` instalado

Instale as dependências:

```bash
uv sync
```

Execute o projeto:

```bash
uv run python main.py
```

O script inicializa o banco `e-commerce`, cria dados de exemplo, gera cliques e imprime rankings de produtos e dispositivos mais clicados.

## Testes

Para rodar a suíte de testes:

```bash
uv run pytest
```

Os testes cobrem geração de dados, camada de banco, serviço de cliques e funções analíticas.

## Observações

Este projeto não tem como foco ser uma aplicação completa de produção. A proposta é servir como laboratório prático para consolidar fundamentos de MongoDB, engenharia de dados em pequena escala, testes e organização de código Python.
