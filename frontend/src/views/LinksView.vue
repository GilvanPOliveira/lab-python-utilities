<script setup lang="ts">
import { computed, ref } from 'vue'
import { api } from '../services/api'

type LinkAction = 'shorten' | 'clean' | 'encode' | 'decode'

const action = ref<LinkAction>('shorten')
const value = ref('')
const customCode = ref('')
const result = ref<any | null>(null)
const error = ref('')
const copied = ref(false)
const loading = ref(false)

const actions = [
  {
    key: 'shorten',
    title: 'Encurtar',
    description: 'Gera um link curto real usando is.gd.',
  },
  {
    key: 'clean',
    title: 'Limpar URL',
    description: 'Remove parâmetros de tracking como UTM, fbclid e gclid.',
  },
  {
    key: 'encode',
    title: 'Encode',
    description: 'Codifica texto ou URL para uso seguro em links.',
  },
  {
    key: 'decode',
    title: 'Decode',
    description: 'Decodifica textos ou URLs previamente codificados.',
  },
] as const

const actionLabel = computed(() => {
  const labels = {
    shorten: 'Encurtar link',
    clean: 'Limpar URL',
    encode: 'Aplicar URL Encode',
    decode: 'Aplicar URL Decode',
  }

  return labels[action.value]
})

const currentAction = computed(() => {
  return actions.find((item) => item.key === action.value)
})

const inputLabel = computed(() => {
  if (action.value === 'encode' || action.value === 'decode') {
    return 'Texto ou URL'
  }

  return 'URL'
})

const inputPlaceholder = computed(() => {
  if (action.value === 'shorten') {
    return 'Cole a URL que deseja encurtar'
  }

  if (action.value === 'clean') {
    return 'Cole uma URL com parâmetros para limpar'
  }

  if (action.value === 'encode') {
    return 'Digite o texto ou URL para codificar'
  }

  return 'Cole o texto ou URL codificado'
})

const resultToCopy = computed(() => {
  if (!result.value) return ''

  if (action.value === 'shorten') return result.value.short_url
  if (action.value === 'clean') return result.value.cleaned_url
  if (action.value === 'encode') return result.value.encoded
  if (action.value === 'decode') return result.value.decoded

  return ''
})

const openableUrl = computed(() => {
  if (!result.value) return ''

  if (action.value === 'shorten') return result.value.short_url
  if (action.value === 'clean') return result.value.cleaned_url

  return ''
})

function resetResult() {
  result.value = null
  error.value = ''
  copied.value = false
}

function selectAction(nextAction: LinkAction) {
  action.value = nextAction
  resetResult()
}

