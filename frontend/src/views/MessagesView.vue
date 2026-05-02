<script setup lang="ts">
import { ref } from 'vue'
import { api } from '../services/api'

type MessageType = 'recruiter' | 'follow_up' | 'thank_you' | 'linkedin' | 'short_reply'

const messageType = ref<MessageType>('recruiter')
const tone = ref('profissional')
const recipientName = ref('')
const context = ref('')
const objective = ref('')

const result = ref<any | null>(null)
const error = ref('')
const copied = ref(false)
const loading = ref(false)

async function generateMessage() {
  error.value = ''
  result.value = null
  copied.value = false
  loading.value = true

  try {
    const response = await api.post('/messages/quick', {
      message_type: messageType.value,
      tone: tone.value,
      recipient_name: recipientName.value,
      context: context.value,
      objective: objective.value,
    })

    result.value = response.data
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Não foi possível gerar a mensagem.'
  } finally {
    loading.value = false
  }
}

async function copyMessage() {
  if (!result.value?.message) return

  await navigator.clipboard.writeText(result.value.message)
  copied.value = true

  window.setTimeout(() => {
    copied.value = false
  }, 1800)
}
</script>

<template>
  <section class="mx-auto max-w-5xl space-y-6">
    <div>
      <h2 class="text-3xl font-bold text-white">Gerador de Mensagem Rápida</h2>
      <p class="mt-2 text-slate-400">
        Gere mensagens rápidas para recrutadores, LinkedIn, follow-up, agradecimentos e respostas curtas.
      </p>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <form class="min-h-[620px] space-y-5 rounded-2xl border border-slate-800 bg-slate-900 p-5" @submit.prevent="generateMessage">
        <div>
          <span class="text-sm font-medium text-slate-300">Tipo de mensagem</span>

          <div class="mt-2 grid grid-cols-2 gap-2 rounded-2xl border border-slate-800 bg-slate-950 p-2">
            <button
              v-for="option in [
                { key: 'recruiter', label: 'Recrutador' },
                { key: 'follow_up', label: 'Follow-up' },
                { key: 'thank_you', label: 'Agradecimento' },
                { key: 'linkedin', label: 'LinkedIn' },
                { key: 'short_reply', label: 'Resposta curta' },
              ]"
              :key="option.key"
              type="button"
              class="rounded-xl px-3 py-3 text-sm font-semibold transition"
              :class="messageType === option.key
                ? 'bg-cyan-400 text-slate-950'
                : 'text-slate-300 hover:bg-slate-900 hover:text-white'"
              @click="messageType = option.key as MessageType; result = null"
            >
              {{ option.label }}
            </button>
          </div>
        </div>

        <label class="block">
          <span class="text-sm font-medium text-slate-300">Tom</span>
          <select
            v-model="tone"
            class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
          >
            <option value="profissional">Profissional</option>
            <option value="amigavel">Amigável</option>
            <option value="direto">Direto</option>
            <option value="formal">Formal</option>
          </select>
        </label>

        <label class="block">
          <span class="text-sm font-medium text-slate-300">Nome do destinatário</span>
          <input
            v-model="recipientName"
            type="text"
            placeholder="Opcional"
            class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
          />
        </label>

        <label class="block">
          <span class="text-sm font-medium text-slate-300">Contexto</span>
          <textarea
            v-model="context"
            rows="5"
            placeholder="Ex: Vi sua publicação sobre vagas para desenvolvedor..."
            class="mt-2 w-full resize-none rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
          />
        </label>

        <label class="block">
          <span class="text-sm font-medium text-slate-300">Objetivo</span>
          <textarea
            v-model="objective"
            rows="4"
            placeholder="Ex: Gostaria de me candidatar ou conversar sobre a oportunidade..."
            class="mt-2 w-full resize-none rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
          />
        </label>

        <button
          type="submit"
          class="w-full rounded-xl bg-cyan-400 px-5 py-3 font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:opacity-60"
          :disabled="loading"
        >
          {{ loading ? 'Gerando...' : 'Gerar mensagem' }}
        </button>

        <p v-if="error" class="rounded-xl border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
          {{ error }}
        </p>
      </form>

      <div class="min-h-[620px] rounded-2xl border border-slate-800 bg-slate-900 p-5">
        <h3 class="text-lg font-semibold text-white">Resultado</h3>

        <div v-if="result" class="mt-4 space-y-4">
          <div class="rounded-xl border border-slate-800 bg-slate-950 p-4">
            <p class="text-sm text-slate-500">{{ result.title }}</p>
            <p class="mt-4 whitespace-pre-wrap text-sm leading-7 text-cyan-100">
              {{ result.message }}
            </p>
          </div>

          <button
            type="button"
            class="rounded-xl border border-cyan-400 px-4 py-2 text-sm font-semibold text-cyan-300 transition hover:bg-cyan-400 hover:text-slate-950"
            @click="copyMessage"
          >
            {{ copied ? 'Mensagem copiada!' : 'Copiar mensagem' }}
          </button>
        </div>

        <p v-else class="mt-4 text-sm leading-6 text-slate-400">
          Preencha os campos e gere uma mensagem rápida.
        </p>
      </div>
    </div>
  </section>
</template>
