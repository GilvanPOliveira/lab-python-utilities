<script setup lang="ts">
import { computed, ref } from 'vue'
import { api } from '../services/api'
import BaseNumberInput from '../components/BaseNumberInput.vue'

type ConversionCategory = 'px-rem' | 'storage' | 'temperature' | 'length' | 'mass' | 'area' | 'volume'
type FórmulaType = 'percentage_of' | 'percentage_change' | 'rule_of_three' | 'bmi'

const category = ref<ConversionCategory>('px-rem')
const fromUnit = ref('px')
const toUnit = ref('rem')
const value = ref(16)
const baseFontSize = ref(16)
const conversionResult = ref<any | null>(null)

const fórmulaType = ref<FórmulaType>('percentage_of')
const fórmulaValues = ref({
  percentage: 10,
  total: 100,
  initial: 100,
  final: 150,
  a: 100,
  b: 50,
  c: 200,
  weight: 70,
  height: 1.75,
})
const fórmulaResult = ref<any | null>(null)

const error = ref('')
const copied = ref(false)
const loading = ref(false)

const unitsByCategory = {
  'px-rem': ['px', 'rem'],
  storage: ['B', 'KB', 'MB', 'GB', 'TB'],
  temperature: ['c', 'f', 'k'],
  length: ['mm', 'cm', 'm', 'km', 'in', 'ft', 'yd', 'mi'],
  mass: ['mg', 'g', 'kg', 't', 'oz', 'lb'],
  area: ['cm2', 'm2', 'km2', 'ha'],
  volume: ['ml', 'l', 'm3'],
}

const fórmulaLabels = {
  percentage_of: 'Porcentagem de um valor',
  percentage_change: 'Variação percentual',
  rule_of_three: 'Regra de três',
  bmi: 'IMC',
}

const currentUnits = computed(() => unitsByCategory[category.value])
const conversionCopyText = computed(() => {
  if (!conversionResult.value) return ''
  return `${conversionResult.value.input_value} ${conversionResult.value.from_unit} = ${conversionResult.value.result} ${conversionResult.value.to_unit}`
})
const formulaCopyText = computed(() => {
  if (!fórmulaResult.value) return ''
  return `${fórmulaResult.value.expression}`
})

function resetResults() {
  conversionResult.value = null
  fórmulaResult.value = null
  error.value = ''
  copied.value = false
}

function changeCategory() {
  const units = unitsByCategory[category.value]
  fromUnit.value = units[0]
  toUnit.value = units[1] || units[0]
  resetResults()
}

async function convertUnit() {
  error.value = ''
  conversionResult.value = null
  loading.value = true

  try {
    const response = await api.post('/units/convert', {
      category: category.value,
      from_unit: fromUnit.value,
      to_unit: toUnit.value,
      value: value.value,
      base_font_size: baseFontSize.value,
    })

    conversionResult.value = response.data
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Não foi possível converter.'
  } finally {
    loading.value = false
  }
}

function buildFórmulaPayload() {
  if (fórmulaType.value === 'percentage_of') {
    return {
      percentage: fórmulaValues.value.percentage,
      total: fórmulaValues.value.total,
    }
  }

  if (fórmulaType.value === 'percentage_change') {
    return {
      initial: fórmulaValues.value.initial,
      final: fórmulaValues.value.final,
    }
  }

  if (fórmulaType.value === 'rule_of_three') {
    return {
      a: fórmulaValues.value.a,
      b: fórmulaValues.value.b,
      c: fórmulaValues.value.c,
    }
  }

  return {
    weight: fórmulaValues.value.weight,
    height: fórmulaValues.value.height,
  }
}

async function calculateFórmula() {
  error.value = ''
  fórmulaResult.value = null
  loading.value = true

  try {
    const response = await api.post('/units/fórmula', {
      fórmula_type: fórmulaType.value,
      values: buildFórmulaPayload(),
    })

    fórmulaResult.value = response.data
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Não foi possível calcular a fórmula.'
  } finally {
    loading.value = false
  }
}

async function copyText(text: string) {
  if (!text) return

  await navigator.clipboard.writeText(text)
  copied.value = true

  window.setTimeout(() => {
    copied.value = false
  }, 1800)
}
</script>

