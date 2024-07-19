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
  }
})

const computedColor = computed(() => {
  switch(props.color){
    case "white": return "bg-white text-neutral-900";
    default: return "bg-white text-neutral-900";
  }
})
</script>

<template>
  <div class="px-3 py-2.5 font-bold rounded-md flex flex-row justify-start items-center gap-2" :class=[computedColor]>
    <Icon v-if="$props.leadingIcon" :icon="$props.leadingIcon"/>
    <p>{{ $props.label }}</p>
    <Icon v-if="$props.trailingIcon" :icon="$props.trailingIcon" />
  </div>
</template>
