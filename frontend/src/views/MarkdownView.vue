<script setup lang="ts">
import { ref } from 'vue'
import { api } from '../services/api'

type MarkdownMode = 'preview' | 'strip' | 'table' | 'list'

const mode = ref<MarkdownMode>('preview')
const content = ref('# Título\n\nTexto com **negrito**, *itálico* e `código`.\n\n- Item 1\n- Item 2')
const headers = ref('Nome, Email, Stack')
const rows = ref('Alex Demo, alex.demo@example.com, Vue\nSam Tester, sam.tester@example.com, Python')
const listItems = ref('Item 1\nItem 2\nItem 3')
const ordered = ref(false)

const result = ref('')
const error = ref('')
const copied = ref(false)
const loading = ref(false)

function parseLines(value: string) {
  return value
    .split('\n')
    .map((item) => item.trim())
    .filter(Boolean)
}

function parseCsvLines(value: string) {
  return value
    .split('\n')
    .map((line) => line.split(',').map((cell) => cell.trim()))
    .filter((row) => row.length > 0)
}

async function processMarkdown() {
  error.value = ''
  result.value = ''
  copied.value = false
  loading.value = true

  try {
    if (mode.value === 'preview') {
      const response = await api.post('/markdown/preview', {
        content: content.value,
      })

      result.value = response.data.result
      return
    }

    if (mode.value === 'strip') {
      const response = await api.post('/markdown/strip', {
        content: content.value,
      })

      result.value = response.data.result
      return
    }

    if (mode.value === 'table') {
      const response = await api.post('/markdown/table', {
        headers: headers.value.split(',').map((item) => item.trim()).filter(Boolean),
        rows: parseCsvLines(rows.value),
      })

      result.value = response.data.result
      return
    }

    const response = await api.post('/markdown/list', {
      items: parseLines(listItems.value),
      ordered: ordered.value,
    })

    result.value = response.data.result
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Não foi possível processar o Markdown.'
  } finally {
    loading.value = false
  }
}

async function copyResult() {
  if (!result.value) return

  await navigator.clipboard.writeText(result.value)
  copied.value = true

  window.setTimeout(() => {
    copied.value = false
  }, 1800)
}
</script>

<template>
  <section class="tool-page">
    <div>
      <h2 class="text-3xl font-bold text-white">Markdown Tools</h2>
      <p class="mt-2 text-slate-400">
        Gere tabelas, listas, remova Markdown ou visualize um preview simples.
      </p>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <form class="min-h-[var(--tool-panel-min-height)] space-y-5 rounded-lg border border-white/10 bg-white/[0.045] p-5" @submit.prevent="processMarkdown">
        <div>
          <span class="text-sm font-medium text-slate-300">Ferramenta</span>

          <div class="mt-2 grid grid-cols-2 gap-2 rounded-lg border border-white/10 bg-[#0b1020] p-2">
            <button
              v-for="option in [
                { key: 'preview', label: 'Preview' },
                { key: 'strip', label: 'Remover MD' },
                { key: 'table', label: 'Tabela' },
                { key: 'list', label: 'Lista' },
              ]"
              :key="option.key"
              type="button"
              class="rounded-md px-3 py-3 text-sm font-semibold transition"
              :class="mode === option.key
                ? 'bg-teal-300 text-slate-950'
                : 'text-slate-300 hover:bg-white/[0.045] hover:text-white'"
              @click="mode = option.key as MarkdownMode; result = ''"
            >
              {{ option.label }}
            </button>
          </div>
        </div>

        <label v-if="mode === 'preview' || mode === 'strip'" class="block">
          <span class="text-sm font-medium text-slate-300">Markdown</span>

          <textarea
            v-model="content"
            rows="14"
            class="mt-2 w-full resize-none rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 font-mono text-sm text-white outline-none focus:border-teal-300"
          />
        </label>

        <div v-if="mode === 'table'" class="space-y-4">
          <label class="block">
            <span class="text-sm font-medium text-slate-300">Cabeçalhos separados por vírgula</span>
            <input
              v-model="headers"
              type="text"
              class="mt-2 w-full rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 text-white outline-none focus:border-teal-300"
            />
          </label>

          <label class="block">
            <span class="text-sm font-medium text-slate-300">Linhas separadas por vírgula</span>
            <textarea
              v-model="rows"
              rows="10"
              class="mt-2 w-full resize-none rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 font-mono text-sm text-white outline-none focus:border-teal-300"
            />
          </label>
        </div>

        <div v-if="mode === 'list'" class="space-y-4">
          <label class="block">
            <span class="text-sm font-medium text-slate-300">Itens, um por linha</span>
            <textarea
              v-model="listItems"
              rows="10"
              class="mt-2 w-full resize-none rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 text-white outline-none focus:border-teal-300"
            />
          </label>

          <label class="flex items-center gap-3 rounded-md border border-white/10 bg-[#0b1020] p-3 text-sm text-slate-300">
            <input v-model="ordered" type="checkbox" class="h-4 w-4 accent-teal-300" />
            Lista ordenada
          </label>
        </div>

        <button
          type="submit"
          class="w-full rounded-md bg-teal-300 px-5 py-3 font-semibold text-slate-950 transition hover:bg-teal-200 disabled:opacity-60"
          :disabled="loading"
        >
          {{ loading ? 'Processando...' : 'Gerar resultado' }}
        </button>

        <p v-if="error" class="rounded-md border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
          {{ error }}
        </p>
      </form>

      <div class="min-h-[var(--tool-panel-min-height)] rounded-lg border border-white/10 bg-white/[0.045] p-5">
        <h3 class="text-lg font-semibold text-white">Resultado</h3>

        <div v-if="result" class="mt-4 space-y-4">
          <div
            v-if="mode === 'preview'"
            class="prose prose-invert max-h-[450px] max-w-none overflow-auto rounded-md border border-white/10 bg-[#0b1020] p-4 text-slate-300"
            v-html="result"
          />

          <pre
            v-else
            class="max-h-[450px] overflow-auto rounded-md border border-white/10 bg-[#0b1020] p-4 text-sm text-teal-50"
          >{{ result }}</pre>

          <button
            type="button"
            class="rounded-md border border-teal-300 px-4 py-2 text-sm font-semibold text-teal-200 transition hover:bg-teal-300 hover:text-slate-950"
            @click="copyResult"
          >
            {{ copied ? 'Copiado!' : 'Copiar resultado' }}
          </button>
        </div>

        <p v-else class="mt-4 text-sm leading-6 text-slate-400">
          O resultado aparecerá aqui.
        </p>
      </div>
    </div>
  </section>
</template>
