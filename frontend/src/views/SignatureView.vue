<script setup lang="ts">
import { ref } from 'vue'
import { api } from '../services/api'

const fullName = ref('')
const role = ref('')
const email = ref('')
const phone = ref('')
const website = ref('')
const github = ref('')
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
  <section class="tool-page">
    <div>
      <h2 class="text-3xl font-bold text-white">Gerador de Assinatura de Email</h2>
      <p class="mt-2 text-slate-400">
        Gere uma assinatura simples em HTML e texto para usar em emails profissionais.
      </p>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <form class="min-h-[var(--tool-panel-min-height)] space-y-4 rounded-lg border border-white/10 bg-white/[0.045] p-5" @submit.prevent="generateSignature">
        <div class="grid gap-4 sm:grid-cols-2">
          <label class="block">
            <span class="text-sm font-medium text-slate-300">Nome</span>
            <input v-model="fullName" type="text" class="mt-2 w-full rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 text-white outline-none focus:border-teal-300" />
          </label>

          <label class="block">
            <span class="text-sm font-medium text-slate-300">Cargo</span>
            <input v-model="role" type="text" class="mt-2 w-full rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 text-white outline-none focus:border-teal-300" />
          </label>
        </div>

        <div class="grid gap-4 sm:grid-cols-2">
          <label class="block">
            <span class="text-sm font-medium text-slate-300">Email</span>
            <input v-model="email" type="email" class="mt-2 w-full rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 text-white outline-none focus:border-teal-300" />
          </label>

          <label class="block">
            <span class="text-sm font-medium text-slate-300">Telefone</span>
            <input v-model="phone" type="text" class="mt-2 w-full rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 text-white outline-none focus:border-teal-300" />
          </label>
        </div>

        <label class="block">
          <span class="text-sm font-medium text-slate-300">Site</span>
          <input v-model="website" type="url" class="mt-2 w-full rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 text-white outline-none focus:border-teal-300" />
        </label>

        <label class="block">
          <span class="text-sm font-medium text-slate-300">GitHub</span>
          <input v-model="github" type="url" class="mt-2 w-full rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 text-white outline-none focus:border-teal-300" />
        </label>

        <label class="block">
          <span class="text-sm font-medium text-slate-300">LinkedIn</span>
          <input v-model="linkedin" type="url" class="mt-2 w-full rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 text-white outline-none focus:border-teal-300" />
        </label>

        <button
          type="submit"
          class="w-full rounded-md bg-teal-300 px-5 py-3 font-semibold text-slate-950 transition hover:bg-teal-200 disabled:opacity-60"
          :disabled="loading"
        >
          {{ loading ? 'Gerando...' : 'Gerar assinatura' }}
        </button>

        <p v-if="error" class="rounded-md border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
          {{ error }}
        </p>
      </form>

      <div class="min-h-[var(--tool-panel-min-height)] rounded-lg border border-white/10 bg-white/[0.045] p-5">
        <h3 class="text-lg font-semibold text-white">Resultado</h3>

        <div v-if="result" class="mt-4 space-y-5">
          <div class="rounded-lg border border-white/10 bg-white p-5 text-slate-900">
            <div v-html="result.html" />
          </div>

          <div class="grid gap-3 sm:grid-cols-2">
            <button
              type="button"
              class="rounded-md border border-teal-300 px-4 py-2 text-sm font-semibold text-teal-200 transition hover:bg-teal-300 hover:text-slate-950"
              @click="copyText(result.html, 'html')"
            >
              {{ copied === 'html' ? 'HTML copiado!' : 'Copiar HTML' }}
            </button>

            <button
              type="button"
              class="rounded-md border border-white/10 px-4 py-2 text-sm font-semibold text-slate-300 transition hover:border-teal-300 hover:text-teal-200"
              @click="copyText(result.plain_text, 'text')"
            >
              {{ copied === 'text' ? 'Texto copiado!' : 'Copiar texto' }}
            </button>
          </div>

          <pre class="max-h-64 overflow-auto rounded-md border border-white/10 bg-[#0b1020] p-4 text-xs text-teal-50">{{ result.html }}</pre>
        </div>

        <p v-else class="mt-4 text-sm leading-6 text-slate-400">
          Preencha os dados e gere uma assinatura.
        </p>
      </div>
    </div>
  </section>
</template>
