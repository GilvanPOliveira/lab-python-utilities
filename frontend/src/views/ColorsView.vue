<script setup lang="ts">
import { computed, ref } from 'vue'
import { api } from '../services/api'

type ColorMode = 'hex' | 'rgb' | 'hsl' | 'palette'

const mode = ref<ColorMode>('hex')

const hexColor = ref('#22D3EE')
const r = ref(34)
const g = ref(211)
const b = ref(238)
const h = ref(188)
const s = ref(85)
const l = ref(53)

const result = ref<any | null>(null)
const error = ref('')
const copied = ref('')
const loading = ref(false)

const resultMain = computed(() => {
  if (!result.value) return null

  if (mode.value === 'palette') return result.value.base

  return result.value
})

async function processColor() {
  error.value = ''
  result.value = null
  copied.value = ''
  loading.value = true

  try {
    if (mode.value === 'hex') {
      const response = await api.post('/colors/hex', {
        hex_color: hexColor.value,
      })

      result.value = response.data
      return
    }

    if (mode.value === 'rgb') {
      const response = await api.post('/colors/rgb', {
        r: r.value,
        g: g.value,
        b: b.value,
      })

      result.value = response.data
      return
    }

    if (mode.value === 'hsl') {
      const response = await api.post('/colors/hsl', {
        h: h.value,
        s: s.value,
        l: l.value,
      })

      result.value = response.data
      return
    }

    const response = await api.post('/colors/palette', {
      hex_color: hexColor.value,
    })

    result.value = response.data
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Não foi possível processar a cor.'
  } finally {
    loading.value = false
  }
}

async function copyText(value: string, key: string) {
  await navigator.clipboard.writeText(value)
  copied.value = key

  window.setTimeout(() => {
    copied.value = ''
  }, 1800)
}
</script>

<template>
  <section class="mx-auto max-w-5xl space-y-6">
    <div>
      <h2 class="text-3xl font-bold text-white">Color Tools</h2>
      <p class="mt-2 text-slate-400">
        Converta cores entre HEX, RGB, HSL e gere variações simples de paleta.
      </p>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <form class="min-h-[560px] space-y-5 rounded-2xl border border-slate-800 bg-slate-900 p-5" @submit.prevent="processColor">
        <div>
          <span class="text-sm font-medium text-slate-300">Ferramenta</span>

          <div class="mt-2 grid grid-cols-2 gap-2 rounded-2xl border border-slate-800 bg-slate-950 p-2">
            <button
              v-for="option in [
                { key: 'hex', label: 'HEX' },
                { key: 'rgb', label: 'RGB' },
                { key: 'hsl', label: 'HSL' },
                { key: 'palette', label: 'Paleta' },
              ]"
              :key="option.key"
              type="button"
              class="rounded-xl px-3 py-3 text-sm font-semibold transition"
              :class="mode === option.key
                ? 'bg-cyan-400 text-slate-950'
                : 'text-slate-300 hover:bg-slate-900 hover:text-white'"
              @click="mode = option.key as ColorMode; result = null"
            >
              {{ option.label }}
            </button>
          </div>
        </div>

        <label v-if="mode === 'hex' || mode === 'palette'" class="block">
          <span class="text-sm font-medium text-slate-300">Cor HEX</span>

          <div class="mt-2 grid grid-cols-[64px_1fr] gap-3">
            <input
              v-model="hexColor"
              type="color"
              class="h-12 w-16 rounded-xl border border-slate-700 bg-slate-950"
            />

            <input
              v-model="hexColor"
              type="text"
              placeholder="#22D3EE"
              class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
            />
          </div>
        </label>

        <div v-if="mode === 'rgb'" class="grid gap-3 sm:grid-cols-3">
          <label class="block">
            <span class="text-sm font-medium text-slate-300">R</span>
            <input v-model.number="r" type="number" min="0" max="255" class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400" />
          </label>

          <label class="block">
            <span class="text-sm font-medium text-slate-300">G</span>
            <input v-model.number="g" type="number" min="0" max="255" class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400" />
          </label>

          <label class="block">
            <span class="text-sm font-medium text-slate-300">B</span>
            <input v-model.number="b" type="number" min="0" max="255" class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400" />
          </label>
        </div>

        <div v-if="mode === 'hsl'" class="grid gap-3 sm:grid-cols-3">
          <label class="block">
            <span class="text-sm font-medium text-slate-300">H</span>
            <input v-model.number="h" type="number" min="0" max="360" class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400" />
          </label>

          <label class="block">
            <span class="text-sm font-medium text-slate-300">S</span>
            <input v-model.number="s" type="number" min="0" max="100" class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400" />
          </label>

          <label class="block">
            <span class="text-sm font-medium text-slate-300">L</span>
            <input v-model.number="l" type="number" min="0" max="100" class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400" />
          </label>
        </div>

        <button
          type="submit"
          class="w-full rounded-xl bg-cyan-400 px-5 py-3 font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:opacity-60"
          :disabled="loading"
        >
          {{ loading ? 'Processando...' : 'Processar cor' }}
        </button>

        <p v-if="error" class="rounded-xl border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
          {{ error }}
        </p>
      </form>

      <div class="min-h-[560px] rounded-2xl border border-slate-800 bg-slate-900 p-5">
        <h3 class="text-lg font-semibold text-white">Resultado</h3>

        <div v-if="resultMain" class="mt-5 space-y-4">
          <div
            class="h-32 rounded-2xl border border-slate-800"
            :style="{ backgroundColor: resultMain.hex }"
          />

          <div class="grid gap-3">
            <button class="rounded-xl border border-slate-800 bg-slate-950 p-4 text-left" @click="copyText(resultMain.hex, 'hex')">
              <span class="text-xs text-slate-500">HEX</span>
              <p class="font-mono text-cyan-300">{{ copied === 'hex' ? 'Copiado!' : resultMain.hex }}</p>
            </button>

            <button class="rounded-xl border border-slate-800 bg-slate-950 p-4 text-left" @click="copyText(resultMain.rgb, 'rgb')">
              <span class="text-xs text-slate-500">RGB</span>
              <p class="font-mono text-cyan-300">{{ copied === 'rgb' ? 'Copiado!' : resultMain.rgb }}</p>
            </button>

            <button class="rounded-xl border border-slate-800 bg-slate-950 p-4 text-left" @click="copyText(resultMain.hsl, 'hsl')">
              <span class="text-xs text-slate-500">HSL</span>
              <p class="font-mono text-cyan-300">{{ copied === 'hsl' ? 'Copiado!' : resultMain.hsl }}</p>
            </button>
          </div>

          <div v-if="mode === 'palette'" class="space-y-3">
            <h4 class="text-sm font-semibold text-white">Variações</h4>

            <div class="grid grid-cols-3 gap-3">
              <button
                v-for="color in [...result.darker, ...result.lighter]"
                :key="color.hex"
                class="h-20 rounded-xl border border-slate-800"
                :style="{ backgroundColor: color.hex }"
                @click="copyText(color.hex, color.hex)"
              />
            </div>
          </div>
        </div>

        <p v-else class="mt-4 text-sm leading-6 text-slate-400">
          O resultado aparecerá aqui.
        </p>
      </div>
    </div>
  </section>
</template>
