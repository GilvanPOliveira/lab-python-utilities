<script setup lang="ts">
import { ref } from 'vue'
import { api } from '../services/api'

const data = ref('')
const imageBase64 = ref('')
const loading = ref(false)
const error = ref('')

async function generateQrCode() {
  loading.value = true
  error.value = ''
  imageBase64.value = ''

  try {
    const response = await api.post('/qrcode/generate', {
      data: data.value,
      box_size: 10,
      border: 4,
    })

    imageBase64.value = response.data.image_base64
  } catch {
    error.value = 'Não foi possível gerar o QR Code.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="mx-auto max-w-3xl space-y-6">
    <div>
      <h2 class="text-3xl font-bold text-white">Gerador de QR Code</h2>
      <p class="mt-2 text-slate-400">Informe um texto ou URL para gerar um QR Code em PNG.</p>
    </div>

    <form class="space-y-4 rounded-2xl border border-slate-800 bg-slate-900 p-5" @submit.prevent="generateQrCode">
      <textarea
        v-model="data"
        class="min-h-32 w-full rounded-xl border border-slate-700 bg-slate-950 p-4 text-slate-100 outline-none focus:border-cyan-400"
        placeholder="Digite uma URL ou texto"
      />

      <button
        class="rounded-xl bg-cyan-400 px-5 py-3 font-semibold text-slate-950 disabled:opacity-60"
        :disabled="loading || !data.trim()"
      >
        {{ loading ? 'Gerando...' : 'Gerar QR Code' }}
      </button>

      <p v-if="error" class="text-sm text-red-400">{{ error }}</p>
    </form>

    <div v-if="imageBase64" class="rounded-2xl border border-slate-800 bg-slate-900 p-5">
      <img
        :src="`data:image/png;base64,${imageBase64}`"
        alt="QR Code gerado"
        class="mx-auto h-64 w-64 rounded-xl bg-white p-3"
      />

      <a
        :href="`data:image/png;base64,${imageBase64}`"
        download="qrcode.png"
        class="mt-5 inline-flex rounded-xl border border-cyan-400 px-5 py-3 font-semibold text-cyan-300 hover:bg-cyan-400 hover:text-slate-950"
      >
        Baixar QR Code
      </a>
    </div>
  </section>
</template>
