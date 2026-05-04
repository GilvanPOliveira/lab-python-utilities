<script setup lang="ts">
import { computed, ref } from 'vue'
import { api } from '../services/api'
import BaseNumberInput from '../components/BaseNumberInput.vue'

type DateAction = 'format' | 'difference' | 'add'

const action = ref<DateAction>('format')
const mainDate = ref('')
const secondDate = ref('')
const outputFormat = ref('br')
const operation = ref<'add' | 'subtract'>('add')
const days = ref(0)
const months = ref(0)
const years = ref(0)

const result = ref<any | null>(null)
const error = ref('')
const copied = ref(false)
const loading = ref(false)

const actionTitle = computed(() => {
  const titles = {
    format: 'Formatar data',
    difference: 'Diferença entre datas',
    add: 'Somar ou subtrair tempo',
  }

  return titles[action.value]
})

const resultToCopy = computed(() => {
  if (!result.value) return ''

  if (action.value === 'format') {
    return result.value.formatted
  }

  if (action.value === 'difference') {
    return `${result.value.absolute_days} dias`
  }

  return result.value.result
})

function resetResult() {
  result.value = null
  error.value = ''
  copied.value = false
}

async function calculate() {
  resetResult()
  loading.value = true

  try {
    if (action.value === 'format') {
      const response = await api.post('/dates/format', {
        value: mainDate.value,
        output_format: outputFormat.value,
      })

      result.value = response.data
      return
    }

    if (action.value === 'difference') {
      const response = await api.post('/dates/difference', {
        start_date: mainDate.value,
        end_date: secondDate.value,
      })

      result.value = response.data
      return
    }

    const response = await api.post('/dates/add', {
      value: mainDate.value,
      operation: operation.value,
      days: days.value,
      months: months.value,
      years: years.value,
      output_format: outputFormat.value,
    })

    result.value = response.data
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Não foi possível calcular a data.'
  } finally {
    loading.value = false
  }
}

async function copyResult() {
  if (!resultToCopy.value) return

  await navigator.clipboard.writeText(resultToCopy.value)
  copied.value = true

  window.setTimeout(() => {
    copied.value = false
  }, 1800)
}
</script>

