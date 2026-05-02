<script setup lang="ts">
import { computed, ref } from 'vue'
import { api } from '../services/api'

type MediaMode = 'info' | 'download-video' | 'download-audio'

const mode = ref<MediaMode>('info')
const url = ref('')

const result = ref<any | null>(null)
const error = ref('')
const loading = ref(false)

const fileUrl = computed(() => {
  if (!result.value?.content_base64) return ''
  return `data:${result.value.mime_type};base64,${result.value.content_base64}`
})

function formatBytes(bytes: number) {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`
  return `${(bytes / 1024 / 1024).toFixed(2)} MB`
}

async function processMedia() {
  result.value = null
  error.value = ''
  loading.value = true

  try {
    const response = await api.post(`/media/${mode.value}`, {
      url: url.value,
    })

    result.value = response.data
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Não foi possível processar a mídia.'
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
</script>

<template>
  <section class="mx-auto max-w-5xl space-y-6">
    <div>
      <h2 class="text-3xl font-bold text-white">Mídia pessoal/autorizada</h2>
      <p class="mt-2 text-slate-400">
        Obtenha informações, baixe vídeo ou extraia MP3 de conteúdos próprios, autorizados ou livres de direitos.
      </p>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <form class="min-h-[560px] space-y-5 rounded-2xl border border-slate-800 bg-slate-900 p-5" @submit.prevent="processMedia">
        <div>
          <span class="text-sm font-medium text-slate-300">Ferramenta</span>

          <div class="mt-2 grid gap-2 rounded-2xl border border-slate-800 bg-slate-950 p-2 sm:grid-cols-3">
            <button
              v-for="option in [
                { key: 'info', label: 'Info' },
                { key: 'download-video', label: 'Vídeo' },
                { key: 'download-audio', label: 'MP3' },
              ]"
              :key="option.key"
              type="button"
              class="rounded-xl px-3 py-3 text-sm font-semibold transition"
              :class="mode === option.key
                ? 'bg-cyan-400 text-slate-950'
                : 'text-slate-300 hover:bg-slate-900 hover:text-white'"
              @click="mode = option.key as MediaMode; result = null; error = ''"
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
            class="mt-2 w-full resize-none rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
          />
        </label>

        <button
          type="submit"
          class="w-full rounded-xl bg-cyan-400 px-5 py-3 font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:opacity-60"
          :disabled="loading"
        >
          {{ loading ? 'Processando...' : 'Processar mídia' }}
        </button>

        <p class="rounded-xl border border-amber-500/30 bg-amber-500/10 p-3 text-xs leading-5 text-amber-200">
          Use apenas com conteúdos próprios, autorizados ou livres de direitos. Para MP3, o FFmpeg precisa estar instalado.
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
              <p class="break-all text-sm text-cyan-100">
                Arquivo:
                <span class="font-mono text-cyan-300">{{ result.filename }}</span>
              </p>

              <p class="mt-2 text-sm text-slate-300">
                Tamanho: {{ formatBytes(result.size_bytes) }}
              </p>
            </div>

            <button
              type="button"
              class="rounded-xl border border-cyan-400 px-4 py-2 text-sm font-semibold text-cyan-300 transition hover:bg-cyan-400 hover:text-slate-950"
              @click="downloadFile"
            >
              Download
            </button>
          </template>

          <template v-else>
            <div class="rounded-2xl border border-slate-800 bg-slate-950 p-4">
              <img
                v-if="result.thumbnail"
                :src="result.thumbnail"
                alt="Thumbnail"
                class="mb-4 max-h-60 w-full rounded-xl object-cover"
              />

              <div class="grid gap-2 text-sm text-slate-300">
                <p class="break-all"><span class="text-slate-500">Título:</span> {{ result.title }}</p>
                <p><span class="text-slate-500">Autor:</span> {{ result.uploader || 'não identificado' }}</p>
                <p><span class="text-slate-500">Duração:</span> {{ result.duration || 'não informada' }} segundos</p>
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
