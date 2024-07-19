<script setup lang="ts">
import GoldAmount from '@/components/UI/GoldAmount.vue'
import SilverAmount from '@/components/UI/SilverAmount.vue'
import UButton from '@/components/UI/UButton.vue'
import UCard from '@/components/UI/UCard.vue'
import UModal from '@/components/UI/UModal.vue'
import UsersList from '@/components/Users/UsersList.vue'
import { useGoldStore } from '@/stores/gold'
import { storeToRefs } from 'pinia'
import { onMounted, ref } from 'vue'
import { useWebAppViewport } from 'vue-tg'

const goldStore = useGoldStore()
const { pending, price, amount } = storeToRefs(goldStore)
const showBuy = ref(false)
const showSell = ref(false)

const buyGold = (amount: number) => {
  console.log(amount)
}

const sellGold = (amount: number) => {
  console.log(amount)
}

onMounted(() => {
  useWebAppViewport().expand()
})
</script>

<template>
  <div class="w-full h-full flex flex-col justify-start items-center gap-6 flex-1">
    <p v-if="pending">Loading...</p>
    <UCard class="flex flex-row justify-between w-full text-lg font-bold" v-else>
      <div class="flex flex-col gap-2">
        <p>Market Cup:</p>
        <GoldAmount :amount="amount" />
      </div>
      <div class="flex flex-col gap-2">
        <p>Price</p>
        <SilverAmount :amount="price" />
      </div>
    </UCard>
    <div class="flex flex-row items-center gap-4">
      <UButton label="Buy" trailing-icon="raphael:arrowup" color="green" @click="showBuy = true" />
      <UButton
        label="Sell"
        trailing-icon="raphael:arrowdown"
        color="red"
        @click="showSell = true"
      />
    </div>

    <UModal v-show="showBuy" @cancel="showBuy = false" @confirm="buyGold" />
    <UModal v-show="showSell" @cancel="showSell = false" @confirm="sellGold" />

    <UCard class="w-full">
      <UsersList />
    </UCard>
  </div>
</template>
