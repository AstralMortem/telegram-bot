<script setup lang="ts">
import GoldAmount from '@/components/UI/GoldAmount.vue'
import SilverAmount from '@/components/UI/SilverAmount.vue'
import UButton from '@/components/UI/UButton.vue'
import UCard from '@/components/UI/UCard.vue'
import UModal from '@/components/UI/UModal.vue'
import UModalBuy from '@/components/UI/UModalBuy.vue'
import UModalSell from '@/components/UI/UModalSell.vue'
import UsersList from '@/components/Users/UsersList.vue'
import axios from '@/plugins/axios'
import { useGoldStore } from '@/stores/gold'
import { useUsersStore } from '@/stores/users'
import { Icon } from '@iconify/vue/dist/iconify.js'
import { storeToRefs } from 'pinia'
import { onMounted, onUnmounted, ref } from 'vue'
import { useWebApp, useWebAppViewport } from 'vue-tg'

const goldStore = useGoldStore()
const { pending, price, amount } = storeToRefs(goldStore)
const userStore = useUsersStore()


const showBuy = ref(false)
const showSell = ref(false)
const showError = ref()


const buyGold = async (amount: number) => {
  if(userStore.current_user.silver_amount < amount){
    showError.value = "Not enough silver"
  }else{
    await axios.post('/buy_gold', {
      "user_id": userStore.current_user.id,
      "amount": amount
    }).then(async (resp)=>{
      showBuy.value = false
      userStore.setCurrentUser(resp.data)
    }).catch((err)=>{
      showError.value = err.details
    })
  }
}

const sellGold = async (amount: number) => {
  if(userStore.current_user.gold_amount < amount){
    showError.value = "Not enough gold"
  }else{
    await axios.post('/sell_gold', {
      "user_id": userStore.current_user.id,
      "amount": amount
    }).then(async (resp)=>{
      showSell.value = false
      userStore.setCurrentUser(resp.data)
    }).catch((err)=>{
      showError.value = err.details
    })
  }
}


onMounted(async () => {
  const tgApp = useWebApp().initDataUnsafe
  
  if(tgApp.user){
    await userStore.fetchUser(tgApp.user.id)
  }
  
  useWebAppViewport().expand()
})


</script>

<template>
  <div class="w-full h-full flex flex-col justify-start items-center gap-6 flex-1">
    <p v-if="pending">Loading...</p>
    <UCard class="flex flex-col justify-between w-full text-lg font-bold gap-4" v-else>
      <div class="flex flex-col gap-2 w-full items-center">
        <p class="self-start text-sm">Market Cup:</p>
        <p class="text-2xl text-wrap">{{ Math.round(amount) }} G</p>
      </div>
      <div class="flex flex-col gap-2">
        <p class="text-sm">Price: </p>
        <div class="flex flex-row items-center justify-around">
          <GoldAmount :amount="1" size="8"/>
          <Icon icon="streamline:equal-sign-solid"/>
          <SilverAmount :amount="price" />
        </div>
        
      </div>
    </UCard>
    <div class="flex flex-row items-center gap-4 w-full px-4">
      <UButton label="Buy" trailing-icon="raphael:arrowup" color="green" @click="showBuy = true" />
      <UButton
        label="Sell"
        trailing-icon="raphael:arrowdown"
        color="red"
        @click="showSell = true"
      />
    </div>

    <UModalBuy v-show="showBuy" @cancel="showBuy = false" @confirm="buyGold" transaction="buy" />
    <UModalSell v-show="showSell" @cancel="showSell = false" @confirm="sellGold" transaction="sell" />
    <tg-alert :message="showError" v-if="showError" @close="showError = undefined"/>
    <UCard class="w-full">
      <UsersList />
    </UCard>
  </div>
</template>
