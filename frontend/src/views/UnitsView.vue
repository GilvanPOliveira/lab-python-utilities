<script setup lang="ts">
import { computed, ref } from 'vue'
import { api } from '../services/api'

type ConversionCategory = 'px-rem' | 'storage' | 'temperature' | 'length' | 'mass' | 'area' | 'volume'
type FormulaType = 'percentage_of' | 'percentage_change' | 'rule_of_three' | 'bmi'

const category = ref<ConversionCategory>('px-rem')
const fromUnit = ref('px')
const toUnit = ref('rem')
const value = ref(16)
const baseFontSize = ref(16)
const conversionResult = ref<any | null>(null)

const formulaType = ref<FormulaType>('percentage_of')
const formulaValues = ref({
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
const formulaResult = ref<any | null>(null)

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

const formulaLabels = {
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
  if (!formulaResult.value) return ''
  return `${formulaResult.value.expression}`
})

function resetResults() {
  conversionResult.value = null
  formulaResult.value = null
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

function buildFormulaPayload() {
  if (formulaType.value === 'percentage_of') {
    return {
      percentage: formulaValues.value.percentage,
      total: formulaValues.value.total,
    }
  }

  if (formulaType.value === 'percentage_change') {
    return {
      initial: formulaValues.value.initial,
      final: formulaValues.value.final,
    }
  }

  if (formulaType.value === 'rule_of_three') {
    return {
      a: formulaValues.value.a,
      b: formulaValues.value.b,
      c: formulaValues.value.c,
    }
  }

  return {
    weight: formulaValues.value.weight,
    height: formulaValues.value.height,
  }
}

async function calculateFormula() {
  error.value = ''
  formulaResult.value = null
  loading.value = true

  try {
    const response = await api.post('/units/formula', {
      formula_type: formulaType.value,
      values: buildFormulaPayload(),
    })

    formulaResult.value = response.data
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
  <section class="mx-auto max-w-5xl space-y-6">
    <div>
      <h2 class="text-3xl font-bold text-white">Unidades e Fórmulas</h2>
      <p class="mt-2 text-slate-400">
        Converta unidades comuns e calcule fórmulas rápidas do dia a dia.
      </p>
    </div>

    <p v-if="error" class="rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-300">
      {{ error }}
    </p>

    <div class="grid gap-6 lg:grid-cols-2">
      <div class="min-h-[560px] rounded-2xl border border-slate-800 bg-slate-900 p-5">
        <h3 class="text-lg font-semibold text-white">Conversor de unidades</h3>

        <form class="mt-5 space-y-4" @submit.prevent="convertUnit">
          <label class="block">
            <span class="text-sm font-medium text-slate-300">Categoria</span>

            <select
              v-model="category"
              class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
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

          <label class="block">
            <span class="text-sm font-medium text-slate-300">Valor</span>

            <input
              v-model.number="value"
              type="number"
              step="any"
              class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
            />
          </label>

          <div class="grid gap-3 sm:grid-cols-2">
            <label class="block">
              <span class="text-sm font-medium text-slate-300">De</span>

              <select
                v-model="fromUnit"
                class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
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
                class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
              >
                <option v-for="unit in currentUnits" :key="unit" :value="unit">
                  {{ unit }}
                </option>
              </select>
            </label>
          </div>

          <label v-if="category === 'px-rem'" class="block">
            <span class="text-sm font-medium text-slate-300">Base font-size</span>

            <input
              v-model.number="baseFontSize"
              type="number"
              min="1"
              step="any"
              class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
            />
          </label>

          <button
            type="submit"
            class="w-full rounded-xl bg-cyan-400 px-5 py-3 font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:opacity-60"
            :disabled="loading"
          >
            {{ loading ? 'Convertendo...' : 'Converter' }}
          </button>
        </form>

        <div v-if="conversionResult" class="mt-5 space-y-4">
          <div class="rounded-2xl border border-cyan-400/30 bg-cyan-400/10 p-5">
            <p class="text-sm text-cyan-200">Resultado</p>
            <p class="mt-2 break-all font-mono text-2xl font-bold text-cyan-300">
              {{ conversionResult.result }} {{ conversionResult.to_unit }}
            </p>
          </div>

          <p class="rounded-xl border border-slate-800 bg-slate-950 p-4 text-sm text-slate-300">
            {{ conversionResult.formula }}
          </p>

          <button
            type="button"
            class="rounded-xl border border-cyan-400 px-4 py-2 text-sm font-semibold text-cyan-300 transition hover:bg-cyan-400 hover:text-slate-950"
            @click="copyText(conversionCopyText)"
          >
            {{ copied ? 'Copiado!' : 'Copiar resultado' }}
          </button>
        </div>
      </div>

      <div class="min-h-[560px] rounded-2xl border border-slate-800 bg-slate-900 p-5">
        <h3 class="text-lg font-semibold text-white">Fórmulas rápidas</h3>

        <form class="mt-5 space-y-4" @submit.prevent="calculateFormula">
          <label class="block">
            <span class="text-sm font-medium text-slate-300">Fórmula</span>

            <select
              v-model="formulaType"
              class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
              @change="formulaResult = null"
            >
              <option value="percentage_of">Porcentagem de um valor</option>
              <option value="percentage_change">Variação percentual</option>
              <option value="rule_of_three">Regra de três</option>
              <option value="bmi">IMC</option>
            </select>
          </label>

          <div v-if="formulaType === 'percentage_of'" class="grid gap-3 sm:grid-cols-2">
            <label class="block">
              <span class="text-sm font-medium text-slate-300">Porcentagem</span>
              <input
                v-model.number="formulaValues.percentage"
                type="number"
                step="any"
                class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
              />
            </label>

            <label class="block">
              <span class="text-sm font-medium text-slate-300">Total</span>
              <input
                v-model.number="formulaValues.total"
                type="number"
                step="any"
                class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
              />
            </label>
          </div>

          <div v-if="formulaType === 'percentage_change'" class="grid gap-3 sm:grid-cols-2">
            <label class="block">
              <span class="text-sm font-medium text-slate-300">Inicial</span>
              <input
                v-model.number="formulaValues.initial"
                type="number"
                step="any"
                class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
              />
            </label>

            <label class="block">
              <span class="text-sm font-medium text-slate-300">Final</span>
              <input
                v-model.number="formulaValues.final"
                type="number"
                step="any"
                class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
              />
            </label>
          </div>

          <div v-if="formulaType === 'rule_of_three'" class="grid gap-3 sm:grid-cols-3">
            <label class="block">
              <span class="text-sm font-medium text-slate-300">A</span>
              <input
                v-model.number="formulaValues.a"
                type="number"
                step="any"
                class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
              />
            </label>

            <label class="block">
              <span class="text-sm font-medium text-slate-300">B</span>
              <input
                v-model.number="formulaValues.b"
                type="number"
                step="any"
                class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
              />
            </label>

            <label class="block">
              <span class="text-sm font-medium text-slate-300">C</span>
              <input
                v-model.number="formulaValues.c"
                type="number"
                step="any"
                class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
              />
            </label>
          </div>

          <div v-if="formulaType === 'bmi'" class="grid gap-3 sm:grid-cols-2">
            <label class="block">
              <span class="text-sm font-medium text-slate-300">Peso kg</span>
              <input
                v-model.number="formulaValues.weight"
                type="number"
                step="any"
                class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
              />
            </label>

            <label class="block">
              <span class="text-sm font-medium text-slate-300">Altura m</span>
              <input
                v-model.number="formulaValues.height"
                type="number"
                step="any"
                class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
              />
            </label>
          </div>

          <button
            type="submit"
            class="w-full rounded-xl bg-cyan-400 px-5 py-3 font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:opacity-60"
            :disabled="loading"
          >
            {{ loading ? 'Calculando...' : 'Calcular fórmula' }}
          </button>
        </form>

        <div v-if="formulaResult" class="mt-5 space-y-4">
          <div class="rounded-2xl border border-cyan-400/30 bg-cyan-400/10 p-5">
            <p class="text-sm text-cyan-200">{{ formulaLabels[formulaType] }}</p>
            <p class="mt-2 break-all font-mono text-2xl font-bold text-cyan-300">
              {{ formulaResult.result }}
            </p>
          </div>

          <p class="rounded-xl border border-slate-800 bg-slate-950 p-4 text-sm text-slate-300">
            {{ formulaResult.expression }}
          </p>

          <button
            type="button"
            class="rounded-xl border border-cyan-400 px-4 py-2 text-sm font-semibold text-cyan-300 transition hover:bg-cyan-400 hover:text-slate-950"
            @click="copyText(formulaCopyText)"
          >
            {{ copied ? 'Copiado!' : 'Copiar fórmula' }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>
