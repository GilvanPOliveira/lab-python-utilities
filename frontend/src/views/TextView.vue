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
  <section class="mx-auto max-w-5xl space-y-6">
    <div>
      <h2 class="text-3xl font-bold text-white">Text Tools</h2>
      <p class="mt-2 text-slate-400">
        Limpe, converta e conte informações de texto.
      </p>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <div class="min-h-[520px] space-y-5 rounded-2xl border border-slate-800 bg-slate-900 p-5">
        <label class="block">
          <span class="text-sm font-medium text-slate-300">Texto de entrada</span>
          <textarea
            v-model="value"
            class="mt-2 min-h-64 w-full resize-y rounded-xl border border-slate-700 bg-slate-950 p-4 text-slate-100 outline-none focus:border-cyan-400"
            placeholder="Digite seu texto"
          />
        </label>

        <div class="flex flex-wrap justify-center gap-3">
          <button
            class="rounded-xl bg-cyan-400 px-5 py-3 font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:opacity-60"
            :disabled="loading"
            @click="cleanText"
          >
            Limpar
          </button>

          <button
            class="rounded-xl border border-cyan-400 px-5 py-3 font-semibold text-cyan-300 transition hover:bg-cyan-400 hover:text-slate-950 disabled:opacity-60"
            :disabled="loading"
            @click="convertText('upper')"
          >
            Maiúsculas
          </button>

          <button
            class="rounded-xl border border-cyan-400 px-5 py-3 font-semibold text-cyan-300 transition hover:bg-cyan-400 hover:text-slate-950 disabled:opacity-60"
            :disabled="loading"
            @click="convertText('lower')"
          >
            Minúsculas
          </button>

          <button
            class="rounded-xl border border-cyan-400 px-5 py-3 font-semibold text-cyan-300 transition hover:bg-cyan-400 hover:text-slate-950 disabled:opacity-60"
            :disabled="loading"
            @click="convertText('title')"
          >
            Title Case
          </button>

          <button
            class="rounded-xl border border-slate-700 px-5 py-3 font-semibold text-slate-300 transition hover:border-cyan-400 hover:text-white disabled:opacity-60"
            :disabled="loading"
            @click="countText"
          >
            Contar
          </button>

          <button
            class="rounded-xl border border-slate-700 px-5 py-3 font-semibold text-slate-300 transition hover:border-red-400 hover:text-red-300"
            @click="clearFields"
          >
            Limpar campos
          </button>
        </div>

        <p v-if="error" class="rounded-xl border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
          {{ error }}
        </p>
      </div>

      <div class="min-h-[520px] rounded-2xl border border-slate-800 bg-slate-900 p-5">
        <h3 class="text-lg font-semibold text-white">Resultado</h3>

        <div v-if="result" class="mt-4 space-y-4">
          <div class="max-h-96 overflow-auto rounded-xl border border-slate-800 bg-slate-950 p-4">
            <p class="whitespace-pre-wrap break-words text-sm leading-6 text-cyan-100">
              {{ result }}
            </p>
          </div>

          <button
            type="button"
            class="rounded-xl border border-cyan-400 px-4 py-2 text-sm font-semibold text-cyan-300 transition hover:bg-cyan-400 hover:text-slate-950"
            @click="copyResult"
          >
            {{ copied ? 'Resultado copiado!' : 'Copiar resultado' }}
          </button>
        </div>

        <div v-else-if="count" class="mt-4 grid gap-3 sm:grid-cols-2">
          <div class="rounded-xl border border-slate-800 bg-slate-950 p-4">
            <p class="text-xs text-slate-500">Caracteres</p>
            <p class="mt-1 text-2xl font-bold text-cyan-300">{{ count.characters }}</p>
          </div>

          <div class="rounded-xl border border-slate-800 bg-slate-950 p-4">
            <p class="text-xs text-slate-500">Sem espaços</p>
            <p class="mt-1 text-2xl font-bold text-cyan-300">{{ count.characters_without_spaces }}</p>
          </div>

          <div class="rounded-xl border border-slate-800 bg-slate-950 p-4">
            <p class="text-xs text-slate-500">Palavras</p>
            <p class="mt-1 text-2xl font-bold text-cyan-300">{{ count.words }}</p>
          </div>

          <div class="rounded-xl border border-slate-800 bg-slate-950 p-4">
            <p class="text-xs text-slate-500">Linhas</p>
            <p class="mt-1 text-2xl font-bold text-cyan-300">{{ count.lines }}</p>
          </div>
        </div>

        <p v-else class="mt-4 text-sm leading-6 text-slate-400">
          O resultado das ações aparecerá aqui.
        </p>
      </div>
    </div>
  </section>
</template>
