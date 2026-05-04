<script setup lang="ts">
import { ref } from 'vue'
import { api } from '../services/api'

const value = ref('')
const algorithm = ref('sha256')
const hash = ref('')
const error = ref('')
const copied = ref(false)
const loading = ref(false)

async function generateHash() {
  error.value = ''
  hash.value = ''
  copied.value = false
  loading.value = true

  try {
    const response = await api.post('/hash/generate', {
      value: value.value,
      algorithm: algorithm.value,
    })

    hash.value = response.data.hash
  } catch {
    error.value = 'Não foi possível gerar o hash.'
  } finally {
    loading.value = false
  }
}

async function copyHash() {
  if (!hash.value) return

  await navigator.clipboard.writeText(hash.value)
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
      <h2 class="mt-2 text-3xl font-bold text-white">Gerador de Hash</h2>
      <p class="mt-2 text-slate-400">
        Gere hashes para comparação, integridade de dados e checksums simples.
      </p>
    </div>

    <div class="grid gap-6 lg:grid-cols-[1fr_1.1fr]">
      <form class="space-y-5 rounded-lg border border-white/10 bg-white/[0.045] p-5" @submit.prevent="generateHash">
        <label class="block">
          <span class="text-sm font-medium text-slate-300">Texto de entrada</span>
          <textarea
            v-model="value"
            rows="8"
            placeholder="Digite o texto para gerar o hash"
            class="mt-2 w-full resize-y rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 text-white outline-none focus:border-teal-300"
          />
        </label>

        <label class="block">
          <span class="text-sm font-medium text-slate-300">Algoritmo</span>
          <select
            v-model="algorithm"
            class="mt-2 w-full rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 text-white outline-none focus:border-teal-300"
          >
            <option value="md5">MD5</option>
            <option value="sha1">SHA1</option>
            <option value="sha256">SHA256</option>
            <option value="sha512">SHA512</option>
          </select>
        </label>

        <button
          type="submit"
          class="w-full rounded-md bg-teal-300 px-5 py-3 font-semibold text-slate-950 transition hover:bg-teal-200 disabled:opacity-60"
          :disabled="loading"
        >
          {{ loading ? 'Gerando...' : 'Gerar hash' }}
        </button>

        <p class="rounded-md border border-amber-500/30 bg-amber-500/10 p-3 text-sm text-amber-200">
          MD5 e SHA1 são úteis para comparação simples, mas não devem ser usados como segurança de senhas.
        </p>

        <p v-if="error" class="rounded-md border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
          {{ error }}
        </p>
      </form>

      <div class="rounded-lg border border-white/10 bg-white/[0.045] p-5">
        <h3 class="text-lg font-semibold text-white">Resultado</h3>

        <div v-if="hash" class="mt-4 space-y-4">
          <div class="rounded-md border border-white/10 bg-[#0b1020] p-4">
            <p class="break-all font-mono text-sm text-teal-200">{{ hash }}</p>
          </div>

          <button
            type="button"
            class="rounded-md border border-teal-300 px-4 py-2 text-sm font-semibold text-teal-200 transition hover:bg-teal-300 hover:text-slate-950"
            @click="copyHash"
          >
            {{ copied ? 'Hash copiado!' : 'Copiar hash' }}
          </button>
        </div>

        <p v-else class="mt-4 text-sm leading-6 text-slate-400">
          Gere um hash para visualizar o resultado aqui.
        </p>
      </div>
    </div>
  </section>
</template>
