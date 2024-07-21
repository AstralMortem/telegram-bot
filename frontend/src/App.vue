<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useGoldStore } from './stores/gold';
import { onMounted } from 'vue';
import { useUsersStore } from './stores/users';

const goldStore = useGoldStore();
const userStore = useUsersStore()


onMounted(async ()=>{
  await goldStore.fetchGold()
  goldStore.bindEvents()
  userStore.bindEvents()
})
</script>

<template>
  <div class="flex w-screen h-screen p-2 bg-neutral-900 text-white">
    <RouterView />
  </div>

</template>

<style scoped>


</style>
