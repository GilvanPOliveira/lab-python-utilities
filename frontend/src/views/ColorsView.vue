<script setup lang="ts">
import { computed, ref } from 'vue'
import { api } from '../services/api'
import BaseNumberInput from '../components/BaseNumberInput.vue'

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
  <section class="tool-page">
    <div>
      <h2 class="text-3xl font-bold text-white">Color Tools</h2>
      <p class="mt-2 text-slate-400">
        Converta cores entre HEX, RGB, HSL e gere variações simples de paleta.
      </p>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <form class="min-h-[var(--tool-panel-min-height)] space-y-5 rounded-lg border border-white/10 bg-white/[0.045] p-5" @submit.prevent="processColor">
        <div>
          <span class="text-sm font-medium text-slate-300">Ferramenta</span>

          <div class="mt-2 grid grid-cols-2 gap-2 rounded-lg border border-white/10 bg-[#0b1020] p-2">
            <button
              v-for="option in [
                { key: 'hex', label: 'HEX' },
                { key: 'rgb', label: 'RGB' },
                { key: 'hsl', label: 'HSL' },
                { key: 'palette', label: 'Paleta' },
              ]"
              :key="option.key"
              type="button"
              class="rounded-md px-3 py-3 text-sm font-semibold transition"
              :class="mode === option.key
                ? 'bg-teal-300 text-slate-950'
                : 'text-slate-300 hover:bg-white/[0.045] hover:text-white'"
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
              class="h-12 w-16 rounded-md border border-white/10 bg-[#0b1020]"
            />

            <input
              v-model="hexColor"
              type="text"
              placeholder="#22D3EE"
              class="w-full rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 text-white outline-none focus:border-teal-300"
            />
          </div>
        </label>

        <div v-if="mode === 'rgb'" class="grid gap-3 sm:grid-cols-3">
          <BaseNumberInput v-model="r" label="R" :min="0" :max="255" :step="1" />
          <BaseNumberInput v-model="g" label="G" :min="0" :max="255" :step="1" />
          <BaseNumberInput v-model="b" label="B" :min="0" :max="255" :step="1" />
        </div>

        <div v-if="mode === 'hsl'" class="grid gap-3 sm:grid-cols-3">
          <BaseNumberInput v-model="h" label="H" :min="0" :max="360" :step="1" />
          <BaseNumberInput v-model="s" label="S" :min="0" :max="100" :step="1" suffix="%" />
          <BaseNumberInput v-model="l" label="L" :min="0" :max="100" :step="1" suffix="%" />
        </div>

        <button
          type="submit"
          class="w-full rounded-md bg-teal-300 px-5 py-3 font-semibold text-slate-950 transition hover:bg-teal-200 disabled:opacity-60"
          :disabled="loading"
        >
          {{ loading ? 'Processando...' : 'Processar cor' }}
        </button>

        <p v-if="error" class="rounded-md border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
          {{ error }}
        </p>
      </form>

      <div class="min-h-[var(--tool-panel-min-height)] rounded-lg border border-white/10 bg-white/[0.045] p-5">
        <h3 class="text-lg font-semibold text-white">Resultado</h3>

        <div v-if="resultMain" class="mt-5 space-y-4">
          <div
            class="h-32 rounded-lg border border-white/10"
            :style="{ backgroundColor: resultMain.hex }"
          />

          <div class="grid gap-3">
            <button class="rounded-md border border-white/10 bg-[#0b1020] p-4 text-left" @click="copyText(resultMain.hex, 'hex')">
              <span class="text-xs text-slate-500">HEX</span>
              <p class="font-mono text-teal-200">{{ copied === 'hex' ? 'Copiado!' : resultMain.hex }}</p>
            </button>

            <button class="rounded-md border border-white/10 bg-[#0b1020] p-4 text-left" @click="copyText(resultMain.rgb, 'rgb')">
              <span class="text-xs text-slate-500">RGB</span>
              <p class="font-mono text-teal-200">{{ copied === 'rgb' ? 'Copiado!' : resultMain.rgb }}</p>
            </button>

            <button class="rounded-md border border-white/10 bg-[#0b1020] p-4 text-left" @click="copyText(resultMain.hsl, 'hsl')">
              <span class="text-xs text-slate-500">HSL</span>
              <p class="font-mono text-teal-200">{{ copied === 'hsl' ? 'Copiado!' : resultMain.hsl }}</p>
            </button>
          </div>

          <div v-if="mode === 'palette'" class="space-y-3">
            <h4 class="text-sm font-semibold text-white">Variações</h4>

            <div class="grid grid-cols-3 gap-3">
              <button
                v-for="color in [...result.darker, ...result.lighter]"
                :key="color.hex"
                class="h-20 rounded-md border border-white/10"
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
