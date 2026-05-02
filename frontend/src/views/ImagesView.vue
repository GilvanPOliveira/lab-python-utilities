<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'
import { api } from '../services/api'

type ImageMode = 'resize' | 'convert' | 'compress' | 'remove-background'

type ImageResult = {
  image_base64: string
  mime_type: string
  filename: string
  original_format: string
  original_width: number
  original_height: number
  original_size_bytes: number
  output_format: string
  output_width: number
  output_height: number
  output_size_bytes: number
}

const mode = ref<ImageMode>('resize')
const file = ref<File | null>(null)
const previewUrl = ref('')

const width = ref(800)
const height = ref(600)
const outputFormat = ref('webp')
const quality = ref(75)

const result = ref<ImageResult | null>(null)
const error = ref('')
const loading = ref(false)

const generatedImageUrl = computed(() => {
  if (!result.value) return ''
  return `data:${result.value.mime_type};base64,${result.value.image_base64}`
})

const currentActionLabel = computed(() => {
  const labels = {
    resize: 'Redimensionar imagem',
    convert: 'Converter imagem',
    compress: 'Comprimir imagem',
    'remove-background': 'Remover fundo',
  }

  return labels[mode.value]
})

function formatBytes(bytes: number) {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`
  return `${(bytes / 1024 / 1024).toFixed(2)} MB`
}

function clearPreviewUrl() {
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
    previewUrl.value = ''
  }
}

function selectMode(nextMode: ImageMode) {
  mode.value = nextMode
  result.value = null
  error.value = ''
}

function handleFile(event: Event) {
  const input = event.target as HTMLInputElement
  const selectedFile = input.files?.[0] || null

  error.value = ''
  result.value = null
  file.value = selectedFile
  clearPreviewUrl()

  if (!selectedFile) return

  if (!selectedFile.type.startsWith('image/')) {
    error.value = 'Envie apenas arquivos de imagem.'
    file.value = null
    return
  }

  if (selectedFile.size > 5 * 1024 * 1024) {
    error.value = 'A imagem deve ter no máximo 5 MB.'
    file.value = null
    return
  }

  previewUrl.value = URL.createObjectURL(selectedFile)
}

async function processImage() {
  if (!file.value) {
    error.value = 'Selecione uma imagem.'
    return
  }

  error.value = ''
  result.value = null
  loading.value = true

  try {
    const formData = new FormData()
    formData.append('file', file.value)

    const endpoint = `/images/${mode.value}`

    if (mode.value === 'resize') {
      formData.append('width', String(width.value))
      formData.append('height', String(height.value))
    }

    if (mode.value === 'convert') {
      formData.append('output_format', outputFormat.value)
    }

    if (mode.value === 'compress') {
      formData.append('output_format', outputFormat.value)
      formData.append('quality', String(quality.value))
    }

    const response = await api.post(endpoint, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    result.value = response.data
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Não foi possível processar a imagem.'
  } finally {
    loading.value = false
  }
}

function downloadImage() {
  if (!generatedImageUrl.value || !result.value) return

  const link = document.createElement('a')
  link.href = generatedImageUrl.value
  link.download = result.value.filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

onBeforeUnmount(() => {
  clearPreviewUrl()
})
</script>

<template>
  <section class="mx-auto max-w-6xl space-y-6">
    <div>
      <h2 class="text-3xl font-bold text-white">Ferramentas de Imagem</h2>
      <p class="mt-2 text-slate-400">
        Converta, redimensione, comprima e remova fundo de imagens.
      </p>
    </div>

    <p v-if="error" class="rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-300">
      {{ error }}
    </p>

    <div class="grid gap-6 xl:grid-cols-[420px_1fr]">
      <form class="h-fit space-y-5 rounded-2xl border border-slate-800 bg-slate-900 p-5" @submit.prevent="processImage">
        <label class="block">
          <span class="text-sm font-medium text-slate-300">Imagem</span>

          <input
            type="file"
            accept="image/*"
            class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-slate-300 outline-none file:mr-4 file:rounded-lg file:border-0 file:bg-cyan-400 file:px-3 file:py-2 file:font-semibold file:text-slate-950"
            @change="handleFile"
          />
        </label>

        <div>
          <span class="text-sm font-medium text-slate-300">Ação</span>

          <div class="mt-2 grid grid-cols-2 gap-2 rounded-2xl border border-slate-800 bg-slate-950 p-2">
            <button
              v-for="option in [
                { key: 'resize', label: 'Redimensionar' },
                { key: 'convert', label: 'Converter' },
                { key: 'compress', label: 'Comprimir' },
                { key: 'remove-background', label: 'Remover fundo' },
              ]"
              :key="option.key"
              type="button"
              class="rounded-xl px-3 py-3 text-sm font-semibold transition"
              :class="mode === option.key
                ? 'bg-cyan-400 text-slate-950'
                : 'text-slate-300 hover:bg-slate-900 hover:text-white'"
              @click="selectMode(option.key as ImageMode)"
            >
              {{ option.label }}
            </button>
          </div>
        </div>

        <div v-if="mode === 'resize'" class="grid gap-3 sm:grid-cols-2">
          <label class="block">
            <span class="text-sm font-medium text-slate-300">Largura</span>
            <input
              v-model.number="width"
              type="number"
              min="1"
              max="4000"
              class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
            />
          </label>

          <label class="block">
            <span class="text-sm font-medium text-slate-300">Altura</span>
            <input
              v-model.number="height"
              type="number"
              min="1"
              max="4000"
              class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
            />
          </label>
        </div>

        <label v-if="mode === 'convert' || mode === 'compress'" class="block">
          <span class="text-sm font-medium text-slate-300">Formato de saída</span>

          <select
            v-model="outputFormat"
            class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
          >
            <option value="png">PNG</option>
            <option value="jpg">JPG</option>
            <option value="webp">WEBP</option>
          </select>
        </label>

        <div v-if="mode === 'compress'" class="rounded-2xl border border-slate-800 bg-slate-950 p-4">
          <div class="flex items-center justify-between">
            <span class="text-sm font-medium text-slate-300">Qualidade</span>
            <span class="text-lg font-bold text-cyan-300">{{ quality }}%</span>
          </div>

          <input
            v-model.number="quality"
            type="range"
            min="1"
            max="100"
            class="mt-4 w-full accent-cyan-400"
          />
        </div>

        <button
          type="submit"
          class="w-full rounded-xl bg-cyan-400 px-5 py-3 font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-60"
          :disabled="loading"
        >
          {{ loading ? 'Processando...' : currentActionLabel }}
        </button>

        <p
          v-if="mode === 'remove-background'"
          class="rounded-xl border border-amber-500/30 bg-amber-500/10 p-3 text-xs leading-5 text-amber-200"
        >
          A primeira remoção de fundo pode demorar mais, pois usa processamento com modelo de imagem.
        </p>

        <p class="rounded-xl border border-slate-800 bg-slate-950 p-3 text-xs leading-5 text-slate-500">
          Limite recomendado: imagens de até 5 MB e dimensões máximas de 4000px.
        </p>
      </form>

      <div class="rounded-2xl border border-slate-800 bg-slate-900 p-5">
        <div class="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
          <div>
            <h3 class="text-lg font-semibold text-white">Preview e resultado</h3>
            <p class="mt-1 text-sm text-slate-400">
              A visualização é limitada para não quebrar a interface.
            </p>
          </div>

          <button
            v-if="result"
            type="button"
            class="rounded-xl border border-cyan-400 px-4 py-2 text-sm font-semibold text-cyan-300 transition hover:bg-cyan-400 hover:text-slate-950"
            @click="downloadImage"
          >
            Download
          </button>
        </div>

        <div class="mt-5 grid gap-5 lg:grid-cols-2">
          <div class="space-y-4">
            <div class="flex h-72 items-center justify-center overflow-hidden rounded-2xl border border-slate-800 bg-slate-950 p-4">
              <img
                v-if="previewUrl"
                :src="previewUrl"
                alt="Preview original"
                class="max-h-full max-w-full rounded-xl object-contain"
              />

              <p v-else class="text-center text-sm text-slate-500">
                Selecione uma imagem para visualizar.
              </p>
            </div>

            <div class="rounded-2xl border border-slate-800 bg-slate-950 p-4">
              <h4 class="text-sm font-semibold text-white">Imagem original</h4>

              <div v-if="file" class="mt-3 grid gap-2 text-sm text-slate-300">
                <p class="truncate"><span class="text-slate-500">Nome:</span> {{ file.name }}</p>
                <p><span class="text-slate-500">Tipo:</span> {{ file.type }}</p>
                <p><span class="text-slate-500">Tamanho:</span> {{ formatBytes(file.size) }}</p>
              </div>

              <p v-else class="mt-3 text-sm text-slate-500">
                Nenhuma imagem selecionada.
              </p>
            </div>
          </div>

          <div class="space-y-4">
            <div class="flex h-72 items-center justify-center overflow-hidden rounded-2xl border border-slate-800 bg-slate-950 p-4">
              <img
                v-if="generatedImageUrl"
                :src="generatedImageUrl"
                alt="Imagem gerada"
                class="max-h-full max-w-full rounded-xl object-contain"
              />

              <p v-else class="text-center text-sm text-slate-500">
                O resultado aparecerá aqui.
              </p>
            </div>

            <div class="rounded-2xl border border-slate-800 bg-slate-950 p-4">
              <h4 class="text-sm font-semibold text-white">Imagem gerada</h4>

              <div v-if="result" class="mt-3 grid gap-2 text-sm text-slate-300 sm:grid-cols-2">
                <p><span class="text-slate-500">Formato:</span> {{ result.output_format }}</p>
                <p><span class="text-slate-500">Tamanho:</span> {{ formatBytes(result.output_size_bytes) }}</p>
                <p><span class="text-slate-500">Dimensão:</span> {{ result.output_width }}x{{ result.output_height }}</p>
                <p><span class="text-slate-500">Original:</span> {{ result.original_width }}x{{ result.original_height }}</p>
              </div>

              <p v-else class="mt-3 text-sm text-slate-500">
                Nenhuma imagem processada.
              </p>
            </div>
          </div>
        </div>

        <div v-if="result" class="mt-5 rounded-2xl border border-cyan-400/20 bg-cyan-400/10 p-4">
          <p class="text-sm text-cyan-100">
            Arquivo pronto:
            <span class="font-mono text-cyan-300">{{ result.filename }}</span>
          </p>
        </div>
      </div>
    </div>
  </section>
</template>
