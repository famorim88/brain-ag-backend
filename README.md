# BRAIN AG - Backend

Este repositório contém o backend da aplicação BRAIN AG, desenvolvido para gerenciar o cadastro de produtores rurais e suas fazendas, incluindo informações sobre área, uso do solo e culturas plantadas. A API oferece funcionalidades CRUD (Create, Read, Update, Delete) para produtores e dados agregados para visualização em dashboards.

## Tecnologias Utilizadas

* **Python**: Linguagem de programação principal.
* **FastAPI**: Framework web moderno e de alta performance para construção de APIs.
* **SQLAlchemy**: ORM (Object-Relational Mapper) para interação com o banco de dados.
* **Alembic**: Ferramenta de migração de banco de dados para gerenciar alterações no esquema.
* **PostgreSQL**: Sistema de gerenciamento de banco de dados relacional.
* **Pydantic**: Biblioteca para validação de dados e configurações, integrada ao FastAPI.
* **Psycopg2**: Adaptador PostgreSQL para Python.
* **Docker / Docker Compose**: Para orquestração e conteinerização do ambiente de desenvolvimento (aplicação e banco de dados).
* **Pytest**: Framework de testes para garantir a robustez e correção do código.
* **python-dotenv**: Para carregar variáveis de ambiente de um arquivo `.env`.

## Estrutura do Projeto

BRAIN-AG-BACKEND/
├── alembic/                # Scripts de migração de banco de dados do Alembic
│   ├── versions/           # Versões das migrações
│   └── env.py              # Ambiente de execução do Alembic
├── app/
│   ├── api/                # Endpoints da API (FastAPI Routers)
│   │   ├── dashboard.py    # Endpoint para dados do dashboard
│   │   └── producer.py     # Endpoints CRUD para produtores
│   ├── core/               # Configurações globais e utilitários
│   │   ├── config.py       # Configurações do ambiente
│   │   └── utils.py        # Funções utilitárias
│   ├── database/           # Configuração de banco de dados
│   │   ├── base.py         # Base declarativa do SQLAlchemy
│   │   └── session.py      # Configuração de sessão do banco de dados
│   ├── models/             # Modelos de dados do SQLAlchemy
│   │   ├── producer.py     # Modelo para Produtor e Cultura
│   ├── crud/               # Funções de operações de banco de dados (Create, Read, Update, Delete)
│   │   └── producer.py     # Lógica CRUD para produtores
│   ├── schemas/            # Schemas de validação e serialização de dados (Pydantic)
│   │   └── producer.py     # Schemas para Produtor, Cultura e Dashboard
│   └── main.py             # Ponto de entrada principal da aplicação FastAPI
├── tests/                  # Testes unitários e de integração
│   ├── conftest.py         # Fixtures e configurações de teste
│   ├── test_dashboard.py   # Testes para o dashboard
│   └── test_producer.py    # Testes para produtores
├── .env                    # Variáveis de ambiente (não deve ser versionado em produção)
├── .gitignore              # Regras para ignorar arquivos no Git
├── docker-compose.yml      # Definição dos serviços Docker
├── Dockerfile              # Definição da imagem Docker da aplicação
├── requirements.txt        # Dependências Python do projeto
└── README.md               # Este arquivo


## Funcionalidades Principais

* **Cadastro e Gestão de Produtores Rurais**: Permite registrar novos produtores com informações detalhadas da fazenda (nome, CPF/CNPJ, cidade, estado, área total, área agricultável, área de vegetação).
* **Gestão de Culturas**: Associar e gerenciar culturas plantadas a cada fazenda (ex: soja, milho, algodão, cana de açúcar) por ano de safra.
* **Validações de Negócio**:
    * Validação de CPF/CNPJ.
    * Verificação de que a soma da área agricultável e de vegetação não excede a área total da fazenda.
* **Dashboard de Análise**:
    * Contagem total de fazendas.
    * Soma da área total de hectares das fazendas.
    * Distribuição de fazendas por estado.
    * Distribuição de culturas plantadas.
    * Distribuição de área por uso do solo (agricultável vs. vegetação).