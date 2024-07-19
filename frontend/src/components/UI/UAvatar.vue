<script setup lang="ts">
defineProps(['username', 'image'])
</script>

<template>
  <div
    class="rounded-full w-14 h-14 flex justify-center items-center bg-white text-neutral-900 font-bold"
  >
    <img :src="$props.image" v-if="image" class="rounded-full"/>
    <p v-else-if="$props.username">
      {{ $props.username.slice(0, 2).toUpperCase() }}
    </p>
    <p v-else></p>
  </div>
</template>
