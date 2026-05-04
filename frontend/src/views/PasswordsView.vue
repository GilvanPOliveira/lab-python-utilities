<script setup lang="ts">
import { computed, ref } from 'vue'
import { api } from '../services/api'

const length = ref(16)
const includeUppercase = ref(true)
const includeLowercase = ref(true)
const includeNumbers = ref(true)
const includeSymbols = ref(true)

const password = ref('')
const error = ref('')
const copied = ref(false)
const loading = ref(false)

const strength = computed(() => {
  if (!password.value) return ''

  let score = 0

  if (password.value.length >= 12) score++
  if (/[A-Z]/.test(password.value)) score++
  if (/[a-z]/.test(password.value)) score++
  if (/[0-9]/.test(password.value)) score++
  if (/[^A-Za-z0-9]/.test(password.value)) score++

  if (score <= 2) return 'Fraca'
  if (score <= 4) return 'Boa'
  return 'Forte'
})

async function generatePassword() {
  error.value = ''
  copied.value = false
  loading.value = true

  try {
    const response = await api.post('/passwords/generate', {
      length: length.value,
      include_uppercase: includeUppercase.value,
      include_lowercase: includeLowercase.value,
      include_numbers: includeNumbers.value,
      include_symbols: includeSymbols.value,
    })

    password.value = response.data.password
  } catch {
    error.value = 'Não foi possível gerar a senha.'
  } finally {
    loading.value = false
  }
}

async function copyPassword() {
  if (!password.value) return

  await navigator.clipboard.writeText(password.value)
  copied.value = true

  window.setTimeout(() => {
    copied.value = false
  }, 1800)
}
</script>

<template>
  <section class="tool-page">
    <div>
      <h2 class="text-3xl font-bold text-white">Gerador de Senhas</h2>
      <p class="mt-2 text-slate-400">
        Crie senhas fortes, escolha a quantidade de caracteres e copie o resultado.
      </p>
    </div>

    <div class="grid gap-6 lg:grid-cols-[1fr_1.1fr]">
      <form class="space-y-5 rounded-lg border border-white/10 bg-white/[0.045] p-5" @submit.prevent="generatePassword">
        <div class="rounded-lg border border-white/10 bg-[#0b1020] p-4">
          <div class="flex items-center justify-between gap-4">
            <div>
              <span class="text-sm font-medium text-slate-300">Quantidade de caracteres</span>
              <p class="mt-1 text-xs text-slate-500">Escolha entre 6 e 128 caracteres.</p>
            </div>

            <div class="flex h-14 w-16 items-center justify-center rounded-lg border border-teal-300/40 bg-teal-300/10">
              <span class="text-xl font-bold text-teal-200">{{ length }}</span>
            </div>
          </div>

          <input
            v-model.number="length"
            type="range"
            min="6"
            max="128"
            class="mt-5 w-full accent-teal-300"
          />

          <div class="mt-3 flex justify-between text-xs text-slate-500">
            <span>6</span>
            <span>128</span>
          </div>
        </div>

        <div class="grid gap-3 sm:grid-cols-2">
          <label class="flex items-center gap-3 rounded-md border border-white/10 bg-[#0b1020] p-3 text-sm text-slate-300">
            <input v-model="includeUppercase" type="checkbox" class="h-4 w-4 accent-teal-300" />
            Maiúsculas
          </label>

          <label class="flex items-center gap-3 rounded-md border border-white/10 bg-[#0b1020] p-3 text-sm text-slate-300">
            <input v-model="includeLowercase" type="checkbox" class="h-4 w-4 accent-teal-300" />
            Minúsculas
          </label>

          <label class="flex items-center gap-3 rounded-md border border-white/10 bg-[#0b1020] p-3 text-sm text-slate-300">
            <input v-model="includeNumbers" type="checkbox" class="h-4 w-4 accent-teal-300" />
            Números
          </label>

          <label class="flex items-center gap-3 rounded-md border border-white/10 bg-[#0b1020] p-3 text-sm text-slate-300">
            <input v-model="includeSymbols" type="checkbox" class="h-4 w-4 accent-teal-300" />
            Símbolos
          </label>
        </div>

        <button
          type="submit"
          class="w-full rounded-md bg-teal-300 px-5 py-3 font-semibold text-slate-950 transition hover:bg-teal-200 disabled:cursor-not-allowed disabled:opacity-60"
          :disabled="loading"
        >
          {{ loading ? 'Gerando...' : 'Gerar senha' }}
        </button>

        <p v-if="error" class="rounded-md border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
          {{ error }}
        </p>
      </form>

      <div class="rounded-lg border border-white/10 bg-white/[0.045] p-5">
        <h3 class="text-lg font-semibold text-white">Resultado</h3>

        <div v-if="password" class="mt-4 space-y-4">
          <div class="rounded-md border border-white/10 bg-[#0b1020] p-4">
            <p class="break-all font-mono text-lg text-teal-200">{{ password }}</p>
          </div>

          <div class="flex flex-wrap items-center gap-3">
            <button
              type="button"
              class="rounded-md border border-teal-300 px-4 py-2 text-sm font-semibold text-teal-200 transition hover:bg-teal-300 hover:text-slate-950"
              @click="copyPassword"
            >
              {{ copied ? 'Copiada!' : 'Copiar senha' }}
            </button>

            <span class="rounded-full border border-white/10 px-3 py-1 text-sm text-slate-300">
              Força: {{ strength }}
            </span>

            <span class="rounded-full border border-white/10 px-3 py-1 text-sm text-slate-300">
              {{ password.length }} caracteres
            </span>
          </div>
        </div>

        <p v-else class="mt-4 text-sm leading-6 text-slate-400">
          Gere uma senha para visualizar o resultado aqui.
        </p>
      </div>
    </div>
  </section>
</template>
