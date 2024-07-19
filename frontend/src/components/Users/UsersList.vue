<script setup lang="ts">
import { useUsersStore } from '@/stores/users'
import { storeToRefs } from 'pinia'
import { onMounted, onUnmounted, ref } from 'vue'
import UsersItem from './UsersItem.vue'

const userStore = useUsersStore()
const { pending, getUsers, current_user } = storeToRefs(userStore)
const scrollComponent = ref()
const handleScroll = async () => {
  let element = scrollComponent.value
  if (element.getBoundingClientRect().bottom < window.innerHeight) {
    await userStore.fetchUsers()
  }
}

onMounted(async () => {
  await userStore.fetchMe()
  await userStore.fetchUsers()
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<template>
  <div class="w-full h-min overflow-auto flex flex-col gap-3" ref="scrollComponent">
    <UsersItem :data="current_user" class="bg-green-600 mb-2" me />
    <hr/>
    <p v-if="pending">Loading...</p>
    <UsersItem v-else v-for="data in getUsers" :key="data.id" :data="data" />
  </div>
</template>