<template>
  <section class="tool-page">
    <div>
      <h2 class="text-3xl font-bold text-white">Unidades e Fórmulas</h2>
      <p class="mt-2 text-slate-400">
        Converta unidades comuns e calcule fórmulas rápidas do dia a dia.
      </p>
    </div>

    <p v-if="error" class="rounded-md border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-300">
      {{ error }}
    </p>

    <div class="grid gap-6 lg:grid-cols-2">
      <div class="min-h-[var(--tool-panel-min-height)] rounded-lg border border-white/10 bg-white/[0.045] p-5">
        <h3 class="text-lg font-semibold text-white">Conversor de unidades</h3>

        <form class="mt-5 space-y-4" @submit.prevent="convertUnit">
          <label class="block">
            <span class="text-sm font-medium text-slate-300">Categoria</span>

            <select
              v-model="category"
              class="mt-2 w-full rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 text-white outline-none focus:border-teal-300"
              @change="changeCategory"
            >
              <option value="px-rem">PX / REM</option>
              <option value="storage">Armazenamento</option>
              <option value="temperature">Temperatura</option>
              <option value="length">Comprimento</option>
              <option value="mass">Massa</option>
              <option value="area">Área</option>
              <option value="volume">Volume</option>
            </select>
          </label>

          <BaseNumberInput v-model="value" label="Valor" :step="1" />

          <div class="grid gap-3 sm:grid-cols-2">
            <label class="block">
              <span class="text-sm font-medium text-slate-300">De</span>

              <select
                v-model="fromUnit"
                class="mt-2 w-full rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 text-white outline-none focus:border-teal-300"
              >
                <option v-for="unit in currentUnits" :key="unit" :value="unit">
                  {{ unit }}
                </option>
              </select>
            </label>

            <label class="block">
              <span class="text-sm font-medium text-slate-300">Para</span>

              <select
                v-model="toUnit"
                class="mt-2 w-full rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 text-white outline-none focus:border-teal-300"
              >
                <option v-for="unit in currentUnits" :key="unit" :value="unit">
                  {{ unit }}
                </option>
              </select>
            </label>
          </div>

          <BaseNumberInput v-if="category === 'px-rem'" v-model="baseFontSize" label="Base font-size" :min="1" :step="1" suffix="px" />

          <button
            type="submit"
            class="w-full rounded-md bg-teal-300 px-5 py-3 font-semibold text-slate-950 transition hover:bg-teal-200 disabled:opacity-60"
            :disabled="loading"
          >
            {{ loading ? 'Convertendo...' : 'Converter' }}
          </button>
        </form>

        <div v-if="conversionResult" class="mt-5 space-y-4">
          <div class="rounded-lg border border-teal-300/30 bg-teal-300/10 p-5">
            <p class="text-sm text-teal-200">Resultado</p>
            <p class="mt-2 break-all font-mono text-2xl font-bold text-teal-200">
              {{ conversionResult.result }} {{ conversionResult.to_unit }}
            </p>
          </div>

          <p class="rounded-md border border-white/10 bg-[#0b1020] p-4 text-sm text-slate-300">
            {{ conversionResult.fórmula }}
          </p>

          <button
            type="button"
            class="rounded-md border border-teal-300 px-4 py-2 text-sm font-semibold text-teal-200 transition hover:bg-teal-300 hover:text-slate-950"
            @click="copyText(conversionCopyText)"
          >
            {{ copied ? 'Copiado!' : 'Copiar resultado' }}
          </button>
        </div>
      </div>

      <div class="min-h-[var(--tool-panel-min-height)] rounded-lg border border-white/10 bg-white/[0.045] p-5">
        <h3 class="text-lg font-semibold text-white">Fórmulas rápidas</h3>

        <form class="mt-5 space-y-4" @submit.prevent="calculateFórmula">
          <label class="block">
            <span class="text-sm font-medium text-slate-300">Fórmula</span>

            <select
              v-model="fórmulaType"
              class="mt-2 w-full rounded-md border border-white/10 bg-[#0b1020] px-4 py-3 text-white outline-none focus:border-teal-300"
              @change="fórmulaResult = null"
            >
              <option value="percentage_of">Porcentagem de um valor</option>
              <option value="percentage_change">Variação percentual</option>
              <option value="rule_of_three">Regra de três</option>
              <option value="bmi">IMC</option>
            </select>
          </label>

          <div v-if="fórmulaType === 'percentage_of'" class="grid gap-3 sm:grid-cols-2">
            <BaseNumberInput v-model="fórmulaValues.percentage" label="Porcentagem" :step="1" suffix="%" />
            <BaseNumberInput v-model="fórmulaValues.total" label="Total" :step="1" />
          </div>

          <div v-if="fórmulaType === 'percentage_change'" class="grid gap-3 sm:grid-cols-2">
            <BaseNumberInput v-model="fórmulaValues.initial" label="Inicial" :step="1" />
            <BaseNumberInput v-model="fórmulaValues.final" label="Final" :step="1" />
          </div>

          <div v-if="fórmulaType === 'rule_of_three'" class="grid gap-3 sm:grid-cols-3">
            <BaseNumberInput v-model="fórmulaValues.a" label="A" :step="1" />
            <BaseNumberInput v-model="fórmulaValues.b" label="B" :step="1" />
            <BaseNumberInput v-model="fórmulaValues.c" label="C" :step="1" />
          </div>

          <div v-if="fórmulaType === 'bmi'" class="grid gap-3 sm:grid-cols-2">
            <BaseNumberInput v-model="fórmulaValues.weight" label="Peso" :step="1" suffix="kg" />
            <BaseNumberInput v-model="fórmulaValues.height" label="Altura" :step="0.01" suffix="m" />
          </div>

          <button
            type="submit"
            class="w-full rounded-md bg-teal-300 px-5 py-3 font-semibold text-slate-950 transition hover:bg-teal-200 disabled:opacity-60"
            :disabled="loading"
          >
            {{ loading ? 'Calculando...' : 'Calcular fórmula' }}
          </button>
        </form>

        <div v-if="fórmulaResult" class="mt-5 space-y-4">
          <div class="rounded-lg border border-teal-300/30 bg-teal-300/10 p-5">
            <p class="text-sm text-teal-200">{{ fórmulaLabels[fórmulaType] }}</p>
            <p class="mt-2 break-all font-mono text-2xl font-bold text-teal-200">
              {{ fórmulaResult.result }}
            </p>
          </div>

          <p class="rounded-md border border-white/10 bg-[#0b1020] p-4 text-sm text-slate-300">
            {{ fórmulaResult.expression }}
          </p>

          <button
            type="button"
            class="rounded-md border border-teal-300 px-4 py-2 text-sm font-semibold text-teal-200 transition hover:bg-teal-300 hover:text-slate-950"
            @click="copyText(formulaCopyText)"
          >
            {{ copied ? 'Copiado!' : 'Copiar fórmula' }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>
