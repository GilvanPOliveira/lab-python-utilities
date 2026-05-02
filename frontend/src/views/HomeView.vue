<script setup lang="ts">
const sections = [
  {
    title: 'Utilitários principais',
    description: 'Ferramentas mais úteis para o dia a dia.',
    tools: [
      {
        title: 'QR Code',
        description: 'Gere QR Codes a partir de URLs ou textos.',
        to: '/qrcode',
      },
      {
        title: 'Senhas',
        description: 'Crie senhas fortes e copie rapidamente.',
        to: '/passwords',
      },
      {
        title: 'CPF/CNPJ',
        description: 'Valide documentos brasileiros e copie o resultado.',
        to: '/documents',
      },
      {
        title: 'Texto',
        description: 'Limpe, converta e conte informações de texto.',
        to: '/text',
      },
      {
        title: 'Datas',
        description: 'Formate, compare e manipule datas.',
        to: '/dates',
      },
      {
        title: 'Imagens',
        description: 'Converta, redimensione e baixe imagens.',
        to: '/images',
      },
      {
        title: 'Links',
        description: 'Limpe URLs, remova tracking e abra o resultado.',
        to: '/links',
      },
      {
        title: 'Arquivos',
        description: 'Extraia metadados de arquivos locais.',
        to: '/files',
      },
      {
        title: 'Unidades e Fórmulas',
        description: 'Converta unidades e calcule fórmulas rápidas.',
        to: '/units',
      },
      {
        title: 'Cores',
        description: 'Converta HEX, RGB, HSL e gere paletas simples.',
        to: '/colors',
      },
      {
        title: 'Markdown',
        description: 'Gere tabelas, listas e visualize Markdown.',
        to: '/markdown',
      },
      {
        title: 'Dados Fake',
        description: 'Gere textos, nomes, emails, telefones e JSON fake.',
        to: '/fake-data',
      },
      {
        title: 'Assinatura',
        description: 'Gere assinatura de email em HTML e texto.',
        to: '/signature',
      },
    ],
  },
  {
    title: 'Dev Tools',
    description: 'Ferramentas úteis para desenvolvimento e manipulação de dados.',
    tools: [
      {
        title: 'JSON',
        description: 'Formate, valide e minifique payloads JSON.',
        to: '/json',
      },
      {
        title: 'Slug',
        description: 'Transforme títulos em slugs para URLs.',
        to: '/slug',
      },
      {
        title: 'Mensagens',
        description: 'Gere mensagens rápidas para LinkedIn, recrutadores e follow-ups.',
        to: '/messages',
      },
      {
        title: 'PDF',
        description: 'Junte, separe e extraia texto de arquivos PDF.',
        to: '/pdf',
      },
      {
        title: 'Mídia',
        description: 'Baixe mídia autorizada e extraia áudio em MP3.',
        to: '/media',
      },
      {
        title: 'Hash',
        description: 'Gere hashes para comparação e integridade de dados.',
        to: '/hash',
      },
    ],
  },
];
</script>

<template>
  <section class="space-y-10">
    <div class="max-w-3xl">
      <p class="mb-3 text-sm font-semibold uppercase tracking-[0.3em] text-cyan-400">
        Python utilities lab
      </p>

      <h2 class="text-4xl font-bold tracking-tight text-white md:text-5xl">
        Um canivete suíço em Python para tarefas rápidas.
      </h2>

      <p class="mt-5 text-lg leading-8 text-slate-300">
        Uma central pessoal de ferramentas úteis para evitar depender de sites cheios de anúncios.
      </p>
    </div>

    <div v-for="section in sections" :key="section.title" class="space-y-4">
      <div>
        <h3 class="text-2xl font-bold text-white">{{ section.title }}</h3>
        <p class="mt-1 text-sm text-slate-400">{{ section.description }}</p>
      </div>

      <div class="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <RouterLink
          v-for="tool in section.tools"
          :key="tool.to"
          :to="tool.to"
          class="min-h-36 rounded-2xl border border-slate-800 bg-slate-900 p-5 transition hover:-translate-y-1 hover:border-cyan-400 hover:bg-slate-900/80"
        >
          <h4 class="text-lg font-semibold text-white">{{ tool.title }}</h4>
          <p class="mt-2 text-sm leading-6 text-slate-400">{{ tool.description }}</p>
        </RouterLink>
      </div>
    </div>
  </section>
</template>
