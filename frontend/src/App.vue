<script setup lang="ts">
import { RouterLink, RouterView, useRoute } from 'vue-router'

const route = useRoute()

const mainLinks = [
  { label: 'Home', to: '/' },
  { label: 'QR Code', to: '/qrcode' },
  { label: 'Senhas', to: '/passwords' },
  { label: 'CPF/CNPJ', to: '/documents' },
  { label: 'Texto', to: '/text' },
  { label: 'Datas', to: '/dates' },
  { label: 'Imagens', to: '/images' },
  { label: 'Links', to: '/links' },
  { label: 'Arquivos', to: '/files' },
  { label: 'Unidades', to: '/units' },
  { label: 'Cores', to: '/colors' },
  { label: 'Markdown', to: '/markdown' },
  { label: 'Dados Fake', to: '/fake-data' },
  { label: 'Assinatura', to: '/signature' },
  { label: 'Mensagens', to: '/messages' },
  { label: 'PDF', to: '/pdf' },
  { label: 'Mídia', to: '/media' },
]

const devLinks = [
  { label: 'JSON', to: '/json' },
  { label: 'Slug', to: '/slug' },
  { label: 'Hash', to: '/hash' },
]
</script>

<template>
  <div class="min-h-screen bg-slate-950 text-slate-100">
    <header class="border-b border-slate-800 bg-slate-950/80 backdrop-blur">
      <div class="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-5">
        <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <RouterLink to="/" class="group">
            <p class="text-sm font-medium text-cyan-400">Lab Python Utilities</p>
            <h1 class="text-xl font-bold tracking-tight text-white">
              Python Tools para o dia a dia
            </h1>
          </RouterLink>

          <div class="flex flex-wrap gap-2">
            <RouterLink
              v-for="link in mainLinks"
              :key="link.to"
              :to="link.to"
              class="rounded-full border px-3 py-1.5 text-sm transition"
              :class="
                route.path === link.to
                  ? 'border-cyan-400 bg-cyan-400 text-slate-950'
                  : 'border-slate-700 bg-slate-900 text-slate-300 hover:border-cyan-400 hover:text-white'
              "
            >
              {{ link.label }}
            </RouterLink>
          </div>
        </div>

        <nav class="flex flex-wrap gap-2 border-t border-slate-800 pt-4">
          <span class="mr-1 flex items-center text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
            Dev Tools
          </span>

          <RouterLink
            v-for="link in devLinks"
            :key="link.to"
            :to="link.to"
            class="rounded-full border px-3 py-1.5 text-sm transition"
            :class="
              route.path === link.to
                ? 'border-cyan-400 bg-cyan-400 text-slate-950'
                : 'border-slate-700 bg-slate-900 text-slate-300 hover:border-cyan-400 hover:text-white'
            "
          >
            {{ link.label }}
          </RouterLink>
        </nav>
      </div>
    </header>

    <main class="mx-auto max-w-7xl px-4 py-8">
      <RouterView />
    </main>
  </div>
</template>
