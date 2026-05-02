# Módulos

## Visão Geral

O Lab Python Utilities será organizado por módulos de ferramentas.

Cada módulo representa uma categoria de utilitários e possui responsabilidades próprias.

No backend, cada módulo ficará em:

backend/src/modules/

No frontend, cada área funcional ficará em:

frontend/src/features/

## Padrão dos Módulos do Backend

Cada módulo do backend deve seguir o padrão:

module_name/
├── router.py
├── schemas.py
└── service.py

## 1. QR Code Tools

## Objetivo

Gerar QR Codes a partir de textos ou URLs.

## Funcionalidades

- Gerar QR Code
- Retornar QR Code em imagem
- Permitir download do QR Code
- Configurar tamanho
- Configurar margem
- Futuramente permitir cores personalizadas

## Rotas Planejadas

POST /api/qrcode/generate

## Prioridade

Alta.

Este será um dos primeiros módulos implementados.

## 2. Password Tools

## Objetivo

Gerar senhas seguras de forma configurável.

## Funcionalidades

- Gerar senha aleatória
- Definir tamanho da senha
- Incluir letras maiúsculas
- Incluir letras minúsculas
- Incluir números
- Incluir símbolos
- Evitar senhas vazias ou inválidas

## Rotas Planejadas

POST /api/passwords/generate

## Prioridade

Alta.

Este módulo é simples, útil e ideal para validar a estrutura inicial do projeto.

## 3. JSON Tools

## Objetivo

Fornecer ferramentas para manipulação de JSON.

## Funcionalidades

- Formatar JSON
- Validar JSON
- Minificar JSON
- Retornar erros claros para JSON inválido

## Rotas Planejadas

POST /api/json/format
POST /api/json/validate
POST /api/json/minify

## Prioridade

Alta.

É uma ferramenta útil para desenvolvedores e simples de implementar.

## 4. Document Tools

## Objetivo

Validar e formatar documentos brasileiros.

## Funcionalidades

- Validar CPF
- Validar CNPJ
- Formatar CPF
- Formatar CNPJ
- Remover máscara de CPF/CNPJ

## Rotas Planejadas

POST /api/documents/validate-cpf
POST /api/documents/validate-cnpj
POST /api/documents/format-cpf
POST /api/documents/format-cnpj

## Prioridade

Alta.

Este módulo demonstra regras de negócio simples e validações reais.

## 5. Slug Tools

## Objetivo

Gerar slugs seguros para URLs.

## Funcionalidades

- Gerar slug a partir de texto
- Remover acentos
- Converter espaços em hífens
- Remover caracteres especiais
- Normalizar texto para uso em URL

## Rotas Planejadas

POST /api/slug/generate

## Prioridade

Alta.

É simples, útil e comum em aplicações web.

## 6. Text Tools

## Objetivo

Manipular e converter textos.

## Funcionalidades

- Converter para maiúsculas
- Converter para minúsculas
- Converter para title case
- Limpar espaços duplicados
- Remover quebras de linha
- Remover acentos
- Contar caracteres
- Contar palavras
- Normalizar texto

## Rotas Planejadas

POST /api/text/clean
POST /api/text/convert
POST /api/text/count

## Prioridade

Alta.

Módulo útil e com baixo custo de processamento.

## 7. Hash Tools

## Objetivo

Gerar hashes a partir de textos.

## Funcionalidades

- Gerar hash MD5
- Gerar hash SHA1
- Gerar hash SHA256
- Gerar hash SHA512

## Rotas Planejadas

POST /api/hash/generate

## Prioridade

Alta.

Ferramenta simples e útil para desenvolvedores.

## 8. Date Tools

## Objetivo

Manipular e formatar datas.

## Funcionalidades

- Formatar datas
- Calcular diferença entre datas
- Adicionar dias
- Adicionar meses
- Adicionar anos
- Converter timestamp
- Gerar data atual formatada

## Rotas Planejadas

POST /api/dates/format
POST /api/dates/difference
POST /api/dates/add

## Prioridade

Média.

Entra após os módulos iniciais.

## 9. Image Tools

## Objetivo

Manipular imagens de forma simples.

## Funcionalidades

- Converter imagens
- Redimensionar imagens
- Extrair metadados
- Comprimir imagens
- Remover fundo de imagem

## Rotas Planejadas

POST /api/images/convert
POST /api/images/resize
POST /api/images/metadata
POST /api/images/remove-background

## Prioridade

Média.

As funcionalidades leves entram primeiro.

Remoção de fundo fica para uma fase posterior por exigir mais processamento.

## 10. Link Tools

## Objetivo

Criar ferramentas para validação e manipulação de URLs.

## Funcionalidades

- Validar URL
- Limpar URL
- Gerar código curto
- Futuramente criar encurtador persistente
- Futuramente redirecionar URLs encurtadas

## Rotas Planejadas

POST /api/links/validate
POST /api/links/short-code
POST /api/links/shorten

## Prioridade

Média.

O encurtador real depende de banco de dados e fica para fase futura.

## 11. File Tools

## Objetivo

Gerar e processar arquivos simples.

## Funcionalidades

- Gerar arquivo TXT
- Gerar arquivo CSV
- Gerar arquivo JSON
- Extrair informações básicas de arquivos
- Retornar arquivo para download

## Rotas Planejadas

POST /api/files/generate-txt
POST /api/files/generate-csv
POST /api/files/generate-json
POST /api/files/metadata

## Prioridade

Média.

Pode ser implementado após os módulos de texto e JSON.

## 12. Media Tools

## Objetivo

Trabalhar com informações e conversões de mídia de forma controlada.

## Funcionalidades Futuras

- Obter informações de vídeo
- Converter vídeo próprio ou autorizado para MP3
- Download de vídeos próprios ou autorizados
- Download de mídias públicas com permissão de uso

## Rotas Planejadas

POST /api/media/video-info
POST /api/media/download-video
POST /api/media/download-audio

## Prioridade

Baixa.

Este módulo será tratado como avançado.

## Observação Importante

O módulo de mídia deve respeitar direitos autorais, termos de uso das plataformas e limitações técnicas do ambiente de deploy.

## Ordem Recomendada de Implementação

1. Health Check
2. QR Code Tools
3. Password Tools
4. JSON Tools
5. Document Tools
6. Slug Tools
7. Text Tools
8. Hash Tools
9. Date Tools
10. Image Tools
11. Link Tools
12. File Tools
13. Media Tools

## Critérios para Adicionar Novos Módulos

Um novo módulo só deve ser adicionado se:

- for útil no dia a dia
- puder ser explicado com clareza
- não exigir complexidade desnecessária
- mantiver o padrão router, schemas e service
- não comprometer o deploy
- estiver documentado neste arquivo

## Decisão Final

Os módulos serão criados de forma progressiva, priorizando primeiro ferramentas leves, úteis e fáceis de validar.
