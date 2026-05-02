# Escopo

## Nome do Projeto

Lab Python Utilities

## Definição

O Lab Python Utilities é uma aplicação full stack que reúne ferramentas úteis do dia a dia desenvolvidas com Python.

O projeto terá um frontend moderno separado e um backend em FastAPI, mantendo uma arquitetura simples, modular e fácil de manter.

## Objetivo Principal

Criar uma aplicação prática para demonstrar o uso de Python em tarefas comuns, como manipulação de textos, dados, documentos, imagens, arquivos, links e automações simples.

## Objetivos Técnicos

O projeto deve demonstrar:

- criação de APIs com FastAPI
- organização modular de backend
- integração entre frontend e backend
- uso prático de Python
- validação de dados
- manipulação de arquivos e imagens
- construção de interface moderna com Vue 3
- deploy de aplicação full stack
- código limpo e de fácil manutenção

## Público-Alvo

O projeto é voltado para:

- desenvolvedores
- estudantes
- pessoas que precisam de ferramentas rápidas
- usuários que desejam utilitários simples em uma única interface

## Stack Oficial

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
- python-slugify
- python-dateutil

### Deploy

- Vercel

## Funcionalidades Planejadas

### QR Code

- Gerar QR Code a partir de texto
- Gerar QR Code a partir de URL
- Baixar QR Code como imagem

### Links

- Validar URL
- Gerar código curto
- Encurtar links futuramente com banco de dados

### Imagens

- Converter imagens
- Redimensionar imagens
- Extrair metadados
- Comprimir imagens
- Remover fundo em fase futura

### Senhas

- Gerar senha segura
- Definir tamanho
- Incluir números
- Incluir símbolos
- Incluir letras maiúsculas e minúsculas

### JSON

- Formatar JSON
- Validar JSON
- Minificar JSON

### Documentos

- Validar CPF
- Validar CNPJ
- Formatar CPF
- Formatar CNPJ

### Slug

- Gerar slug
- Remover acentos
- Normalizar texto para URL

### Texto

- Converter texto para maiúsculas
- Converter texto para minúsculas
- Converter texto para title case
- Limpar espaços duplicados
- Remover acentos
- Contar palavras
- Contar caracteres

### Arquivos

- Gerar arquivos simples
- Gerar TXT
- Gerar CSV
- Gerar JSON
- Extrair informações básicas

### Hash

- Gerar MD5
- Gerar SHA1
- Gerar SHA256
- Gerar SHA512

### Datas

- Formatar datas
- Calcular diferença entre datas
- Adicionar dias, meses ou anos
- Converter timestamp

### Mídia

- Obter informações de vídeos
- Converter vídeos próprios ou autorizados para MP3
- Baixar conteúdos próprios, autorizados ou livres de direitos

## Escopo do MVP

A primeira versão do projeto será focada em ferramentas leves e de rápida validação.

### Entra no MVP

- Health check da API
- Gerador de QR Code
- Gerador de senhas
- Formatador de JSON
- Validador de JSON
- Validador de CPF
- Validador de CNPJ
- Gerador de slug
- Limpador de texto
- Conversor de texto
- Gerador de hash
- Manipulação básica de datas
- Conversor simples de imagens
- Redimensionador de imagens

### Não Entra no MVP

- Autenticação
- Banco de dados
- Histórico de uso
- Sistema de usuários
- Painel administrativo
- Encurtador persistente
- Download automatizado de vídeos protegidos
- Conversões pesadas de mídia
- Processamento assíncrono
- Filas
- Pagamentos
- Recursos premium

## Regras do Projeto

### Simplicidade

O projeto deve começar simples.

Funcionalidades avançadas só devem ser adicionadas após a base estar funcionando.

### Modularidade

Cada ferramenta deve ter seu próprio módulo.

### Clareza

O código deve ser fácil de entender.

A documentação deve explicar o projeto sem excesso de detalhes.

### Responsabilidade

Funcionalidades de mídia devem respeitar permissões, direitos autorais e termos de uso das plataformas.

## Limites Técnicos

Como o deploy inicial será feito na Vercel, o projeto deve evitar:

- processamento muito pesado
- arquivos grandes
- armazenamento local permanente
- tarefas longas
- dependências desnecessariamente pesadas

## Critérios de Sucesso

O projeto será considerado bem-sucedido quando:

- o frontend estiver integrado ao backend
- as primeiras ferramentas estiverem funcionais
- a API estiver organizada por módulos
- a documentação estiver clara
- o deploy estiver publicado
- o código estiver limpo e fácil de evoluir

## Resultado Esperado

O resultado final será uma central de utilitários feita com Python, com frontend moderno, backend modular e estrutura preparada para evolução progressiva.
