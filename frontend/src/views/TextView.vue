<script setup lang="ts">
import { ref } from 'vue'
import { api } from '../services/api'

type TextCount = {
  characters: number
  characters_without_spaces: number
  words: number
  lines: number
}

const value = ref('')
const result = ref('')
const count = ref<TextCount | null>(null)
const error = ref('')
const copied = ref(false)
const loading = ref(false)

async function cleanText() {
  error.value = ''
  result.value = ''
  count.value = null
  copied.value = false
  loading.value = true

  try {
    const response = await api.post('/text/clean', {
      value: value.value,
    })

    result.value = response.data.cleaned
  } catch {
    error.value = 'Não foi possível limpar o texto.'
  } finally {
    loading.value = false
  }
}

async function convertText(mode: 'upper' | 'lower' | 'title' | 'capitalize') {
  error.value = ''
  result.value = ''
  count.value = null
  copied.value = false
  loading.value = true

  try {
    const response = await api.post('/text/convert', {
      value: value.value,
      mode,
    })

    result.value = response.data.converted
  } catch {
    error.value = 'Não foi possível converter o texto.'
  } finally {
    loading.value = false
  }
}

async function countText() {
  error.value = ''
  result.value = ''
  copied.value = false
  loading.value = true

  try {
    const response = await api.post('/text/count', {
      value: value.value,
    })

    count.value = response.data
  } catch {
    error.value = 'Não foi possível contar o texto.'
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

function clearFields() {
  value.value = ''
  result.value = ''
  count.value = null
  error.value = ''
  copied.value = false
}
</script>

<template>
  <section class="tool-page">
    <div>
      <h2 class="text-3xl font-bold text-white">Text Tools</h2>
      <p class="mt-2 text-slate-400">
        Limpe, converta e conte informações de texto.
      </p>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <div class="min-h-[var(--tool-panel-min-height)] space-y-5 rounded-lg border border-white/10 bg-white/[0.045] p-5">
        <label class="block">
          <span class="text-sm font-medium text-slate-300">Texto de entrada</span>
          <textarea
            v-model="value"
            class="mt-2 min-h-64 w-full resize-y rounded-md border border-white/10 bg-[#0b1020] p-4 text-slate-100 outline-none focus:border-teal-300"
            placeholder="Digite seu texto"
          />
        </label>

        <div class="flex flex-wrap justify-center gap-3">
          <button
            class="rounded-md bg-teal-300 px-5 py-3 font-semibold text-slate-950 transition hover:bg-teal-200 disabled:opacity-60"
            :disabled="loading"
            @click="cleanText"
          >
            Limpar
          </button>

          <button
            class="rounded-md border border-teal-300 px-5 py-3 font-semibold text-teal-200 transition hover:bg-teal-300 hover:text-slate-950 disabled:opacity-60"
            :disabled="loading"
            @click="convertText('upper')"
          >
            Maiúsculas
          </button>

          <button
            class="rounded-md border border-teal-300 px-5 py-3 font-semibold text-teal-200 transition hover:bg-teal-300 hover:text-slate-950 disabled:opacity-60"
            :disabled="loading"
            @click="convertText('lower')"
          >
            Minúsculas
          </button>

          <button
            class="rounded-md border border-teal-300 px-5 py-3 font-semibold text-teal-200 transition hover:bg-teal-300 hover:text-slate-950 disabled:opacity-60"
            :disabled="loading"
            @click="convertText('title')"
          >
            Title Case
          </button>

          <button
            class="rounded-md border border-white/10 px-5 py-3 font-semibold text-slate-300 transition hover:border-teal-300 hover:text-white disabled:opacity-60"
            :disabled="loading"
            @click="countText"
          >
            Contar
          </button>

          <button
            class="rounded-md border border-white/10 px-5 py-3 font-semibold text-slate-300 transition hover:border-red-400 hover:text-red-300"
            @click="clearFields"
          >
            Limpar campos
          </button>
        </div>

        <p v-if="error" class="rounded-md border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
          {{ error }}
        </p>
      </div>

      <div class="min-h-[var(--tool-panel-min-height)] rounded-lg border border-white/10 bg-white/[0.045] p-5">
        <h3 class="text-lg font-semibold text-white">Resultado</h3>

        <div v-if="result" class="mt-4 space-y-4">
          <div class="max-h-96 overflow-auto rounded-md border border-white/10 bg-[#0b1020] p-4">
            <p class="whitespace-pre-wrap break-words text-sm leading-6 text-teal-50">
              {{ result }}
            </p>
          </div>

          <button
            type="button"
            class="rounded-md border border-teal-300 px-4 py-2 text-sm font-semibold text-teal-200 transition hover:bg-teal-300 hover:text-slate-950"
            @click="copyResult"
          >
            {{ copied ? 'Resultado copiado!' : 'Copiar resultado' }}
          </button>
        </div>

        <div v-else-if="count" class="mt-4 grid gap-3 sm:grid-cols-2">
          <div class="rounded-md border border-white/10 bg-[#0b1020] p-4">
            <p class="text-xs text-slate-500">Caracteres</p>
            <p class="mt-1 text-2xl font-bold text-teal-200">{{ count.characters }}</p>
          </div>

          <div class="rounded-md border border-white/10 bg-[#0b1020] p-4">
            <p class="text-xs text-slate-500">Sem espaços</p>
            <p class="mt-1 text-2xl font-bold text-teal-200">{{ count.characters_without_spaces }}</p>
          </div>

          <div class="rounded-md border border-white/10 bg-[#0b1020] p-4">
            <p class="text-xs text-slate-500">Palavras</p>
            <p class="mt-1 text-2xl font-bold text-teal-200">{{ count.words }}</p>
          </div>

          <div class="rounded-md border border-white/10 bg-[#0b1020] p-4">
            <p class="text-xs text-slate-500">Linhas</p>
            <p class="mt-1 text-2xl font-bold text-teal-200">{{ count.lines }}</p>
          </div>
        </div>

        <p v-else class="mt-4 text-sm leading-6 text-slate-400">
          O resultado das ações aparecerá aqui.
        </p>
      </div>
    </div>
  </section>
</template>
