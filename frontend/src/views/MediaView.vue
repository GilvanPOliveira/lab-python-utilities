<script setup lang="ts">
import { ref } from 'vue'
import { api } from '../services/api'

type MediaMode = 'info' | 'download-video' | 'download-audio'

const mode = ref<MediaMode>('info')
const url = ref('')

const result = ref<any | null>(null)
const error = ref('')
const loading = ref(false)
const fileUrl = ref('')

function formatBytes(bytes: number) {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`
  return `${(bytes / 1024 / 1024).toFixed(2)} MB`
}

function clearFileUrl() {
  if (!fileUrl.value) return
  URL.revokeObjectURL(fileUrl.value)
  fileUrl.value = ''
}

async function extractErrorDetail(err: any) {
  const data = err.response?.data

  if (data instanceof Blob) {
    try {
      const parsed = JSON.parse(await data.text())
      return parsed.detail
    } catch {
      return ''
    }
  }

  return data?.detail
}

function getFilenameFromHeaders(headers: any) {
  const contentDisposition = headers['content-disposition'] || ''
  const filenameMatch = contentDisposition.match(/filename\*=UTF-8''([^;]+)|filename="?([^"]+)"?/)
  return decodeURIComponent(filenameMatch?.[1] || filenameMatch?.[2] || 'media-download')
}

async function processMedia() {
  clearFileUrl()
  result.value = null
  error.value = ''
  loading.value = true

  try {
    const response = await api.post(
      `/media/${mode.value}`,
      { url: url.value },
      mode.value === 'info' ? undefined : { responseType: 'blob' },
    )

    if (mode.value === 'info') {
      result.value = response.data
      return
    }

    const blob = response.data as Blob
    fileUrl.value = URL.createObjectURL(blob)
    result.value = {
      filename: getFilenameFromHeaders(response.headers),
      mime_type: blob.type || response.headers['content-type'] || 'application/octet-stream',
      size_bytes: blob.size,
      is_file: true,
    }
  } catch (err: any) {
    const detail = await extractErrorDetail(err)
    error.value = detail || 'Não foi possível processar a mídia.'
  } finally {
    loading.value = false
  }
}

function downloadFile() {
  if (!fileUrl.value || !result.value?.filename) return

  const link = document.createElement('a')
  link.href = fileUrl.value
  link.download = result.value.filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

function changeMode(nextMode: MediaMode) {
  mode.value = nextMode
  result.value = null
  error.value = ''
  clearFileUrl()
}
</script>

<template>
  <section class="tool-page">
    <div>
      <h2 class="text-3xl font-bold text-white">Mídia pessoal/autorizada</h2>
      <p class="mt-2 text-slate-400">
        Obtenha informações, baixe vídeo ou extraia MP3 de conteúdos próprios, autorizados ou livres de direitos.
      </p>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <form class="min-h-[var(--tool-panel-min-height)] space-y-5 rounded-lg border border-white/10 bg-white/[0.045] p-5" @submit.prevent="processMedia">
        <div>
          <span class="text-sm font-medium text-slate-300">Ferramenta</span>

          <div class="mt-2 grid gap-2 rounded-lg border border-white/10 bg-[#0b1020] p-2 sm:grid-cols-3">
            <button
              v-for="option in [
                { key: 'info', label: 'Info' },
                { key: 'download-video', label: 'Vídeo' },
                { key: 'download-audio', label: 'MP3' },
              ]"
              :key="option.key"
              type="button"
              class="rounded-md px-3 py-3 text-sm font-semibold transition"
              :class="mode === option.key
                ? 'bg-teal-300 text-slate-950'
                : 'text-slate-300 hover:bg-white/[0.045] hover:text-white'"
              @click="changeMode(option.key as MediaMode)"
            >
              {{ option.label }}
            </button>
          </div>
        </div>

        <label class="block">
          <span class="text-sm font-medium text-slate-300">URL da mídia</span>
          <textarea
            v-model="url"
            rows="6"
            placeholder="Cole a URL do seu vídeo, Reel autorizado ou mídia livre"
            class="mt-2 w-full resize-none rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 text-white outline-none focus:border-teal-300"
          />
        </label>

        <button
          type="submit"
          class="w-full rounded-md bg-teal-300 px-5 py-3 font-semibold text-slate-950 transition hover:bg-teal-200 disabled:opacity-60"
          :disabled="loading"
        >
          {{ loading ? 'Processando...' : 'Processar mídia' }}
        </button>

        <p class="rounded-md border border-amber-500/30 bg-amber-500/10 p-3 text-xs leading-5 text-amber-200">
          Use apenas com conteúdos próprios, autorizados ou livres de direitos. Para MP3, o backend usa FFmpeg do sistema ou imageio-ffmpeg.
        </p>

        <p v-if="error" class="rounded-md border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
          {{ error }}
        </p>
      </form>

      <div class="min-h-[var(--tool-panel-min-height)] rounded-lg border border-white/10 bg-white/[0.045] p-5">
        <h3 class="text-lg font-semibold text-white">Resultado</h3>

        <div v-if="result" class="mt-4 space-y-4">
          <template v-if="result.is_file">
            <div class="rounded-lg border border-teal-300/30 bg-teal-300/10 p-4">
              <p class="break-all text-sm text-teal-50">
                Arquivo:
                <span class="font-mono text-teal-200">{{ result.filename }}</span>
              </p>

              <p class="mt-2 text-sm text-slate-300">
                Tamanho: {{ formatBytes(result.size_bytes) }}
              </p>
            </div>

            <button
              type="button"
              class="rounded-md border border-teal-300 px-4 py-2 text-sm font-semibold text-teal-200 transition hover:bg-teal-300 hover:text-slate-950"
              @click="downloadFile"
            >
              Download
            </button>
          </template>

          <template v-else>
            <div class="rounded-lg border border-white/10 bg-[#0b1020] p-4">
              <img
                v-if="result.thumbnail"
                :src="result.thumbnail"
                alt="Thumbnail"
                class="mb-4 max-h-60 w-full rounded-md object-cover"
              />

              <div class="grid gap-2 text-sm text-slate-300">
                <p class="break-all"><span class="text-slate-500">Título:</span> {{ result.title }}</p>
                <p><span class="text-slate-500">Autor:</span> {{ result.uploader || 'não identificado' }}</p>
                <p><span class="text-slate-500">Duracao:</span> {{ result.duration || 'não informada' }} segundos</p>
                <p class="break-all"><span class="text-slate-500">URL:</span> {{ result.webpage_url }}</p>
              </div>
            </div>
          </template>
        </div>

        <p v-else class="mt-4 text-sm leading-6 text-slate-400">
          O resultado aparecerá aqui.
        </p>
      </div>
    </div>
  </section>
</template>