async function processLink() {
  resetResult()
  loading.value = true

  try {
    if (action.value === 'shorten') {
      const response = await api.post('/links/shorten', {
        url: value.value,
        custom_code: customCode.value.trim() || null,
      })

      result.value = response.data
      return
    }

    const endpoint = `/links/${action.value}`
    const payloadKey = action.value === 'encode' || action.value === 'decode' ? 'value' : 'url'

    const response = await api.post(endpoint, {
      [payloadKey]: value.value,
    })

    result.value = response.data
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Não foi possível processar o link.'
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

function openResult() {
  if (!openableUrl.value) return

  window.open(openableUrl.value, '_blank', 'noopener,noreferrer')
}

function clearFields() {
  value.value = ''
  customCode.value = ''
  resetResult()
}
</script>

<template>
  <section class="tool-page">
    <div>
      <h2 class="text-3xl font-bold text-white">Link Tools</h2>
      <p class="mt-2 text-slate-400">
        Encurte links reais, limpe URLs e aplique encode/decode sem depender de páginas cheias de anúncios.
      </p>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <form
        class="min-h-[var(--tool-panel-min-height)] space-y-5 rounded-lg border border-white/10 bg-white/[0.045] p-5"
        @submit.prevent="processLink"
      >
        <div>
          <span class="text-sm font-medium text-slate-300">Escolha uma ferramenta</span>

          <div class="mt-3 grid gap-3 sm:grid-cols-2">
            <button
              v-for="option in actions"
              :key="option.key"
              type="button"
              class="rounded-lg border p-4 text-left transition"
              :class="action === option.key
                ? 'border-teal-300 bg-teal-300/10'
                : 'border-white/10 bg-[#0b1020] hover:border-teal-300/70'"
              @click="selectAction(option.key)"
            >
              <span
                class="block text-sm font-semibold"
                :class="action === option.key ? 'text-teal-200' : 'text-white'"
              >
                {{ option.title }}
              </span>

              <span class="mt-2 block text-xs leading-5 text-slate-500">
                {{ option.description }}
              </span>
            </button>
          </div>
        </div>

        <div class="rounded-lg border border-white/10 bg-[#0b1020] p-4">
          <p class="text-sm font-semibold text-white">
            {{ currentAction?.title }}
          </p>

          <p class="mt-1 text-xs leading-5 text-slate-500">
            {{ currentAction?.description }}
          </p>
        </div>

        <label class="block">
          <span class="text-sm font-medium text-slate-300">{{ inputLabel }}</span>

          <textarea
            v-model="value"
            rows="6"
            :placeholder="inputPlaceholder"
            class="mt-2 w-full resize-none rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 text-white outline-none focus:border-teal-300"
          />
        </label>

        <label v-if="action === 'shorten'" class="block">
          <span class="text-sm font-medium text-slate-300">Alias personalizado opcional</span>

          <input
            v-model="customCode"
            type="text"
            placeholder="Ex: meu-link"
            class="mt-2 w-full rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 text-white outline-none focus:border-teal-300"
          />

          <p class="mt-2 text-xs text-slate-500">
            Entre 5 e 30 caracteres. O alias pode estar indisponível caso já exista no is.gd.
          </p>
        </label>

        <div class="grid gap-3 sm:grid-cols-[1fr_auto]">
          <button
            type="submit"
            class="rounded-md bg-teal-300 px-5 py-3 font-semibold text-slate-950 transition hover:bg-teal-200 disabled:cursor-not-allowed disabled:opacity-60"
            :disabled="loading"
          >
            {{ loading ? 'Processando...' : actionLabel }}
          </button>

          <button
            type="button"
            class="rounded-md border border-white/10 px-5 py-3 font-semibold text-slate-300 transition hover:border-red-400 hover:text-red-300"
            @click="clearFields"
          >
            Limpar
          </button>
        </div>

        <p v-if="action === 'shorten'" class="rounded-md border border-teal-300/30 bg-teal-300/10 p-3 text-xs leading-5 text-teal-50">
          O link encurtado  gerado pelo is.gd e funciona publicamente, sem banco de dados no projeto.
        </p>

        <p v-if="error" class="rounded-md border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
          {{ error }}
        </p>
      </form>

      <div class="min-h-[var(--tool-panel-min-height)] rounded-lg border border-white/10 bg-white/[0.045] p-5">
        <div class="flex items-start justify-between gap-4">
          <div>
            <h3 class="text-lg font-semibold text-white">Resultado</h3>
            <p class="mt-1 text-sm text-slate-400">
              {{ currentAction?.title }}
            </p>
          </div>

          <span class="rounded-full border border-white/10 px-3 py-1 text-xs font-medium text-slate-400">
            {{ action }}
          </span>
        </div>

        <div v-if="result" class="mt-5 space-y-4">
          <div class="rounded-lg border border-teal-300/30 bg-teal-300/10 p-5">
            <p class="text-sm text-teal-200">Resultado principal</p>

            <p class="mt-2 break-all font-mono text-teal-200">
              {{ resultToCopy }}
            </p>
          </div>

          <div v-if="action === 'shorten'" class="rounded-md border border-white/10 bg-[#0b1020] p-4 text-sm text-slate-300">
            <p class="break-all">
              <span class="text-slate-500">Original:</span>
              {{ result.original_url }}
            </p>

            <p class="mt-2">
              <span class="text-slate-500">Provedor:</span>
              {{ result.provider }}
            </p>
          </div>

          <div v-if="action === 'clean'" class="rounded-md border border-white/10 bg-[#0b1020] p-4 text-sm text-slate-300">
            <p>
              <span class="text-slate-500">Domínio:</span>
              {{ result.domain }}
            </p>

            <p class="mt-2">
              <span class="text-slate-500">Parâmetros removidos:</span>
              {{ result.removed_params.length ? result.removed_params.join(', ') : 'nenhum' }}
            </p>
          </div>

          <div class="flex flex-wrap gap-3">
            <button
              type="button"
              class="rounded-md border border-teal-300 px-4 py-2 text-sm font-semibold text-teal-200 transition hover:bg-teal-300 hover:text-slate-950"
              @click="copyResult"
            >
              {{ copied ? 'Copiado!' : 'Copiar resultado' }}
            </button>

            <button
              v-if="openableUrl"
              type="button"
              class="rounded-md border border-white/10 px-4 py-2 text-sm font-semibold text-slate-300 transition hover:border-teal-300 hover:text-teal-200"
              @click="openResult"
            >
              Abrir link
            </button>
          </div>
        </div>

        <p v-else class="mt-6 text-sm leading-6 text-slate-400">
          Escolha uma ferramenta, informe o conteúdo no card ao lado e processe o resultado.
        </p>
      </div>
    </div>
  </section>
</template>
