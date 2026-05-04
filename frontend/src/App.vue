<script setup lang="ts">
import { computed, ref } from 'vue'
import { RouterLink, RouterView, useRoute } from 'vue-router'

const route = useRoute()
const search = ref('')
const menuOpen = ref(false)

const groups = [
  {
    label: 'Essenciais',
    tools: [
      { label: 'Home', to: '/', description: 'Visao geral das ferramentas' },
      { label: 'QR Code', to: '/qrcode', description: 'Gerar imagem PNG' },
      { label: 'Senhas', to: '/passwords', description: 'Criar credenciais fortes' },
      { label: 'CPF/CNPJ', to: '/documents', description: 'Validar documentos BR' },
      { label: 'Texto', to: '/text', description: 'Limpar e converter texto' },
      { label: 'Datas', to: '/dates', description: 'Formatar e calcular datas' },
    ],
  },
  {
    label: 'Arquivos e Mídia',
    tools: [
      { label: 'Imagens', to: '/images', description: 'Converter e redimensionar' },
      { label: 'Arquivos', to: '/files', description: 'Ler metadados' },
      { label: 'PDF', to: '/pdf', description: 'Juntar, separar e extrair texto' },
      { label: 'Mídia', to: '/media', description: 'Baixar vídeo e extrair MP3' },
    ],
  },
  {
    label: 'Dados e Dev',
    tools: [
      { label: 'JSON', to: '/json', description: 'Formatar, validar e minificar' },
      { label: 'Slug', to: '/slug', description: 'Criar URLs amigáveis' },
      { label: 'Hash', to: '/hash', description: 'Gerar checksums' },
      { label: 'Links', to: '/links', description: 'Limpar e encurtar URLs' },
      { label: 'Unidades', to: '/units', description: 'Converter medidas' },
      { label: 'Cores', to: '/colors', description: 'Converter HEX, RGB e HSL' },
      { label: 'Markdown', to: '/markdown', description: 'Criar tabelas e listas' },
      { label: 'Dados Fake', to: '/fake-data', description: 'Gerar dados de teste' },
    ],
  },
  {
    label: 'Comunicação',
    tools: [
      { label: 'Assinatura', to: '/signature', description: 'Gerar assinatura de email' },
      { label: 'Mensagens', to: '/messages', description: 'Criar textos rápidos' },
    ],
  },
]

const allTools = computed(() => groups.flatMap((group) => group.tools))

const currentTool = computed(() => {
  return allTools.value.find((tool) => tool.to === route.path) || allTools.value[0]
})

const filteredGroups = computed(() => {
  const term = search.value.trim().toLowerCase()

  if (!term) return groups

  return groups
    .map((group) => ({
      ...group,
      tools: group.tools.filter((tool) => {
        return `${tool.label} ${tool.description}`.toLowerCase().includes(term)
      }),
    }))
    .filter((group) => group.tools.length)
})

function closeMenu() {
  menuOpen.value = false
}
</script>

<template>
  <div class="min-h-screen bg-[#0b1020] text-slate-100">
    <a
      href="#content"
      class="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:rounded-md focus:bg-white focus:px-4 focus:py-2 focus:text-sm focus:font-semibold focus:text-slate-950"
    >
      Ir para o conteúdo
    </a>

    <header class="sticky top-0 z-40 border-b border-white/10 bg-[#0b1020]/95 backdrop-blur">
      <div class="mx-auto flex max-w-[1500px] items-center justify-between gap-4 px-4 py-3 lg:px-6">
        <RouterLink to="/" class="min-w-0" @click="closeMenu">
          <span class="block text-xs font-semibold uppercase tracking-[0.24em] text-teal-300">Lab Python</span>
          <span class="block truncaté text-lg font-bold text-white">Utilities Workspace</span>
        </RouterLink>

        <div class="hidden min-w-[280px] max-w-md flex-1 lg:block">
          <label class="sr-only" for="global-search">Buscar ferramenta</label>
          <input
            id="global-search"
            v-model="search"
            type="search"
            placeholder="Buscar ferramenta"
            class="w-full rounded-md border border-white/10 bg-white/[0.04] px-3 py-2 text-sm text-white outline-none transition placeholder:text-slate-500 focus:border-teal-300 focus:ring-2 focus:ring-teal-300/20"
          />
        </div>

        <button
          type="button"
          class="rounded-md border border-white/10 px-3 py-2 text-sm font-semibold text-slate-200 transition hover:border-teal-300 hover:text-white lg:hidden"
          :aria-expanded="menuOpen"
          aria-controls="mobile-navigation"
          @click="menuOpen = !menuOpen"
        >
          Menu
        </button>
      </div>
    </header>

    <div class="mx-auto grid max-w-[1500px] lg:grid-cols-[300px_1fr]">
      <aside
        id="mobile-navigation"
        class="border-b border-white/10 bg-[#0f172a] lg:sticky lg:top-[65px] lg:h-[calc(100vh-65px)] lg:border-b-0 lg:border-r"
        :class="menuOpen ? 'block' : 'hidden lg:block'"
      >
        <div class="flex h-full flex-col gap-4 overflow-y-auto px-4 py-4 lg:px-5">
          <div class="lg:hidden">
            <label class="sr-only" for="mobile-search">Buscar ferramenta</label>
            <input
              id="mobile-search"
              v-model="search"
              type="search"
              placeholder="Buscar ferramenta"
              class="w-full rounded-md border border-white/10 bg-white/[0.04] px-3 py-2 text-sm text-white outline-none transition placeholder:text-slate-500 focus:border-teal-300 focus:ring-2 focus:ring-teal-300/20"
            />
          </div>

          <div class="rounded-lg border border-white/10 bg-white/[0.035] p-3">
            <p class="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Atual</p>
            <p class="mt-2 text-sm font-semibold text-white">{{ currentTool.label }}</p>
            <p class="mt-1 text-xs leading-5 text-slate-400">{{ currentTool.description }}</p>
          </div>

          <nav class="space-y-5" aria-label="Ferramentas">
            <section v-for="group in filteredGroups" :key="group.label" class="space-y-2">
              <h2 class="px-2 text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">
                {{ group.label }}
              </h2>

              <div class="space-y-1">
                <RouterLink
                  v-for="tool in group.tools"
                  :key="tool.to"
                  :to="tool.to"
                  class="group block rounded-md border px-3 py-2 transition"
                  :class="
                    route.path === tool.to
                      ? 'border-teal-300/60 bg-teal-300/10 text-white'
                      : 'border-transparent text-slate-300 hover:border-white/10 hover:bg-white/[0.045] hover:text-white'
                  "
                  @click="closeMenu"
                >
                  <span class="block text-sm font-semibold">{{ tool.label }}</span>
                  <span class="mt-0.5 block text-xs leading-5 text-slate-500 group-hover:text-slate-400">
                    {{ tool.description }}
                  </span>
                </RouterLink>
              </div>
            </section>
          </nav>
        </div>
      </aside>

      <main id="content" class="min-w-0 px-4 py-6 lg:px-8 lg:py-8">
        <div class="mx-auto max-w-6xl">
          <RouterView v-slot="{ Component }">
            <Transition name="page" mode="out-in">
              <component :is="Component" :key="route.fullPath" />
            </Transition>
          </RouterView>
        </div>
      </main>
    </div>
  </div>
</template>
