<script setup lang="ts">
import { useGoldStore } from '@/stores/gold'
import type { IUserList } from '@/types'
import { computed, type PropType } from 'vue'
import SilverAmount from '../UI/SilverAmount.vue'
import { useWebApp } from 'vue-tg'
import UAvatar from '../UI/UAvatar.vue'
import GoldAmount from '../UI/GoldAmount.vue'

const goldStore = useGoldStore()

const props = defineProps({
  data: { type: {} as PropType<IUserList>, required: true },
  me: Boolean
})

const wealth = computed(() => {
  return props.data.silver_amount + goldStore.price * props.data.gold_amount
})

const tgApp = useWebApp()
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
      <SilverAmount :amount="wealth" />
    </div>
  </RouterLink>
</template>
