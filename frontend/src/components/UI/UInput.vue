<script setup lang="ts">
const model = defineModel({ default: null })
</script>

<template>
  <input
    v-model="model"
    type="number"
    class="relative block w-full disabled:cursor-not-allowed disabled:opacity-75 focus:outline-none border-0 form-input rounded-md placeholder-gray-400 dark:placeholder-gray-500 text-lg px-2.5 py-1.5 shadow-sm bg-white dark:bg-neutral-900 text-neutral-900 dark:text-white ring-1 ring-inset ring-gray-300 dark:ring-gray-700 focus:ring-2 focus:ring-primary-500 dark:focus:ring-primary-400"
  />
</template>
