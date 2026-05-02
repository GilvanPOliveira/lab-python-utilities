# Decisões Técnicas

## 1. Nome do Projeto

O nome oficial do repositório será:

lab-python-utilities

Esse nome mantém o padrão dos laboratórios técnicos e deixa claro que o foco é criar utilitários com Python.

## 2. Tipo de Projeto

O projeto será uma aplicação full stack.

Ele terá:

- frontend moderno separado
- backend em Python
- documentação técnica
- deploy na Vercel

## 3. Frontend Separado

Foi decidido utilizar frontend separado para manter o projeto mais próximo de uma aplicação real.

Essa decisão facilita:

- organização visual
- evolução da interface
- separação de responsabilidades
- consumo claro da API
- manutenção independente do backend

## 4. Stack do Frontend

A stack oficial do frontend será:

- Vue 3
- TypeScript
- Vite
- Tailwind CSS v3
- Vue Router
- Pinia
- Axios

Essa stack mantém o padrão dos projetos anteriores e permite criar uma interface moderna, responsiva e de fácil manutenção.

## 5. Backend com Python

Foi decidido utilizar Python no backend para que o projeto cumpra seu objetivo principal: demonstrar utilitários práticos criados com Python.

A stack oficial do backend será:

- Python
- FastAPI
- Pydantic
- Uvicorn
- Pillow
- qrcode
- python-multipart
- python-slugify
- python-dateutil

## 6. Uso do FastAPI

FastAPI foi escolhido por ser simples, moderno e adequado para criação de APIs.

Ele permite:

- validação com Pydantic
- documentação automática
- boa organização de rotas
- integração simples com frontend
- produtividade no desenvolvimento

## 7. Arquitetura Modular

O backend será organizado por módulos.

Cada grupo de ferramentas terá sua própria pasta dentro de:

backend/src/modules/

Exemplo:

backend/src/modules/qrcode_tools/
backend/src/modules/password_tools/
backend/src/modules/json_tools/

Cada módulo terá:

- router.py
- schemas.py
- service.py

## 8. Sem Banco de Dados no MVP

O MVP não utilizará banco de dados.

Essa decisão mantém o projeto simples e focado em funções úteis.

Banco de dados poderá ser adicionado futuramente para funcionalidades como:

- encurtador de links persistente
- histórico de uso
- autenticação
- favoritos
- painel do usuário

## 9. Sem Autenticação no MVP

O MVP não terá autenticação.

As ferramentas serão públicas e acessíveis diretamente.

Autenticação poderá ser adicionada em uma fase futura caso o projeto evolua para salvar histórico, favoritos ou dados de usuário.

## 10. Deploy na Vercel

O deploy inicial será feito na Vercel.

Essa decisão foi tomada para manter o fluxo simples e alinhado aos demais projetos publicados.

O projeto deve ser construído considerando limitações de ambiente serverless.

## 11. Backend Stateless

O backend não deve depender de armazenamento local permanente.

Arquivos gerados devem ser:

- retornados diretamente na resposta
- processados em memória
- tratados como temporários

Essa decisão facilita deploy e evita problemas em ambiente serverless.

## 12. Processamento de Imagens

Ferramentas de imagem entrarão de forma progressiva.

No MVP, o foco será em operações leves:

- conversão de imagem
- redimensionamento
- extração básica de metadados

Remoção de fundo poderá ser adicionada depois, pois pode exigir processamento mais pesado.

## 13. Processamento de Mídia

Funcionalidades relacionadas a download de vídeos, conversão para MP3 e Reels serão tratadas como recursos futuros.

Essas funcionalidades devem respeitar direitos autorais e termos de uso das plataformas.

O projeto deve deixar claro que essas ferramentas são voltadas para conteúdos próprios, autorizados ou livres de direitos.

## 14. Encurtador de Links

No MVP, o projeto pode gerar códigos curtos ou validar URLs.

Um encurtador real com redirecionamento e persistência será implementado apenas quando houver banco de dados.

## 15. Documentação

A documentação técnica ficará concentrada na pasta:

docs/

Arquivos principais:

- scope.md
- architecture.md
- modules.md
- decisions.md
- roadmap.md

O README será mantido mais curto, servindo como apresentação principal do repositório.

## 16. Código Limpo

O projeto deve priorizar:

- nomes claros
- funções pequenas
- baixa complexidade
- separação de responsabilidades
- módulos fáceis de entender
- respostas padronizadas da API

## 17. Evolução Progressiva

O projeto será construído em fases.

A prioridade inicial é entregar uma base funcional e simples.

Novas ferramentas devem ser adicionadas somente depois que a estrutura principal estiver estável.

## 18. Decisão Final

O Lab Python Utilities será um laboratório técnico simples, modular e escalável, com foco em ferramentas úteis feitas com Python e uma interface moderna para consumo dessas funcionalidades.
