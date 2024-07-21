<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { computed } from 'vue';
const props = defineProps({
  leadingIcon: String,
  trailingIcon: String,
  label: {
    type: String,
    required: true
  },
  color: {
    type: String,
    default: 'white'
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const computedColor = computed(() => {
  switch(props.color){
    case "white": return "bg-white text-neutral-900";
    case "red": return "bg-red-500 text-white";
    case "green": return "bg-green-500 text-white"
    default: return "bg-white text-neutral-900";
  }
})

const disabledClass = computed(()=>{
  if(props.disabled){
    return "pointer-events-none bg-neutral-600 opacity-70 cursor-none"
  }
})
</script>

<template>
  <div class="px-3 py-2.5 font-bold rounded-md flex flex-row justify-center items-center gap-2 w-full" :class="[computedColor, disabledClass]">
    <Icon v-if="$props.leadingIcon" :icon="$props.leadingIcon"/>
    <p>{{ $props.label }}</p>
    <Icon v-if="$props.trailingIcon" :icon="$props.trailingIcon" />
  </div>
</template>
