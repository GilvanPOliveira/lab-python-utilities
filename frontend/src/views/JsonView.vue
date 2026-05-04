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
  <section class="tool-page">
    <div>
      <p class="text-sm font-semibold uppercase tracking-[0.3em] text-teal-300">Dev Tools</p>
      <h2 class="mt-2 text-3xl font-bold text-white">JSON Tools</h2>
      <p class="mt-2 text-slate-400">
        Formate, valide ou minifique payloads JSON usados em APIs e integrações.
      </p>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <div class="rounded-lg border border-white/10 bg-white/[0.045] p-5">
        <label class="block">
          <span class="text-sm font-medium text-slate-300">JSON de entrada</span>
          <textarea
            v-model="content"
            rows="16"
            placeholder='{"name":"Alex Demo","stack":["Vue","Python"]}'
            class="mt-2 w-full resize-y rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 font-mono text-sm text-white outline-none focus:border-teal-300"
          />
        </label>

        <div class="mt-4 flex flex-wrap gap-3">
          <button
            type="button"
            class="rounded-md bg-teal-300 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-teal-200 disabled:opacity-60"
            :disabled="loading"
            @click="runAction('format')"
          >
            Formatar
          </button>

          <button
            type="button"
            class="rounded-md border border-white/10 px-4 py-2 text-sm font-semibold text-slate-300 hover:border-teal-300 hover:text-white"
            :disabled="loading"
            @click="runAction('validate')"
          >
            Validar
          </button>

          <button
            type="button"
            class="rounded-md border border-white/10 px-4 py-2 text-sm font-semibold text-slate-300 hover:border-teal-300 hover:text-white"
            :disabled="loading"
            @click="runAction('minify')"
          >
            Minificar
          </button>

          <button
            type="button"
            class="rounded-md border border-white/10 px-4 py-2 text-sm font-semibold text-slate-300 hover:border-red-400 hover:text-red-300"
            @click="clearFields"
          >
            Limpar
          </button>
        </div>
      </div>

      <div class="rounded-lg border border-white/10 bg-white/[0.045] p-5">
        <h3 class="text-lg font-semibold text-white">Resultado</h3>

        <div v-if="valid !== null" class="mt-4">
          <p
            class="rounded-md border p-3 text-sm"
            :class="valid ? 'border-emerald-500/30 bg-emerald-500/10 text-emerald-300' : 'border-red-500/30 bg-red-500/10 text-red-300'"
          >
            {{ valid ? 'JSON válido.' : 'JSON inválido.' }}
          </p>
        </div>

        <p v-if="error" class="mt-4 rounded-md border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
          {{ error }}
        </p>

        <pre v-if="result" class="mt-4 max-h-[440px] overflow-auto rounded-md border border-white/10 bg-[#0b1020] p-4 text-sm text-teal-50">{{ result }}</pre>

        <button
          v-if="result"
          type="button"
          class="mt-4 rounded-md border border-teal-300 px-4 py-2 text-sm font-semibold text-teal-200 hover:bg-teal-300 hover:text-slate-950"
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
