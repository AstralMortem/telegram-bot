<script setup lang="ts">
import UAvatar from '@/components/UI/UAvatar.vue';
import axios from '@/plugins/axios';
import { useUsersStore } from '@/stores/users';
import { type IUserList } from '@/types';
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import UCard from '../components/UI/UCard.vue'
import SilverAmount from '@/components/UI/SilverAmount.vue';
import GoldAmount from '@/components/UI/GoldAmount.vue';
import { Icon } from '@iconify/vue/dist/iconify.js';
import { useGoldStore } from '@/stores/gold';
const userStore = useUsersStore()
const route = useRoute()

const currentUser = ref<IUserList>()
const goldStore = useGoldStore()

onMounted(async ()=>{
  currentUser.value = (await axios.get(`/users/${route.params.id}`)).data
})

const wealth = computed(() => {
  if(currentUser.value){
    return (currentUser.value?.silver_amount + goldStore.price * currentUser.value?.gold_amount).toFixed(4)
  }
  return 0
  
})
</script>

<template>
  <div class="w-full h-full flex flex-col justify-start items-start gap-4">
    <tg-back-button @click="$router.go(-1)" />
    <UCard class="w-full flex flex-col items-center gap-2" v-if="currentUser">
      <UAvatar :image="currentUser.image_url" :username="currentUser.username"/>
      <p class="text-xl">{{ currentUser.username }}</p>
      <div class="flex flex-row items-center gap-2 text-2xl font-bold">
        <Icon icon="tdesign:wealth"/>
        <p>{{ wealth }}</p>
      </div>
    </UCard>
    <UCard class="w-full flex flex-row gap-4 justify-around">
      <GoldAmount :amount="currentUser?.gold_amount"/>
      <SilverAmount :amount="currentUser?.silver_amount"/>
    </UCard>
  </div>
</template>
