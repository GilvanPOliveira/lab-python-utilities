<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    modelValue: number
    label: string
    min?: number
    max?: number
    step?: number
    suffix?: string
  }>(),
  {
    step: 1,
    suffix: '',
  },
)

const emit = defineEmits<{
  'update:modelValue': [value: number]
}>()

function clamp(value: number) {
  if (props.min !== undefined && value < props.min) return props.min
  if (props.max !== undefined && value > props.max) return props.max
  return value
}

function update(value: number) {
  if (Number.isNaN(value)) return
  emit('update:modelValue', clamp(value))
}

function adjust(direction: 1 | -1) {
  update(Number(props.modelValue || 0) + props.step * direction)
}
</script>

<template>
  <label class="block">
    <span class="text-sm font-medium text-slate-300">{{ label }}</span>

    <div class="number-control mt-2 grid min-h-12 grid-cols-[44px_1fr_44px] overflow-hidden rounded-md border border-white/10 bg-[#0b1020] transition focus-within:border-teal-300 focus-within:ring-2 focus-within:ring-teal-300/20">
      <button
        type="button"
        class="min-h-0 rounded-none border-r border-white/10 px-0 text-lg font-bold text-slate-300 transition hover:bg-white/[0.06] hover:text-white"
        :aria-label="`Diminuir ${label}`"
        @click="adjust(-1)"
      >
        -
      </button>

      <div class="flex min-w-0 items-center">
        <input
          :value="modelValue"
          type="number"
          :min="min"
          :max="max"
          :step="step"
          class="h-full min-h-12 w-full border-0 bg-transparent px-3 text-center font-mono text-base font-semibold text-white outline-none"
          @input="update(Number(($event.target as HTMLInputElement).value))"
        />
        <span v-if="suffix" class="pr-3 text-xs font-semibold uppercase tracking-[0.12em] text-slate-500">
          {{ suffix }}
        </span>
      </div>

      <button
        type="button"
        class="min-h-0 rounded-none border-l border-white/10 px-0 text-lg font-bold text-slate-300 transition hover:bg-white/[0.06] hover:text-white"
        :aria-label="`Aumentar ${label}`"
        @click="adjust(1)"
      >
        +
      </button>
    </div>
  </label>
</template>
