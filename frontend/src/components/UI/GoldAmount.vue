<template>
  <div class="flex flex-row justify-start items-center gap-1">
    <p class="text-white font-bold text-xl">{{ $props.amount }}</p>
    <img src="/img/gold_coin.png" class="max-w-10 max-h-10" />
  </div>
</template>

<script setup lang="ts">
defineProps(['amount'])
</script>
