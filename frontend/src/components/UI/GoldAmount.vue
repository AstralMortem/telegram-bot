<template>
  <div class="flex flex-row justify-start items-center gap-2 text-xl text-white">
    <p class=" font-bold ">{{ $props.amount }}</p>
    <img src="/img/gold_coin.png" :class="[compSize]" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps(['amount', 'size'])

const compSize = computed(()=>{
  switch (props.size){
    case "5": return "w-5 h-5";
    case "10": return "w-10 h-10"
    case "12": return "w-12 h-12"
    case "8": return "w-8 h-8"
    default: return "w-10 h-10"
  }
})
</script>
