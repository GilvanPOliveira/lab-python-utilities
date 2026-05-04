<script setup lang="ts">
const sections = [
  {
    title: 'Essenciais',
    description: 'Tarefas frequentes para uso rápido no dia a dia.',
    tools: [
      { title: 'QR Code', description: 'Gere QR Codes em PNG a partir de texto ou URL.', to: '/qrcode' },
      { title: 'Senhas', description: 'Crie senhas fortes com regras configuraveis.', to: '/passwords' },
      { title: 'CPF/CNPJ', description: 'Valide documentos brasileiros em poucos segundos.', to: '/documents' },
      { title: 'Texto', description: 'Limpe, converta, conte e normalize textos.', to: '/text' },
      { title: 'Datas', description: 'Formate, compare e some períodos.', to: '/dates' },
      { title: 'Links', description: 'Limpe tracking, codifique e encurte URLs.', to: '/links' },
    ],
  },
  {
    title: 'Arquivos',
    description: 'Ferramentas para conteúdo local e mídias autorizadas.',
    tools: [
      { title: 'Imagens', description: 'Converta, redimensione, compacte e remova fundos.', to: '/images' },
      { title: 'Arquivos', description: 'Extraia metadados básicos de arquivos locais.', to: '/files' },
      { title: 'PDF', description: 'Junte, separe e extraia texto de documentos.', to: '/pdf' },
      { title: 'Mídia', description: 'Baixe vídeo autorizado ou extraia áudio em MP3.', to: '/media' },
    ],
  },
  {
    title: 'Dados e desenvolvimento',
    description: 'Atalhos para payloads, strings, cores e testes.',
    tools: [
      { title: 'JSON', description: 'Formate, valide e minifique payloads.', to: '/json' },
      { title: 'Slug', description: 'Transforme títulos em URLs amigáveis.', to: '/slug' },
      { title: 'Hash', description: 'Gere MD5, SHA1, SHA256 e SHA512.', to: '/hash' },
      { title: 'Unidades', description: 'Converta unidades e calcule fórmulas.', to: '/units' },
      { title: 'Cores', description: 'Converta HEX, RGB, HSL e gere paletas.', to: '/colors' },
      { title: 'Markdown', description: 'Crie tabelas, listas e previews.', to: '/markdown' },
      { title: 'Dados Fake', description: 'Gere nomes, emails, telefones e JSON fake.', to: '/fake-data' },
      { title: 'Mensagens', description: 'Monte textos rápidos para contatos e follow-ups.', to: '/messages' },
      { title: 'Assinatura', description: 'Crie assinatura de email em HTML e texto.', to: '/signature' },
    ],
  },
]

const stats = [
  { label: 'Ferramentas', value: '20' },
  { label: 'Categorias', value: '4' },
  { label: 'Uso', value: 'Pessoal' },
]
</script>

<template>
  <section class="tool-page">
    <div class="grid gap-5 lg:grid-cols-[1fr_320px]">
      <div class="rounded-lg border border-white/10 bg-white/[0.045] p-6">
        <p class="text-xs font-semibold uppercase tracking-[0.24em] text-teal-200">
          Central pessoal de utilitários
        </p>

        <h1 class="mt-3 max-w-4xl text-3xl font-bold tracking-tight text-white md:text-4xl">
          Ferramentas simples, reunidas em um único painel.
        </h1>

        <p class="mt-4 max-w-2xl text-base leading-7 text-slate-300">
          Acesse tarefas de texto, arquivos, mídia, dados e desenvolvimento sem depender de sites externos cheios de ruído.
        </p>
      </div>

      <div class="grid gap-3 sm:grid-cols-3 lg:grid-cols-1">
        <div
          v-for="item in stats"
          :key="item.label"
          class="rounded-lg border border-white/10 bg-white/[0.045] p-4"
        >
          <p class="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">{{ item.label }}</p>
          <p class="mt-2 text-2xl font-bold text-white">{{ item.value }}</p>
        </div>
      </div>
    </div>

    <div v-for="section in sections" :key="section.title" class="space-y-3">
      <div class="flex flex-col gap-1 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h2 class="text-xl font-bold text-white">{{ section.title }}</h2>
          <p class="text-sm text-slate-400">{{ section.description }}</p>
        </div>
      </div>

      <div class="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
        <RouterLink
          v-for="tool in section.tools"
          :key="tool.to"
          :to="tool.to"
          class="group min-h-32 rounded-lg border border-white/10 bg-white/[0.04] p-4 transition hover:-translate-y-0.5 hover:border-teal-300/60 hover:bg-white/[0.065]"
        >
          <div class="flex items-start justify-between gap-3">
            <h3 class="text-base font-semibold text-white">{{ tool.title }}</h3>
            <span class="rounded-md border border-white/10 px-2 py-1 text-xs text-slate-400 transition group-hover:border-teal-300/50 group-hover:text-teal-200">
              Abrir
            </span>
          </div>
          <p class="mt-3 text-sm leading-6 text-slate-400">{{ tool.description }}</p>
        </RouterLink>
      </div>
    </div>
  </section>
</template>