<template>
  <section class="tool-page">
    <div>
      <h2 class="text-3xl font-bold text-white">Manipulador de Datas</h2>
      <p class="mt-2 text-slate-400">
        Informe uma data, escolha a operação desejada e veja o resultado de forma simples.
      </p>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <form class="min-h-[var(--tool-panel-min-height)] space-y-5 rounded-lg border border-white/10 bg-white/[0.045] p-5" @submit.prevent="calculate">
        <div>
          <span class="text-sm font-medium text-slate-300">O que deseja fazer?</span>

          <div class="mt-2 grid gap-2 rounded-lg border border-white/10 bg-[#0b1020] p-2 sm:grid-cols-3">
            <button
              type="button"
              class="rounded-md px-3 py-3 text-sm font-semibold transition"
              :class="action === 'format'
                ? 'bg-teal-300 text-slate-950'
                : 'text-slate-300 hover:bg-white/[0.045] hover:text-white'"
              @click="action = 'format'; resetResult()"
            >
              Formatar
            </button>

            <button
              type="button"
              class="rounded-md px-3 py-3 text-sm font-semibold transition"
              :class="action === 'difference'
                ? 'bg-teal-300 text-slate-950'
                : 'text-slate-300 hover:bg-white/[0.045] hover:text-white'"
              @click="action = 'difference'; resetResult()"
            >
              Diferença
            </button>

            <button
              type="button"
              class="rounded-md px-3 py-3 text-sm font-semibold transition"
              :class="action === 'add'
                ? 'bg-teal-300 text-slate-950'
                : 'text-slate-300 hover:bg-white/[0.045] hover:text-white'"
              @click="action = 'add'; resetResult()"
            >
              Somar/Subtrair
            </button>
          </div>
        </div>

        <label class="block">
          <span class="text-sm font-medium text-slate-300">
            {{ action === 'difference' ? 'Data inicial' : 'Data' }}
          </span>

          <input
            v-model="mainDate"
            type="text"
            placeholder="Ex: 23/08/2024, 23082024 ou 2024-08-23"
            class="mt-2 w-full rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 text-white outline-none focus:border-teal-300"
          />

          <p class="mt-2 text-xs text-slate-500">
            Datas numéricas com 8 dígitos sero lidas como DDMMAAAA.
          </p>
        </label>

        <label v-if="action === 'difference'" class="block">
          <span class="text-sm font-medium text-slate-300">Data final</span>

          <input
            v-model="secondDate"
            type="text"
            placeholder="Ex: 14/11/2026"
            class="mt-2 w-full rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 text-white outline-none focus:border-teal-300"
          />
        </label>

        <label v-if="action === 'format' || action === 'add'" class="block">
          <span class="text-sm font-medium text-slate-300">Formato de saída</span>

          <select
            v-model="outputFormat"
            class="mt-2 w-full rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 text-white outline-none focus:border-teal-300"
          >
            <option value="br">DD/MM/YYYY</option>
            <option value="iso">YYYY-MM-DD</option>
            <option value="datetime-br">DD/MM/YYYY HH:mm:ss</option>
            <option value="datetime-iso">YYYY-MM-DD HH:mm:ss</option>
          </select>
        </label>

        <div v-if="action === 'add'" class="space-y-4">
          <label class="block">
            <span class="text-sm font-medium text-slate-300">Operação</span>

            <select
              v-model="operation"
              class="mt-2 w-full rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 text-white outline-none focus:border-teal-300"
            >
              <option value="add">Adicionar</option>
              <option value="subtract">Subtrair</option>
            </select>
          </label>

          <div class="grid gap-3 sm:grid-cols-3">
            <BaseNumberInput v-model="days" label="Dias" :min="0" :step="1" />
            <BaseNumberInput v-model="months" label="Meses" :min="0" :step="1" />
            <BaseNumberInput v-model="years" label="Anos" :min="0" :step="1" />
          </div>
        </div>

        <button
          type="submit"
          class="w-full rounded-md bg-teal-300 px-5 py-3 font-semibold text-slate-950 transition hover:bg-teal-200 disabled:cursor-not-allowed disabled:opacity-60"
          :disabled="loading"
        >
          {{ loading ? 'Calculando...' : 'Calcular' }}
        </button>

        <p v-if="error" class="rounded-md border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
          {{ error }}
        </p>
      </form>

      <div class="min-h-[var(--tool-panel-min-height)] rounded-lg border border-white/10 bg-white/[0.045] p-5">
        <div class="flex items-start justify-between gap-4">
          <div>
            <h3 class="text-lg font-semibold text-white">Resultado</h3>
            <p class="mt-1 text-sm text-slate-400">{{ actionTitle }}</p>
          </div>

          <span class="rounded-full border border-white/10 px-3 py-1 text-xs font-medium text-slate-400">
            {{ action }}
          </span>
        </div>

        <div v-if="result" class="mt-6 space-y-4">
          <div class="rounded-lg border border-teal-300/30 bg-teal-300/10 p-5">
            <p class="text-sm text-teal-200">Resultado principal</p>

            <p class="mt-2 break-all font-mono text-2xl font-bold text-teal-200">
              {{ resultToCopy }}
            </p>
          </div>

          <div v-if="action === 'format'" class="grid gap-3 text-sm text-slate-300">
            <p><span class="text-slate-500">Original:</span> {{ result.original }}</p>
            <p><span class="text-slate-500">ISO:</span> {{ result.iso }}</p>
            <p><span class="text-slate-500">Timestamp:</span> {{ result.timestamp }}</p>
            <p><span class="text-slate-500">Formato detectado:</span> {{ result.detected_format }}</p>
          </div>

          <div v-if="action === 'difference'" class="grid gap-3 text-sm text-slate-300">
            <p><span class="text-slate-500">Data inicial:</span> {{ result.start_daté }}</p>
            <p><span class="text-slate-500">Data final:</span> {{ result.end_daté }}</p>
            <p><span class="text-slate-500">Leitura:</span> {{ result.human_readable }}</p>
            <p><span class="text-slate-500">Horas:</span> {{ result.total_hours }}</p>
            <p><span class="text-slate-500">Minutos:</span> {{ result.total_minutes }}</p>
          </div>

          <div v-if="action === 'add'" class="grid gap-3 text-sm text-slate-300">
            <p><span class="text-slate-500">Original:</span> {{ result.original }}</p>
            <p><span class="text-slate-500">Operação:</span> {{ result.operation === 'add' ? 'Adicionar' : 'Subtrair' }}</p>
            <p><span class="text-slate-500">ISO:</span> {{ result.iso }}</p>
          </div>

          <button
            type="button"
            class="rounded-md border border-teal-300 px-4 py-2 text-sm font-semibold text-teal-200 transition hover:bg-teal-300 hover:text-slate-950"
            @click="copyResult"
          >
            {{ copied ? 'Resultado copiado!' : 'Copiar resultado' }}
          </button>
        </div>

        <p v-else class="mt-6 text-sm leading-6 text-slate-400">
          Informe os dados no card ao lado e clique em calcular.
        </p>
      </div>
    </div>
  </section>
</template>
