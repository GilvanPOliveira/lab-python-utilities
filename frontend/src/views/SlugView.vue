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
  <section class="tool-page">
    <div>
      <p class="text-sm font-semibold uppercase tracking-[0.3em] text-teal-300">Dev Tools</p>
      <h2 class="mt-2 text-3xl font-bold text-white">Gerador de Slug</h2>
      <p class="mt-2 text-slate-400">
        Transforme títulos e textos em slugs seguros para URLs, rotas, blogs e nomes de páginas.
      </p>
    </div>

    <div class="grid gap-6 lg:grid-cols-[1fr_1.1fr]">
      <form class="space-y-5 rounded-lg border border-white/10 bg-white/[0.045] p-5" @submit.prevent="generateSlug">
        <label class="block">
          <span class="text-sm font-medium text-slate-300">Texto original</span>
          <textarea
            v-model="value"
            rows="8"
            placeholder="Ex: Meu Novo Projeto Python Utilities"
            class="mt-2 w-full resize-y rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 text-white outline-none focus:border-teal-300"
          />
        </label>

        <button
          type="submit"
          class="w-full rounded-md bg-teal-300 px-5 py-3 font-semibold text-slate-950 transition hover:bg-teal-200 disabled:opacity-60"
          :disabled="loading"
        >
          {{ loading ? 'Gerando...' : 'Gerar slug' }}
        </button>

        <p v-if="error" class="rounded-md border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
          {{ error }}
        </p>
      </form>

      <div class="rounded-lg border border-white/10 bg-white/[0.045] p-5">
        <h3 class="text-lg font-semibold text-white">Resultado</h3>

        <div v-if="slug" class="mt-4 space-y-4">
          <div class="rounded-md border border-white/10 bg-[#0b1020] p-4">
            <p class="break-all font-mono text-lg text-teal-200">{{ slug }}</p>
          </div>

          <button
            type="button"
            class="rounded-md border border-teal-300 px-4 py-2 text-sm font-semibold text-teal-200 transition hover:bg-teal-300 hover:text-slate-950"
            @click="copySlug"
          >
            {{ copied ? 'Slug copiado!' : 'Copiar slug' }}
          </button>
        </div>

        <p v-else class="mt-4 text-sm leading-6 text-slate-400">
          Use esta ferramenta para criar URLs amigveis, nomes de rotas e identificadores limpos.
        </p>
      </div>
    </div>
  </section>
</template>
