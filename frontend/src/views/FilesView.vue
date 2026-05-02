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
  <section class="mx-auto max-w-5xl space-y-6">
    <div>
      <h2 class="text-3xl font-bold text-white">File Tools</h2>
      <p class="mt-2 text-slate-400">
        Extraia metadados de arquivos locais rapidamente.
      </p>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <div class="min-h-[480px] space-y-5 rounded-2xl border border-slate-800 bg-slate-900 p-5">
        <div>
          <h3 class="text-lg font-semibold text-white">Extrair metadados</h3>
          <p class="mt-1 text-sm text-slate-400">
            Veja nome, extensão, MIME type, tamanho e informações de imagem quando houver.
          </p>
        </div>

        <input
          type="file"
          class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-slate-300 outline-none file:mr-4 file:rounded-lg file:border-0 file:bg-cyan-400 file:px-3 file:py-2 file:font-semibold file:text-slate-950"
          @change="handleFile"
        />

        <button
          type="button"
          class="w-full rounded-xl bg-cyan-400 px-5 py-3 font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:opacity-60"
          :disabled="loading"
          @click="extractMetadata"
        >
          {{ loading ? 'Lendo arquivo...' : 'Extrair metadados' }}
        </button>

        <p v-if="error" class="rounded-xl border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
          {{ error }}
        </p>

        <div v-if="selectedFile" class="rounded-2xl border border-slate-800 bg-slate-950 p-4">
          <h4 class="text-sm font-semibold text-white">Arquivo selecionado</h4>
          <div class="mt-3 grid gap-2 text-sm text-slate-300">
            <p class="break-all"><span class="text-slate-500">Nome:</span> {{ selectedFile.name }}</p>
            <p><span class="text-slate-500">Tipo:</span> {{ selectedFile.type || 'não identificado' }}</p>
            <p><span class="text-slate-500">Tamanho:</span> {{ formatBytes(selectedFile.size) }}</p>
          </div>
        </div>
      </div>

      <div class="min-h-[480px] rounded-2xl border border-slate-800 bg-slate-900 p-5">
        <h3 class="text-lg font-semibold text-white">Resultado</h3>

        <div v-if="metadata" class="mt-4 space-y-4">
          <div class="rounded-2xl border border-cyan-400/30 bg-cyan-400/10 p-4">
            <p class="text-sm text-cyan-100">
              Arquivo lido:
              <span class="font-mono text-cyan-300">{{ metadata.filename }}</span>
            </p>
          </div>

          <div class="rounded-2xl border border-slate-800 bg-slate-950 p-4">
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
            class="rounded-xl border border-cyan-400 px-4 py-2 text-sm font-semibold text-cyan-300 transition hover:bg-cyan-400 hover:text-slate-950"
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
