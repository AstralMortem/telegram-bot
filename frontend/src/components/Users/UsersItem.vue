<script setup lang="ts">
import { useGoldStore } from '@/stores/gold'
import type { IUserList } from '@/types'
import { computed, type PropType } from 'vue'
import SilverAmount from '../UI/SilverAmount.vue'
import { useWebApp } from 'vue-tg'
import UAvatar from '../UI/UAvatar.vue'
import GoldAmount from '../UI/GoldAmount.vue'
import { Icon } from '@iconify/vue/dist/iconify.js'

const goldStore = useGoldStore()

const props = defineProps({
  data: { type: {} as PropType<IUserList>, required: true },
  me: Boolean
})

const wealth = computed(() => {
  return (props.data.silver_amount + goldStore.price * props.data.gold_amount).toFixed(4)
})

</script>

<template>
  <RouterLink
    class="flex flex-row justify-between items-center gap-4 w-full bg-neutral-700 p-2 rounded-lg"
    :to="`/users/${$props.data.id}`"
  >
    <UAvatar :username="$props.data.username" :image="$props.data.image_url" />
    <div class="flex flex-col justify-end items-end gap-1">
      <p class="text-white font-bold">
        {{ $props.data.username }} <span v-if="$props.me">(Me)</span>
      </p>
      <div class="flex flex-col gap-1 items-end">
        
        <div class="flex flex-row justify-end items-center gap-2 " v-if="$props.me">
          <SilverAmount :amount="$props.data.silver_amount" size="5" class="text-base text-neutral-300"/>
          <GoldAmount :amount="$props.data.gold_amount" size="5" class="text-base text-neutral-300"/>
        </div>
        <div class="flex flex-row items-center gap-2 text-2xl font-bold">
          <p>{{ wealth }}</p>
          <Icon icon="tdesign:wealth"/>
        </div>
      </div>
      
    </div>
  </RouterLink>
</template>
