<script setup lang="ts">
import { ref } from 'vue'
import { api } from '../services/api'

type JsonAction = 'format' | 'validate' | 'minify'

const content = ref('')
const result = ref('')
const valid = ref<boolean | null>(null)
const error = ref('')
const copied = ref(false)
const loading = ref(false)

async function runAction(action: JsonAction) {
  error.value = ''
  result.value = ''
  valid.value = null
  copied.value = false
  loading.value = true

  try {
    const response = await api.post(`/json/${action}`, {
      content: content.value,
    })

    valid.value = response.data.valid

    if (response.data.result) {
      result.value = response.data.result
    } else if (response.data.valid) {
      result.value = 'JSON válido.'
    }

    if (response.data.error) {
      error.value = response.data.error
    }
  } catch {
    error.value = 'Não foi possível processar o JSON.'
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
  content.value = ''
  result.value = ''
  valid.value = null
  error.value = ''
}
</script>

<template>
  <section class="mx-auto max-w-5xl space-y-6">
    <div>
      <p class="text-sm font-semibold uppercase tracking-[0.3em] text-cyan-400">Dev Tools</p>
      <h2 class="mt-2 text-3xl font-bold text-white">JSON Tools</h2>
      <p class="mt-2 text-slate-400">
        Formate, valide ou minifique payloads JSON usados em APIs e integrações.
      </p>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <div class="rounded-2xl border border-slate-800 bg-slate-900 p-5">
        <label class="block">
          <span class="text-sm font-medium text-slate-300">JSON de entrada</span>
          <textarea
            v-model="content"
            rows="16"
            placeholder='{"name":"Gilvan","stack":["Vue","Python"]}'
            class="mt-2 w-full resize-y rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 font-mono text-sm text-white outline-none focus:border-cyan-400"
          />
        </label>

        <div class="mt-4 flex flex-wrap gap-3">
          <button
            type="button"
            class="rounded-xl bg-cyan-400 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-cyan-300 disabled:opacity-60"
            :disabled="loading"
            @click="runAction('format')"
          >
            Formatar
          </button>

          <button
            type="button"
            class="rounded-xl border border-slate-700 px-4 py-2 text-sm font-semibold text-slate-300 hover:border-cyan-400 hover:text-white"
            :disabled="loading"
            @click="runAction('validate')"
          >
            Validar
          </button>

          <button
            type="button"
            class="rounded-xl border border-slate-700 px-4 py-2 text-sm font-semibold text-slate-300 hover:border-cyan-400 hover:text-white"
            :disabled="loading"
            @click="runAction('minify')"
          >
            Minificar
          </button>

          <button
            type="button"
            class="rounded-xl border border-slate-700 px-4 py-2 text-sm font-semibold text-slate-300 hover:border-red-400 hover:text-red-300"
            @click="clearFields"
          >
            Limpar
          </button>
        </div>
      </div>

      <div class="rounded-2xl border border-slate-800 bg-slate-900 p-5">
        <h3 class="text-lg font-semibold text-white">Resultado</h3>

        <div v-if="valid !== null" class="mt-4">
          <p
            class="rounded-xl border p-3 text-sm"
            :class="valid ? 'border-emerald-500/30 bg-emerald-500/10 text-emerald-300' : 'border-red-500/30 bg-red-500/10 text-red-300'"
          >
            {{ valid ? 'JSON válido.' : 'JSON inválido.' }}
          </p>
        </div>

        <p v-if="error" class="mt-4 rounded-xl border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
          {{ error }}
        </p>

        <pre v-if="result" class="mt-4 max-h-[440px] overflow-auto rounded-xl border border-slate-800 bg-slate-950 p-4 text-sm text-cyan-100">{{ result }}</pre>

        <button
          v-if="result"
          type="button"
          class="mt-4 rounded-xl border border-cyan-400 px-4 py-2 text-sm font-semibold text-cyan-300 hover:bg-cyan-400 hover:text-slate-950"
          @click="copyResult"
        >
          {{ copied ? 'Copiado!' : 'Copiar resultado' }}
        </button>

        <p v-if="!result && !error" class="mt-4 text-sm leading-6 text-slate-400">
          O resultado aparecerá aqui.
        </p>
      </div>
    </div>
  </section>
</template>
