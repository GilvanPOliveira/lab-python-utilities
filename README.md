# Lab Python Utilities

Aplicação full stack com ferramentas úteis do dia a dia desenvolvidas com Python.

## 

## Sobre

O **Lab Python Utilities** é um laboratório técnico focado na criação de ferramentas práticas utilizando Python no backend e uma interface moderna no frontend.

## 

## Funcionalidades Planejadas

- Gerar QR Code
- Encurtar links
- Remover fundo de imagem
- Converter imagens
- Redimensionar imagens
- Gerar senhas
- Formatar JSON
- Validar CPF e CNPJ
- Gerar slug
- Converter textos
- Limpar textos
- Extrair metadados de arquivos
- Gerar hash
- Manipular datas
- Gerar arquivos simples
- Download de vídeos próprios ou autorizados
- Conversão de vídeos próprios ou autorizados para MP3

##

## Estrutura do Projeto
```
lab-python-utilities/
│
├── frontend/       # aplicação web
├── backend/        # API em Python com FastAPI
├── docs/           # documentação técnica do projeto
├── README.md
├── .gitignore
└── vercel.json
```

##

## Documentação

A documentação técnica do projeto está organizada na pasta `docs`.

- [`scope.md`](./docs/scope.md) — escopo do projeto
- [`architecture.md`](./docs/architecture.md) — arquitetura da aplicação
- [`modules.md`](./docs/modules.md) — módulos e ferramentas planejadas
- [`decisions.md`](./docs/decisions.md) — decisões técnicas
- [`roadmap.md`](./docs/roadmap.md) — plano de evolução

##

## Como Executar

### Backend
```
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.index:app --reload
```

A API ficará disponível em:
```
http://localhost:8000
```

### Frontend
```
cd frontend
npm install
npm run dev
```

A aplicação ficará disponível em:
```
http://localhost:5173
```

##

## Stack

[![My Skills](https://skillicons.dev/icons?i=python,fastapi,vue,ts,tailwind,pinia&perline=5)](https://skillicons.dev)


### Frontend

- Vue 3
- TypeScript
- Vite
- Tailwind CSS v3
- Vue Router
- Pinia
- Axios

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn
- Pillow
- qrcode
- python-multipart

##

## Contato

* Portfólio: https://gilvanpoliveira.github.io
* Email: [gilvanoliveira06@gmail.com](mailto:gilvanoliveira06@gmail.com)
