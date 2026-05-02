# Arquitetura

## Visão Geral

O Lab Python Utilities é uma aplicação full stack organizada em duas partes principais:

- `frontend`: interface web moderna desenvolvida com Vue 3, TypeScript e Tailwind CSS
- `backend`: API desenvolvida com Python e FastAPI

A arquitetura foi pensada para ser simples, prática e fácil de evoluir, evitando excesso de abstrações no início do projeto.

## Objetivo da Arquitetura

A estrutura do projeto deve permitir:

- separar frontend e backend
- manter o backend modular
- facilitar a criação de novas ferramentas
- evitar arquivos grandes e difíceis de manter
- centralizar regras de processamento no backend
- manter o frontend focado em experiência e consumo da API
- permitir deploy na Vercel

## Estrutura Geral

lab-python-utilities/
│
├── frontend/
├── backend/
├── docs/
├── README.md
├── .gitignore
└── vercel.json

## Frontend

O frontend será responsável por:

- exibir as páginas das ferramentas
- coletar dados do usuário
- validar dados básicos de formulário
- enviar requisições para o backend
- exibir resultados
- mostrar estados de loading, erro e sucesso

O frontend não deve concentrar regras pesadas de processamento.

## Estrutura do Frontend

frontend/
│
├── src/
│   ├── app/
│   │   └── router/
│   │
│   ├── assets/
│   │   └── main.css
│   │
│   ├── components/
│   │   ├── layout/
│   │   ├── ui/
│   │   └── tools/
│   │
│   ├── features/
│   │   ├── qrcode/
│   │   ├── passwords/
│   │   ├── json/
│   │   ├── documents/
│   │   ├── slug/
│   │   ├── text/
│   │   ├── hash/
│   │   ├── dates/
│   │   ├── images/
│   │   ├── links/
│   │   └── media/
│   │
│   ├── services/
│   │   └── api.ts
│   │
│   ├── views/
│   ├── types/
│   ├── utils/
│   ├── App.vue
│   └── main.ts
│
├── public/
├── index.html
├── package.json
├── tailwind.config.js
├── postcss.config.js
└── vite.config.ts

## Backend

O backend será responsável por:

- receber requisições da interface
- validar entradas com Pydantic
- executar as funções Python
- manipular textos, dados, arquivos e imagens
- retornar respostas padronizadas
- manter cada ferramenta isolada em seu próprio módulo

## Estrutura do Backend

backend/
│
├── src/
│   ├── index.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── constants.py
│   │   └── exceptions.py
│   │
│   ├── modules/
│   │   ├── qrcode_tools/
│   │   ├── password_tools/
│   │   ├── json_tools/
│   │   ├── document_tools/
│   │   ├── slug_tools/
│   │   ├── text_tools/
│   │   ├── hash_tools/
│   │   ├── date_tools/
│   │   ├── image_tools/
│   │   ├── link_tools/
│   │   └── media_tools/
│   │
│   └── shared/
│       ├── file_helpers.py
│       ├── string_helpers.py
│       ├── response_helpers.py
│       └── validators.py
│
├── requirements.txt
└── pyproject.toml

## Padrão dos Módulos

Cada módulo do backend deve seguir a estrutura:

module_name/
├── router.py
├── schemas.py
└── service.py

## Responsabilidades

### router.py

Responsável por:

- declarar rotas da API
- receber payloads
- chamar o service correspondente
- retornar resposta HTTP

### schemas.py

Responsável por:

- definir schemas Pydantic
- validar dados de entrada
- padronizar dados de saída

### service.py

Responsável por:

- concentrar a regra principal da ferramenta
- executar processamento em Python
- retornar dados prontos para a rota

## Comunicação entre Frontend e Backend

O frontend consumirá o backend através de um serviço central:

frontend/src/services/api.ts

Esse arquivo deve concentrar a configuração do Axios, incluindo:

- base URL da API
- headers padrão
- tratamento básico de erro

## Rotas Base da API

GET /api/health

POST /api/qrcode/generate
POST /api/passwords/generate
POST /api/json/format
POST /api/json/validate
POST /api/documents/validate-cpf
POST /api/documents/validate-cnpj
POST /api/slug/generate
POST /api/text/clean
POST /api/text/convert
POST /api/hash/generate
POST /api/dates/format
POST /api/images/convert
POST /api/images/resize

## Princípios Técnicos

## Simplicidade

O projeto deve evitar overengineering.

A estrutura precisa ser clara, mas sem camadas desnecessárias.

## Modularidade

Cada ferramenta deve ficar isolada em seu próprio módulo.

Isso facilita manutenção e evolução.

## Baixo Acoplamento

O frontend não deve depender da implementação interna do backend.

O backend deve expor apenas contratos claros via API.

## Código Limpo

O código deve priorizar:

- nomes claros
- funções pequenas
- responsabilidades bem definidas
- validações explícitas
- respostas previsíveis

## Escalabilidade Progressiva

O projeto começa simples, mas pode evoluir para:

- banco de dados
- autenticação
- histórico de uso
- favoritos
- encurtador de links persistente
- processamento assíncrono
- uso de serviços externos para tarefas pesadas

## Deploy

O deploy inicial será feito na Vercel.

A aplicação deve ser pensada para rodar de forma stateless, sem depender de arquivos locais permanentes.

Arquivos gerados devem ser retornados diretamente na resposta ou tratados como dados temporários.

## Decisão Final

A arquitetura oficial do projeto será:

- frontend separado
- backend modular
- API simples com FastAPI
- frontend moderno com Vue 3
- documentação enxuta
- evolução por fases
