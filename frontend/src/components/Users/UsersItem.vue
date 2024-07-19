<script setup lang="ts">
import { useGoldStore } from '@/stores/gold';
import type { IUserList } from '@/types';
import { computed, type PropType } from 'vue';
import SilverAmount from '../UI/SilverAmount.vue';

const goldStore = useGoldStore()

const props = defineProps({
    data: {type:{} as PropType<IUserList>, required:true}
})

const wealth = computed(()=>{
    return props.data.silver_amount + (goldStore.price * props.data.gold_amount)
})
</script>

<template>
    <RouterLink class="flex flex-row justify-between items-center gap-4 w-full bg-neutral-700 p-2 rounded-lg" :to="`/users/${$props.data.id}`">
        <div class="rounded-full w-14 h-14 flex justify-center items-center bg-white text-neutral-900 font-bold">
            {{$props.data.username.slice(0,2).toUpperCase()}}
        </div>
        <div class="flex flex-col justify-end items-end gap-1">
            <p class="text-white font-bold">{{ $props.data.username }}</p>
            <SilverAmount :amount="wealth"/>
        </div>

    </RouterLink>
</template>