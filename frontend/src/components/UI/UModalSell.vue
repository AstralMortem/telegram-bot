<script setup lang="ts">
import { computed, ref, watch } from 'vue'

defineEmits(['confirm', 'cancel'])
const props = defineProps(["transaction"])
import UButton from '@/components/UI/UButton.vue'
import UInput from './UInput.vue'
import GoldAmount from './GoldAmount.vue';
import SilverAmount from './SilverAmount.vue';
import { useGoldStore } from '@/stores/gold';

const goldStore = useGoldStore()

const goldAmount = ref<number>(0)

const silverAmount = computed({
    get(){
        return goldAmount.value * goldStore.price
    },
    set(value){
      goldAmount.value = value / goldStore.price
    }
})

watch(goldAmount, (newVal)=>{
  silverAmount.value = newVal * goldStore.price
})

watch(silverAmount, (newVal)=>{
  goldAmount.value = newVal / goldStore.price
})

</script>

<template>
  <div class="relative z-50">
    <div class="fixed inset-0 transition-opacity bg-gray-200/75 dark:bg-neutral-800/75"></div>
    <div class="fixed inset-0 overflow-y-auto">
      <div class="flex min-h-full items-center justify-center text-center p-4 sm:p-0">
        <div
          class=" relative text-left rtl:text-right flex flex-col bg-white dark:bg-neutral-900 shadow-xl w-full sm:max-w-lg rounded-lg sm:my-8"
        >
          <div class="flex flex-col p-4 gap-4">
            <p class="text-lg flex items-center">How much <span>
              <img src='/img/gold_coin.png' class="w-10 h-10 mx-1"/>
            </span> you want to sell?</p>
            <div class="flex flex-row gap-1 items-center justify-start w-fit flex-wrap">
              
              <div class="flex flex-row gap-1 justify-start">
                <img src='/img/gold_coin.png' class="w-10 h-10"/>
                <UInput v-model="goldAmount" />
              </div>
              <p class="text-lg font-bold">≈</p>
              <div class="flex flex-row gap-1 justify-start">
                <img src='/img/silver_coin.png' class="w-10 h-10"/>
                <UInput v-model="silverAmount"/>
              </div>
            </div>
            
            <div class="flex flex-row justify-start gap-4">
              <UButton label="Confirm" color="green" @click="$emit('confirm', goldAmount)" :disabled="!silverAmount || !goldAmount" />
              <UButton label="Cancel" color="red" @click="$emit('cancel'), (silverAmount = 0)" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
