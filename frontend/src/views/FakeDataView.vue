<script setup lang="ts">
import { ref } from 'vue'
import { api } from '../services/api'

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
  <section class="mx-auto max-w-5xl space-y-6">
    <div>
      <h2 class="text-3xl font-bold text-white">Lorem Ipsum / Dados Fake</h2>
      <p class="mt-2 text-slate-400">
        Gere textos, nomes, emails, telefones e payloads fake para testes rápidos.
      </p>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <form class="min-h-[520px] space-y-5 rounded-2xl border border-slate-800 bg-slate-900 p-5" @submit.prevent="generateData">
        <div>
          <span class="text-sm font-medium text-slate-300">Tipo de dado</span>

          <div class="mt-2 grid grid-cols-2 gap-2 rounded-2xl border border-slate-800 bg-slate-950 p-2">
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
              class="rounded-xl px-3 py-3 text-sm font-semibold transition"
              :class="mode === option.key
                ? 'bg-cyan-400 text-slate-950'
                : 'text-slate-300 hover:bg-slate-900 hover:text-white'"
              @click="mode = option.key as FakeMode; result = ''"
            >
              {{ option.label }}
            </button>
          </div>
        </div>

        <label v-if="mode === 'lorem'" class="block">
          <span class="text-sm font-medium text-slate-300">Quantidade de parágrafos</span>

          <input
            v-model.number="paragraphs"
            type="number"
            min="1"
            max="10"
            class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
          />
        </label>

        <label v-else class="block">
          <span class="text-sm font-medium text-slate-300">Quantidade</span>

          <input
            v-model.number="quantity"
            type="number"
            min="1"
            max="50"
            class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
          />
        </label>

        <button
          type="submit"
          class="w-full rounded-xl bg-cyan-400 px-5 py-3 font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:opacity-60"
          :disabled="loading"
        >
          {{ loading ? 'Gerando...' : `Gerar ${modeLabel[mode]}` }}
        </button>

        <p v-if="error" class="rounded-xl border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
          {{ error }}
        </p>
      </form>

      <div class="min-h-[520px] rounded-2xl border border-slate-800 bg-slate-900 p-5">
        <h3 class="text-lg font-semibold text-white">Resultado</h3>

        <div v-if="result" class="mt-4 space-y-4">
          <pre class="max-h-[390px] overflow-auto rounded-xl border border-slate-800 bg-slate-950 p-4 whitespace-pre-wrap text-sm text-cyan-100">{{ result }}</pre>

          <button
            type="button"
            class="rounded-xl border border-cyan-400 px-4 py-2 text-sm font-semibold text-cyan-300 transition hover:bg-cyan-400 hover:text-slate-950"
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
