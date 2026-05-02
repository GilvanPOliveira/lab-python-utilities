<script setup lang="ts">
import { ref } from 'vue'
import { api } from '../services/api'

const fullName = ref('Gilvan Oliveira')
const role = ref('Desenvolvedor Full Stack')
const email = ref('')
const phone = ref('')
const website = ref('')
const github = ref('https://github.com/gilvanpoliveira')
const linkedin = ref('')

const result = ref<any | null>(null)
const error = ref('')
const copied = ref('')
const loading = ref(false)

async function generateSignature() {
  error.value = ''
  result.value = null
  copied.value = ''
  loading.value = true

  try {
    const response = await api.post('/signatures/email', {
      full_name: fullName.value,
      role: role.value,
      email: email.value,
      phone: phone.value,
      website: website.value,
      github: github.value,
      linkedin: linkedin.value,
    })

    result.value = response.data
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Não foi possível gerar a assinatura.'
  } finally {
    loading.value = false
  }
}

async function copyText(value: string, key: string) {
  if (!value) return

  await navigator.clipboard.writeText(value)
  copied.value = key

  window.setTimeout(() => {
    copied.value = ''
  }, 1800)
}
</script>

<template>
  <section class="mx-auto max-w-6xl space-y-6">
    <div>
      <h2 class="text-3xl font-bold text-white">Gerador de Assinatura de Email</h2>
      <p class="mt-2 text-slate-400">
        Gere uma assinatura simples em HTML e texto para usar em emails profissionais.
      </p>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <form class="min-h-[620px] space-y-4 rounded-2xl border border-slate-800 bg-slate-900 p-5" @submit.prevent="generateSignature">
        <div class="grid gap-4 sm:grid-cols-2">
          <label class="block">
            <span class="text-sm font-medium text-slate-300">Nome</span>
            <input v-model="fullName" type="text" class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400" />
          </label>

          <label class="block">
            <span class="text-sm font-medium text-slate-300">Cargo</span>
            <input v-model="role" type="text" class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400" />
          </label>
        </div>

        <div class="grid gap-4 sm:grid-cols-2">
          <label class="block">
            <span class="text-sm font-medium text-slate-300">Email</span>
            <input v-model="email" type="email" class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400" />
          </label>

          <label class="block">
            <span class="text-sm font-medium text-slate-300">Telefone</span>
            <input v-model="phone" type="text" class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400" />
          </label>
        </div>

        <label class="block">
          <span class="text-sm font-medium text-slate-300">Site</span>
          <input v-model="website" type="url" class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400" />
        </label>

        <label class="block">
          <span class="text-sm font-medium text-slate-300">GitHub</span>
          <input v-model="github" type="url" class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400" />
        </label>

        <label class="block">
          <span class="text-sm font-medium text-slate-300">LinkedIn</span>
          <input v-model="linkedin" type="url" class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400" />
        </label>

        <button
          type="submit"
          class="w-full rounded-xl bg-cyan-400 px-5 py-3 font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:opacity-60"
          :disabled="loading"
        >
          {{ loading ? 'Gerando...' : 'Gerar assinatura' }}
        </button>

        <p v-if="error" class="rounded-xl border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
          {{ error }}
        </p>
      </form>

      <div class="min-h-[620px] rounded-2xl border border-slate-800 bg-slate-900 p-5">
        <h3 class="text-lg font-semibold text-white">Resultado</h3>

        <div v-if="result" class="mt-4 space-y-5">
          <div class="rounded-2xl border border-slate-800 bg-white p-5 text-slate-900">
            <div v-html="result.html" />
          </div>

          <div class="grid gap-3 sm:grid-cols-2">
            <button
              type="button"
              class="rounded-xl border border-cyan-400 px-4 py-2 text-sm font-semibold text-cyan-300 transition hover:bg-cyan-400 hover:text-slate-950"
              @click="copyText(result.html, 'html')"
            >
              {{ copied === 'html' ? 'HTML copiado!' : 'Copiar HTML' }}
            </button>

            <button
              type="button"
              class="rounded-xl border border-slate-700 px-4 py-2 text-sm font-semibold text-slate-300 transition hover:border-cyan-400 hover:text-cyan-300"
              @click="copyText(result.plain_text, 'text')"
            >
              {{ copied === 'text' ? 'Texto copiado!' : 'Copiar texto' }}
            </button>
          </div>

          <pre class="max-h-64 overflow-auto rounded-xl border border-slate-800 bg-slate-950 p-4 text-xs text-cyan-100">{{ result.html }}</pre>
        </div>

        <p v-else class="mt-4 text-sm leading-6 text-slate-400">
          Preencha os dados e gere uma assinatura.
        </p>
      </div>
    </div>
  </section>
</template>
