<script setup lang='ts'>
import GoldAmount from '@/components/UI/GoldAmount.vue';
import SilverAmount from '@/components/UI/SilverAmount.vue';
import UButton from '@/components/UI/UButton.vue';
import UCard from '@/components/UI/UCard.vue';
import UsersList from '@/components/Users/UsersList.vue';
import { useGoldStore } from '@/stores/gold';
import { storeToRefs } from 'pinia';
import { onMounted, ref } from 'vue';
import { useWebAppViewport } from 'vue-tg'

const goldStore = useGoldStore()
const {pending, price, amount} = storeToRefs(goldStore)
const showBuy = ref(false)

onMounted(()=>{
    useWebAppViewport().expand()
})

</script>

<template>
    <div class="w-full h-full flex flex-col justify-start items-center gap-6 flex-1">
        <p v-if="pending">Loading...</p>
        <div class="flex flex-row justify-evenly w-full" v-else>
            <UCard>
                <div class="flex flex-col gap-2">
                    <p>Циркуляційний запас:</p>
                    <GoldAmount :amount="amount"/>
                </div>
            </UCard>
            <UCard>
                <div class="flex flex-col gap-2">
                    <p>Ціна</p>
                    <SilverAmount :amoutn="price"/>
                </div>
            </UCard>
        </div>
        <div class="flex flex-row items-center gap-4">
            <UButton label="Buy" trailing-icon="raphael:arrowup" color="green" @click="showBuy = true"/>
            <UButton label="Sell" trailing-icon="raphael:arrowdown" color="red"/>

            
        </div>

        <UCard class="w-full">
            <UsersList/>
        </UCard>
    </div>
</template>