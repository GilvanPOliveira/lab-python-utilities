<script setup lang="ts">
import { computed, ref } from 'vue'
import { api } from '../services/api'
import BaseNumberInput from '../components/BaseNumberInput.vue'

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
  <section class="tool-page">
    <div>
      <h2 class="text-3xl font-bold text-white">PDF Tools</h2>
      <p class="mt-2 text-slate-400">
        Junte PDFs, separe páginas e extraia texto de arquivos PDF.
      </p>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <form class="min-h-[var(--tool-panel-min-height)] space-y-5 rounded-lg border border-white/10 bg-white/[0.045] p-5" @submit.prevent="processPdf">
        <div>
          <span class="text-sm font-medium text-slate-300">Ferramenta</span>

          <div class="mt-2 grid grid-cols-3 gap-2 rounded-lg border border-white/10 bg-[#0b1020] p-2">
            <button
              v-for="option in [
                { key: 'merge', label: 'Juntar' },
                { key: 'split', label: 'Separar' },
                { key: 'extract-text', label: 'Texto' },
              ]"
              :key="option.key"
              type="button"
              class="rounded-md px-3 py-3 text-sm font-semibold transition"
              :class="mode === option.key
                ? 'bg-teal-300 text-slate-950'
                : 'text-slate-300 hover:bg-white/[0.045] hover:text-white'"
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
            class="mt-2 w-full rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 text-sm text-slate-300 outline-none"
            @change="handleMultipleFiles"
          />
          <p class="mt-2 text-xs text-slate-500">Envie pelo menos dois arquivos PDF.</p>
        </label>

        <label v-else class="block">
          <span class="text-sm font-medium text-slate-300">PDF</span>
          <input
            type="file"
            accept="application/pdf"
            class="mt-2 w-full rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 text-sm text-slate-300 outline-none"
            @change="handleSingleFile"
          />
        </label>

        <div v-if="mode === 'split'" class="grid gap-3 sm:grid-cols-2">
          <BaseNumberInput v-model="startPage" label="Pagina inicial" :min="1" :step="1" />
          <BaseNumberInput v-model="endPage" label="Pagina final" :min="1" :step="1" />
        </div>

        <button
          type="submit"
          class="w-full rounded-md bg-teal-300 px-5 py-3 font-semibold text-slate-950 transition hover:bg-teal-200 disabled:opacity-60"
          :disabled="loading"
        >
          {{ loading ? 'Processando...' : 'Processar PDF' }}
        </button>

        <p class="rounded-md border border-white/10 bg-[#0b1020] p-3 text-xs leading-5 text-slate-500">
          Limite recomendado: PDFs de até 15 MB.
        </p>

        <p v-if="error" class="rounded-md border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
          {{ error }}
        </p>
      </form>

      <div class="min-h-[var(--tool-panel-min-height)] rounded-lg border border-white/10 bg-white/[0.045] p-5">
        <h3 class="text-lg font-semibold text-white">Resultado</h3>

        <div v-if="result" class="mt-4 space-y-4">
          <template v-if="result.content_base64">
            <div class="rounded-lg border border-teal-300/30 bg-teal-300/10 p-4">
              <p class="text-sm text-teal-50">
                Arquivo pronto:
                <span class="font-mono text-teal-200">{{ result.filename }}</span>
              </p>
              <p class="mt-2 text-sm text-slate-300">
                Tamanho: {{ result.size_bytes }} bytes
              </p>
            </div>

            <button
              type="button"
              class="rounded-md border border-teal-300 px-4 py-2 text-sm font-semibold text-teal-200 transition hover:bg-teal-300 hover:text-slate-950"
              @click="downloadPdf"
            >
              Download PDF
            </button>
          </template>

          <template v-else>
            <div class="rounded-lg border border-white/10 bg-[#0b1020] p-4">
              <p class="text-sm text-slate-500">
                {{ result.filename }} - {{ result.pages }} página(s)
              </p>
              <pre class="mt-4 max-h-96 overflow-auto whitespace-pre-wrap text-sm text-teal-50">{{ result.text }}</pre>
            </div>

            <button
              type="button"
              class="rounded-md border border-teal-300 px-4 py-2 text-sm font-semibold text-teal-200 transition hover:bg-teal-300 hover:text-slate-950"
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
