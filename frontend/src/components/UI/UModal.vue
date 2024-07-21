<script setup lang="ts">
import { computed, ref } from 'vue'

defineEmits(['confirm', 'cancel'])
const props = defineProps(["transaction"])
import UButton from '@/components/UI/UButton.vue'
import UInput from './UInput.vue'
import GoldAmount from './GoldAmount.vue';
import SilverAmount from './SilverAmount.vue';
import { useGoldStore } from '@/stores/gold';

const goldStore = useGoldStore()


const input = ref<number>(0)

const convert = computed(()=>{
  if(props.transaction == "sell"){
    return input.value * goldStore.price
  }else{
    return (input.value / goldStore.price).toFixed(4)
  }
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
            <p class="text-lg">Please input your amount</p>
            <div class="flex flex-row gap-1 items-center justify-start w-fit flex-wrap">
              <div class="flex flex-row gap-1 justify-start">
                <img :src="$props.transaction == 'sell'?'/img/gold_coin.png':'/img/silver_coin.png'" class="w-10 h-10"/>
                <UInput v-model="input" />
              </div>
              <p class="text-lg font-bold">≈</p>
              <SilverAmount v-if="$props.transaction == 'sell'" :amount="convert"/>
              <GoldAmount  :amount="convert" v-else size="8"/>
            </div>
            
            <div class="flex flex-row justify-start gap-4">
              <UButton label="Confirm" color="green" @click="$emit('confirm', input)" :disabled="!input" />
              <UButton label="Cancel" color="red" @click="$emit('cancel'), (input = 0)" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
