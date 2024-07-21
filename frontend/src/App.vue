<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useGoldStore } from './stores/gold';
import { onMounted } from 'vue';

const goldStore = useGoldStore();


onMounted(async ()=>{
  await goldStore.fetchGold()
  goldStore.bindEvents()
})
</script>

<template>
  <div class="flex w-screen h-screen p-2 bg-neutral-900 text-white">
    <RouterView />
  </div>

</template>

<style scoped>


</style>
