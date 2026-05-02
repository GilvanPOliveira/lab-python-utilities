# Roadmap

## Visão Geral

O roadmap do Lab Python Utilities será dividido em fases.

A ideia é construir o projeto de forma progressiva, começando por uma base simples e funcional, depois adicionando novas ferramentas conforme a estrutura estiver estável.

## Fase 1 — Base do Projeto

## Objetivo

Criar a estrutura inicial do projeto com frontend, backend e documentação.

## Entregas

- Criar estrutura do monorepo
- Criar pasta frontend
- Criar pasta backend
- Criar pasta docs
- Configurar README
- Configurar .gitignore
- Configurar frontend com Vue 3, TypeScript e Vite
- Configurar Tailwind CSS v3
- Configurar Vue Router
- Configurar Pinia
- Configurar Axios
- Configurar backend com FastAPI
- Criar endpoint de health check
- Validar comunicação entre frontend e backend

## Status

Pendente.

## Fase 2 — Primeiros Utilitários

## Objetivo

Implementar as primeiras ferramentas simples para validar a arquitetura modular.

## Entregas

- Gerador de QR Code
- Gerador de senhas
- Estrutura base de resposta da API
- Tela inicial do frontend
- Navegação entre ferramentas
- Primeiras páginas de ferramentas
- Integração frontend/backend

## Módulos Envolvidos

- qrcode_tools
- password_tools

## Status

Pendente.

## Fase 3 — Ferramentas para Desenvolvedores

## Objetivo

Adicionar ferramentas úteis para desenvolvimento.

## Entregas

- Formatador de JSON
- Validador de JSON
- Minificador de JSON
- Gerador de hashes
- Gerador de slug
- Utilitários de texto

## Módulos Envolvidos

- json_tools
- hash_tools
- slug_tools
- text_tools

## Status

Pendente.

## Fase 4 — Validações e Datas

## Objetivo

Adicionar ferramentas com regras simples e utilidade prática.

## Entregas

- Validador de CPF
- Validador de CNPJ
- Formatador de CPF
- Formatador de CNPJ
- Manipulação de datas
- Cálculo de diferença entre datas
- Conversão de timestamp

## Módulos Envolvidos

- document_tools
- date_tools

## Status

Pendente.

## Fase 5 — Imagens

## Objetivo

Adicionar ferramentas para manipulação básica de imagens.

## Entregas

- Upload de imagem
- Conversão de formatos
- Redimensionamento de imagem
- Extração de metadados
- Compressão simples

## Módulos Envolvidos

- image_tools

## Status

Pendente.

## Fase 6 — Links e Arquivos

## Objetivo

Adicionar ferramentas para manipulação de links e geração de arquivos simples.

## Entregas

- Validador de URL
- Gerador de código curto
- Gerador de arquivo TXT
- Gerador de arquivo CSV
- Gerador de arquivo JSON
- Download de arquivos gerados

## Módulos Envolvidos

- link_tools
- file_tools

## Status

Pendente.

## Fase 7 — Recursos Avançados

## Objetivo

Adicionar funcionalidades mais complexas de forma controlada.

## Entregas Possíveis

- Remoção de fundo de imagem
- Encurtador de links com banco de dados
- Histórico de uso
- Autenticação
- Painel do usuário
- Favoritos
- Processamento de mídia

## Módulos Envolvidos

- image_tools
- link_tools
- media_tools

## Status

Futuro.

## Fase 8 — Deploy e Polimento

## Objetivo

Preparar o projeto para publicação e apresentação no portfólio.

## Entregas

- Deploy do frontend
- Deploy do backend
- Configuração da Vercel
- Ajustes de responsividade
- Melhorias visuais
- Tratamento de erros
- Estados de loading
- Revisão do README
- Revisão da documentação
- Prints ou preview do projeto
- Adição ao portfólio

## Status

Futuro.

## Fase 9 — Melhorias Futuras

## Possibilidades

- Testes automatizados
- Logs estruturados
- Rate limit
- Banco de dados
- Autenticação
- Histórico por usuário
- Deploy separado do backend
- Serviços externos para processamento pesado
- Internacionalização
- Tema claro e escuro
- Mais ferramentas utilitárias

## Critérios de Evolução

Uma nova fase só deve começar quando a anterior estiver estável.

Antes de adicionar novas ferramentas, o projeto deve manter:

- código limpo
- layout funcional
- endpoints testados
- documentação atualizada
- padrão modular preservado

## Ordem Oficial

1. Base do projeto
2. QR Code e senhas
3. JSON, hash, slug e texto
4. CPF, CNPJ e datas
5. Imagens
6. Links e arquivos
7. Recursos avançados
8. Deploy e polimento
9. Melhorias futuras

## Objetivo Final

Ao final do roadmap, o projeto deve funcionar como uma central de utilitários desenvolvida com Python, com interface moderna, arquitetura simples e potencial de evolução.
