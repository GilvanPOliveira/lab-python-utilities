<script setup lang="ts">
import { ref } from 'vue'
import { api } from '../services/api'

const selectedFile = ref<File | null>(null)
const metadata = ref<any | null>(null)
const error = ref('')
const copied = ref(false)
const loading = ref(false)

function formatBytes(bytes: number) {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`
  return `${(bytes / 1024 / 1024).toFixed(2)} MB`
}

function handleFile(event: Event) {
  const input = event.target as HTMLInputElement
  selectedFile.value = input.files?.[0] || null
  metadata.value = null
  error.value = ''
  copied.value = false
}

async function extractMetadata() {
  if (!selectedFile.value) {
    error.value = 'Selecione um arquivo.'
    return
  }

  error.value = ''
  metadata.value = null
  copied.value = false
  loading.value = true

  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)

    const response = await api.post('/files/metadata', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    metadata.value = response.data
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Não foi possível extrair os metadados.'
  } finally {
    loading.value = false
  }
}

async function copyMetadata() {
  if (!metadata.value) return

  await navigator.clipboard.writeText(JSON.stringify(metadata.value, null, 2))
  copied.value = true

  window.setTimeout(() => {
    copied.value = false
  }, 1800)
}
</script>

<template>
  <section class="tool-page">
    <div>
      <h2 class="text-3xl font-bold text-white">File Tools</h2>
      <p class="mt-2 text-slate-400">
        Extraia metadados de arquivos locais rapidamente.
      </p>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <div class="min-h-[var(--tool-panel-min-height)] space-y-5 rounded-lg border border-white/10 bg-white/[0.045] p-5">
        <div>
          <h3 class="text-lg font-semibold text-white">Extrair metadados</h3>
          <p class="mt-1 text-sm text-slate-400">
            Veja nome, extensão, MIME type, tamanho e informações de imagem quando houver.
          </p>
        </div>

        <input
          type="file"
          class="w-full rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 text-sm text-slate-300 outline-none"
          @change="handleFile"
        />

        <button
          type="button"
          class="w-full rounded-md bg-teal-300 px-5 py-3 font-semibold text-slate-950 transition hover:bg-teal-200 disabled:opacity-60"
          :disabled="loading"
          @click="extractMetadata"
        >
          {{ loading ? 'Lendo arquivo...' : 'Extrair metadados' }}
        </button>

        <p v-if="error" class="rounded-md border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
          {{ error }}
        </p>

        <div v-if="selectedFile" class="rounded-lg border border-white/10 bg-[#0b1020] p-4">
          <h4 class="text-sm font-semibold text-white">Arquivo selecionado</h4>
          <div class="mt-3 grid gap-2 text-sm text-slate-300">
            <p class="break-all"><span class="text-slate-500">Nome:</span> {{ selectedFile.name }}</p>
            <p><span class="text-slate-500">Tipo:</span> {{ selectedFile.type || 'não identificado' }}</p>
            <p><span class="text-slate-500">Tamanho:</span> {{ formatBytes(selectedFile.size) }}</p>
          </div>
        </div>
      </div>

      <div class="min-h-[var(--tool-panel-min-height)] rounded-lg border border-white/10 bg-white/[0.045] p-5">
        <h3 class="text-lg font-semibold text-white">Resultado</h3>

        <div v-if="metadata" class="mt-4 space-y-4">
          <div class="rounded-lg border border-teal-300/30 bg-teal-300/10 p-4">
            <p class="text-sm text-teal-50">
              Arquivo lido:
              <span class="font-mono text-teal-200">{{ metadata.filename }}</span>
            </p>
          </div>

          <div class="rounded-lg border border-white/10 bg-[#0b1020] p-4">
            <div class="grid gap-2 text-sm text-slate-300">
              <p><span class="text-slate-500">Extensão:</span> {{ metadata.extension || 'sem extensão' }}</p>
              <p><span class="text-slate-500">Tipo:</span> {{ metadata.mime_type || 'não identificado' }}</p>
              <p><span class="text-slate-500">Tamanho:</span> {{ formatBytes(metadata.size_bytes) }}</p>
              <p><span class="text-slate-500">É imagem:</span> {{ metadata.is_image ? 'sim' : 'não' }}</p>
              <p v-if="metadata.is_image"><span class="text-slate-500">Formato:</span> {{ metadata.image_format }}</p>
              <p v-if="metadata.is_image"><span class="text-slate-500">Dimensões:</span> {{ metadata.width }}x{{ metadata.height }}</p>
              <p v-if="metadata.is_image"><span class="text-slate-500">Modo de cor:</span> {{ metadata.color_mode }}</p>
            </div>
          </div>

          <button
            type="button"
            class="rounded-md border border-teal-300 px-4 py-2 text-sm font-semibold text-teal-200 transition hover:bg-teal-300 hover:text-slate-950"
            @click="copyMetadata"
          >
            {{ copied ? 'Metadados copiados!' : 'Copiar metadados' }}
          </button>
        </div>

        <p v-else class="mt-4 text-sm leading-6 text-slate-400">
          Selecione um arquivo e extraia os metadados.
        </p>
      </div>
    </div>
  </section>
</template>
