<script setup lang="ts">
import { computed, ref } from 'vue'
import { api } from '../services/api'

type PdfMode = 'merge' | 'split' | 'extract-text'

const mode = ref<PdfMode>('merge')
const files = ref<File[]>([])
const singleFile = ref<File | null>(null)
const startPage = ref(1)
const endPage = ref(1)

const result = ref<any | null>(null)
const error = ref('')
const copied = ref(false)
const loading = ref(false)

const fileUrl = computed(() => {
  if (!result.value?.content_base64) return ''
  return `data:${result.value.mime_type};base64,${result.value.content_base64}`
})

function handleMultipleFiles(event: Event) {
  const input = event.target as HTMLInputElement
  files.value = Array.from(input.files || [])
  result.value = null
  error.value = ''
}

function handleSingleFile(event: Event) {
  const input = event.target as HTMLInputElement
  singleFile.value = input.files?.[0] || null
  result.value = null
  error.value = ''
}

async function processPdf() {
  result.value = null
  error.value = ''
  copied.value = false
  loading.value = true

  try {
    if (mode.value === 'merge') {
      const formData = new FormData()

      files.value.forEach((file) => {
        formData.append('files', file)
      })

      const response = await api.post('/pdf/merge', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })

      result.value = response.data
      return
    }

    if (!singleFile.value) {
      error.value = 'Selecione um PDF.'
      return
    }

    const formData = new FormData()
    formData.append('file', singleFile.value)

    if (mode.value === 'split') {
      formData.append('start_page', String(startPage.value))
      formData.append('end_page', String(endPage.value))

      const response = await api.post('/pdf/split', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })

      result.value = response.data
      return
    }

    const response = await api.post('/pdf/extract-text', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })

    result.value = response.data
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Não foi possível processar o PDF.'
  } finally {
    loading.value = false
  }
}

function downloadPdf() {
  if (!fileUrl.value || !result.value?.filename) return

  const link = document.createElement('a')
  link.href = fileUrl.value
  link.download = result.value.filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

async function copyText() {
  if (!result.value?.text) return

  await navigator.clipboard.writeText(result.value.text)
  copied.value = true

  window.setTimeout(() => {
    copied.value = false
  }, 1800)
}
</script>

<template>
  <section class="mx-auto max-w-5xl space-y-6">
    <div>
      <h2 class="text-3xl font-bold text-white">PDF Tools</h2>
      <p class="mt-2 text-slate-400">
        Junte PDFs, separe páginas e extraia texto de arquivos PDF.
      </p>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <form class="min-h-[560px] space-y-5 rounded-2xl border border-slate-800 bg-slate-900 p-5" @submit.prevent="processPdf">
        <div>
          <span class="text-sm font-medium text-slate-300">Ferramenta</span>

          <div class="mt-2 grid grid-cols-3 gap-2 rounded-2xl border border-slate-800 bg-slate-950 p-2">
            <button
              v-for="option in [
                { key: 'merge', label: 'Juntar' },
                { key: 'split', label: 'Separar' },
                { key: 'extract-text', label: 'Texto' },
              ]"
              :key="option.key"
              type="button"
              class="rounded-xl px-3 py-3 text-sm font-semibold transition"
              :class="mode === option.key
                ? 'bg-cyan-400 text-slate-950'
                : 'text-slate-300 hover:bg-slate-900 hover:text-white'"
              @click="mode = option.key as PdfMode; result = null; error = ''"
            >
              {{ option.label }}
            </button>
          </div>
        </div>

        <label v-if="mode === 'merge'" class="block">
          <span class="text-sm font-medium text-slate-300">PDFs para juntar</span>
          <input
            type="file"
            accept="application/pdf"
            multiple
            class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-slate-300 outline-none file:mr-4 file:rounded-lg file:border-0 file:bg-cyan-400 file:px-3 file:py-2 file:font-semibold file:text-slate-950"
            @change="handleMultipleFiles"
          />
          <p class="mt-2 text-xs text-slate-500">Envie pelo menos dois arquivos PDF.</p>
        </label>

        <label v-else class="block">
          <span class="text-sm font-medium text-slate-300">PDF</span>
          <input
            type="file"
            accept="application/pdf"
            class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-slate-300 outline-none file:mr-4 file:rounded-lg file:border-0 file:bg-cyan-400 file:px-3 file:py-2 file:font-semibold file:text-slate-950"
            @change="handleSingleFile"
          />
        </label>

        <div v-if="mode === 'split'" class="grid gap-3 sm:grid-cols-2">
          <label class="block">
            <span class="text-sm font-medium text-slate-300">Página inicial</span>
            <input
              v-model.number="startPage"
              type="number"
              min="1"
              class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
            />
          </label>

          <label class="block">
            <span class="text-sm font-medium text-slate-300">Página final</span>
            <input
              v-model.number="endPage"
              type="number"
              min="1"
              class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
            />
          </label>
        </div>

        <button
          type="submit"
          class="w-full rounded-xl bg-cyan-400 px-5 py-3 font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:opacity-60"
          :disabled="loading"
        >
          {{ loading ? 'Processando...' : 'Processar PDF' }}
        </button>

        <p class="rounded-xl border border-slate-800 bg-slate-950 p-3 text-xs leading-5 text-slate-500">
          Limite recomendado: PDFs de até 15 MB.
        </p>

        <p v-if="error" class="rounded-xl border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
          {{ error }}
        </p>
      </form>

      <div class="min-h-[560px] rounded-2xl border border-slate-800 bg-slate-900 p-5">
        <h3 class="text-lg font-semibold text-white">Resultado</h3>

        <div v-if="result" class="mt-4 space-y-4">
          <template v-if="result.content_base64">
            <div class="rounded-2xl border border-cyan-400/30 bg-cyan-400/10 p-4">
              <p class="text-sm text-cyan-100">
                Arquivo pronto:
                <span class="font-mono text-cyan-300">{{ result.filename }}</span>
              </p>
              <p class="mt-2 text-sm text-slate-300">
                Tamanho: {{ result.size_bytes }} bytes
              </p>
            </div>

            <button
              type="button"
              class="rounded-xl border border-cyan-400 px-4 py-2 text-sm font-semibold text-cyan-300 transition hover:bg-cyan-400 hover:text-slate-950"
              @click="downloadPdf"
            >
              Download PDF
            </button>
          </template>

          <template v-else>
            <div class="rounded-2xl border border-slate-800 bg-slate-950 p-4">
              <p class="text-sm text-slate-500">
                {{ result.filename }} - {{ result.pages }} página(s)
              </p>
              <pre class="mt-4 max-h-96 overflow-auto whitespace-pre-wrap text-sm text-cyan-100">{{ result.text }}</pre>
            </div>

            <button
              type="button"
              class="rounded-xl border border-cyan-400 px-4 py-2 text-sm font-semibold text-cyan-300 transition hover:bg-cyan-400 hover:text-slate-950"
              @click="copyText"
            >
              {{ copied ? 'Texto copiado!' : 'Copiar texto' }}
            </button>
          </template>
        </div>

        <p v-else class="mt-4 text-sm leading-6 text-slate-400">
          O resultado aparecerá aqui.
        </p>
      </div>
    </div>
  </section>
</template>
