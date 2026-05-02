<script setup lang="ts">
import { ref } from 'vue'
import { api } from '../services/api'

const value = ref('')
const slug = ref('')
const error = ref('')
const copied = ref(false)
const loading = ref(false)

async function generateSlug() {
  error.value = ''
  slug.value = ''
  copied.value = false
  loading.value = true

  try {
    const response = await api.post('/slug/generate', {
      value: value.value,
    })

    slug.value = response.data.slug
  } catch {
    error.value = 'Não foi possível gerar o slug.'
  } finally {
    loading.value = false
  }
}

async function copySlug() {
  if (!slug.value) return

  await navigator.clipboard.writeText(slug.value)
  copied.value = true

  window.setTimeout(() => {
    copied.value = false
  }, 1800)
}
</script>

<template>
  <section class="mx-auto max-w-4xl space-y-6">
    <div>
      <p class="text-sm font-semibold uppercase tracking-[0.3em] text-cyan-400">Dev Tools</p>
      <h2 class="mt-2 text-3xl font-bold text-white">Gerador de Slug</h2>
      <p class="mt-2 text-slate-400">
        Transforme títulos e textos em slugs seguros para URLs, rotas, blogs e nomes de páginas.
      </p>
    </div>

    <div class="grid gap-6 lg:grid-cols-[1fr_1.1fr]">
      <form class="space-y-5 rounded-2xl border border-slate-800 bg-slate-900 p-5" @submit.prevent="generateSlug">
        <label class="block">
          <span class="text-sm font-medium text-slate-300">Texto original</span>
          <textarea
            v-model="value"
            rows="8"
            placeholder="Ex: Meu Novo Projeto Python Utilities"
            class="mt-2 w-full resize-y rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
          />
        </label>

        <button
          type="submit"
          class="w-full rounded-xl bg-cyan-400 px-5 py-3 font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:opacity-60"
          :disabled="loading"
        >
          {{ loading ? 'Gerando...' : 'Gerar slug' }}
        </button>

        <p v-if="error" class="rounded-xl border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
          {{ error }}
        </p>
      </form>

      <div class="rounded-2xl border border-slate-800 bg-slate-900 p-5">
        <h3 class="text-lg font-semibold text-white">Resultado</h3>

        <div v-if="slug" class="mt-4 space-y-4">
          <div class="rounded-xl border border-slate-800 bg-slate-950 p-4">
            <p class="break-all font-mono text-lg text-cyan-300">{{ slug }}</p>
          </div>

          <button
            type="button"
            class="rounded-xl border border-cyan-400 px-4 py-2 text-sm font-semibold text-cyan-300 transition hover:bg-cyan-400 hover:text-slate-950"
            @click="copySlug"
          >
            {{ copied ? 'Slug copiado!' : 'Copiar slug' }}
          </button>
        </div>

        <p v-else class="mt-4 text-sm leading-6 text-slate-400">
          Use esta ferramenta para criar URLs amigáveis, nomes de rotas e identificadores limpos.
        </p>
      </div>
    </div>
  </section>
</template>
