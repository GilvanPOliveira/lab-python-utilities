<script setup lang="ts">
import { ref } from 'vue'
import { api } from '../services/api'
import BaseNumberInput from '../components/BaseNumberInput.vue'

type FakeMode = 'lorem' | 'names' | 'emails' | 'phones' | 'json'

const mode = ref<FakeMode>('lorem')
const quantity = ref(5)
const paragraphs = ref(2)
const result = ref('')
const error = ref('')
const copied = ref(false)
const loading = ref(false)

const modeLabel = {
  lorem: 'Lorem Ipsum',
  names: 'Nomes',
  emails: 'Emails',
  phones: 'Telefones',
  json: 'JSON fake',
}

async function generateData() {
  error.value = ''
  result.value = ''
  copied.value = false
  loading.value = true

  try {
    if (mode.value === 'lorem') {
      const response = await api.post('/fake-data/lorem', {
        paragraphs: paragraphs.value,
      })

      result.value = response.data.result
      return
    }

    const response = await api.post(`/fake-data/${mode.value}`, {
      quantity: quantity.value,
    })

    result.value = response.data.result
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Não foi possível gerar os dados.'
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
</script>

<template>
  <section class="tool-page">
    <div>
      <h2 class="text-3xl font-bold text-white">Lorem Ipsum / Dados Fake</h2>
      <p class="mt-2 text-slate-400">
        Gere textos, nomes, emails, telefones e payloads fake para testes rpidos.
      </p>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <form class="min-h-[var(--tool-panel-min-height)] space-y-5 rounded-lg border border-white/10 bg-white/[0.045] p-5" @submit.prevent="generateData">
        <div>
          <span class="text-sm font-medium text-slate-300">Tipo de dado</span>

          <div class="mt-2 grid grid-cols-2 gap-2 rounded-lg border border-white/10 bg-[#0b1020] p-2">
            <button
              v-for="option in [
                { key: 'lorem', label: 'Lorem' },
                { key: 'names', label: 'Nomes' },
                { key: 'emails', label: 'Emails' },
                { key: 'phones', label: 'Telefones' },
                { key: 'json', label: 'JSON' },
              ]"
              :key="option.key"
              type="button"
              class="rounded-md px-3 py-3 text-sm font-semibold transition"
              :class="mode === option.key
                ? 'bg-teal-300 text-slate-950'
                : 'text-slate-300 hover:bg-white/[0.045] hover:text-white'"
              @click="mode = option.key as FakeMode; result = ''"
            >
              {{ option.label }}
            </button>
          </div>
        </div>

        <BaseNumberInput
          v-if="mode === 'lorem'"
          v-model="paragraphs"
          label="Quantidade de paragrafos"
          :min="1"
          :max="10"
          :step="1"
        />

        <BaseNumberInput
          v-else
          v-model="quantity"
          label="Quantidade"
          :min="1"
          :max="50"
          :step="1"
        />

        <button
          type="submit"
          class="w-full rounded-md bg-teal-300 px-5 py-3 font-semibold text-slate-950 transition hover:bg-teal-200 disabled:opacity-60"
          :disabled="loading"
        >
          {{ loading ? 'Gerando...' : `Gerar ${modeLabel[mode]}` }}
        </button>

        <p v-if="error" class="rounded-md border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
          {{ error }}
        </p>
      </form>

      <div class="min-h-[var(--tool-panel-min-height)] rounded-lg border border-white/10 bg-white/[0.045] p-5">
        <h3 class="text-lg font-semibold text-white">Resultado</h3>

        <div v-if="result" class="mt-4 space-y-4">
          <pre class="max-h-[390px] overflow-auto rounded-md border border-white/10 bg-[#0b1020] p-4 whitespace-pre-wrap text-sm text-teal-50">{{ result }}</pre>

          <button
            type="button"
            class="rounded-md border border-teal-300 px-4 py-2 text-sm font-semibold text-teal-200 transition hover:bg-teal-300 hover:text-slate-950"
            @click="copyResult"
          >
            {{ copied ? 'Copiado!' : 'Copiar resultado' }}
          </button>
        </div>

        <p v-else class="mt-4 text-sm leading-6 text-slate-400">
          O resultado aparecerá aqui.
        </p>
      </div>
    </div>
  </section>
</template>
