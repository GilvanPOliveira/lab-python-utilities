<script setup lang="ts">
import { computed, ref } from 'vue'
import { api } from '../services/api'

type DocumentType = 'cpf' | 'cnpj'

type DocumentResult = {
  valid: boolean
  value: string
  formatted: string | null
  digits: string
}

const documentType = ref<DocumentType>('cpf')
const value = ref('')
const result = ref<DocumentResult | null>(null)
const error = ref('')
const copiedFormatted = ref(false)
const copiedDigits = ref(false)
const loading = ref(false)

const validNumberToCopy = computed(() => {
  if (!result.value || !result.value.valid) return ''
  return result.value.formatted || result.value.digits
})

const validDigitsToCopy = computed(() => {
  if (!result.value || !result.value.valid) return ''
  return result.value.digits
})

async function validateDocument() {
  error.value = ''
  result.value = null
  copiedFormatted.value = false
  copiedDigits.value = false
  loading.value = true

  try {
    const endpoint = documentType.value === 'cpf'
      ? '/documents/validate-cpf'
      : '/documents/validate-cnpj'

    const response = await api.post(endpoint, {
      value: value.value,
    })

    result.value = response.data
  } catch {
    error.value = 'Não foi possível validar o documento.'
  } finally {
    loading.value = false
  }
}

async function copyValidatedNumber() {
  if (!validNumberToCopy.value) return

  await navigator.clipboard.writeText(validNumberToCopy.value)
  copiedFormatted.value = true

  window.setTimeout(() => {
    copiedFormatted.value = false
  }, 1800)
}

async function copyOnlyDigits() {
  if (!validDigitsToCopy.value) return

  await navigator.clipboard.writeText(validDigitsToCopy.value)
  copiedDigits.value = true

  window.setTimeout(() => {
    copiedDigits.value = false
  }, 1800)
}
</script>

<template>
  <section class="mx-auto max-w-5xl space-y-6">
    <div>
      <h2 class="text-3xl font-bold text-white">CPF/CNPJ</h2>
      <p class="mt-2 text-slate-400">
        Valide documentos brasileiros e copie o número formatado ou somente os dígitos.
      </p>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <form class="min-h-[430px] space-y-5 rounded-2xl border border-slate-800 bg-slate-900 p-5" @submit.prevent="validateDocument">
        <div>
          <span class="text-sm font-medium text-slate-300">Tipo de documento</span>

          <div class="mt-2 grid grid-cols-2 gap-3 rounded-2xl border border-slate-800 bg-slate-950 p-2">
            <button
              type="button"
              class="rounded-xl px-4 py-3 text-sm font-semibold transition"
              :class="documentType === 'cpf'
                ? 'bg-cyan-400 text-slate-950'
                : 'text-slate-300 hover:bg-slate-900 hover:text-white'"
              @click="documentType = 'cpf'"
            >
              CPF
            </button>

            <button
              type="button"
              class="rounded-xl px-4 py-3 text-sm font-semibold transition"
              :class="documentType === 'cnpj'
                ? 'bg-cyan-400 text-slate-950'
                : 'text-slate-300 hover:bg-slate-900 hover:text-white'"
              @click="documentType = 'cnpj'"
            >
              CNPJ
            </button>
          </div>
        </div>

        <label class="block">
          <span class="text-sm font-medium text-slate-300">Documento</span>
          <input
            v-model="value"
            type="text"
            placeholder="Digite com ou sem máscara"
            class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
          />
        </label>

        <button
          type="submit"
          class="w-full rounded-xl bg-cyan-400 px-5 py-3 font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-60"
          :disabled="loading"
        >
          {{ loading ? 'Validando...' : `Validar ${documentType.toUpperCase()}` }}
        </button>

        <p v-if="error" class="rounded-xl border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
          {{ error }}
        </p>
      </form>

      <div class="min-h-[430px] rounded-2xl border border-slate-800 bg-slate-900 p-5">
        <h3 class="text-lg font-semibold text-white">Resultado</h3>

        <div v-if="result" class="mt-4 space-y-4">
          <div
            class="rounded-xl border p-4"
            :class="result.valid ? 'border-emerald-500/30 bg-emerald-500/10' : 'border-red-500/30 bg-red-500/10'"
          >
            <p class="text-sm font-semibold" :class="result.valid ? 'text-emerald-300' : 'text-red-300'">
              {{ documentType.toUpperCase() }} {{ result.valid ? 'válido' : 'inválido' }}
            </p>

            <div class="mt-4 grid gap-3 text-sm text-slate-300">
              <p class="break-all">
                <span class="text-slate-500">Informado:</span>
                {{ result.value }}
              </p>

              <p class="break-all">
                <span class="text-slate-500">Formatado:</span>
                {{ result.formatted || 'Não disponível' }}
              </p>

              <p class="break-all">
                <span class="text-slate-500">Somente dígitos:</span>
                {{ result.digits }}
              </p>
            </div>
          </div>

          <div v-if="result.valid" class="flex flex-wrap gap-3">
            <button
              type="button"
              class="rounded-xl border border-cyan-400 px-4 py-2 text-sm font-semibold text-cyan-300 transition hover:bg-cyan-400 hover:text-slate-950"
              @click="copyValidatedNumber"
            >
              {{ copiedFormatted ? 'Formatado copiado!' : 'Copiar formatado' }}
            </button>

            <button
              type="button"
              class="rounded-xl border border-slate-700 px-4 py-2 text-sm font-semibold text-slate-300 transition hover:border-cyan-400 hover:text-cyan-300"
              @click="copyOnlyDigits"
            >
              {{ copiedDigits ? 'Dígitos copiados!' : 'Copiar somente dígitos' }}
            </button>
          </div>

          <p v-else class="text-sm text-slate-500">
            As opções de copiar aparecem apenas quando o documento é válido.
          </p>
        </div>

        <p v-else class="mt-4 text-sm leading-6 text-slate-400">
          Informe um CPF ou CNPJ para validar.
        </p>
      </div>
    </div>
  </section>
</template>
