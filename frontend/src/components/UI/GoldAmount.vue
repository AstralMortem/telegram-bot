<template>
    <div class="flex flex-row justify-start items-center gap-1">
        <img src="/img/gold_coin.png" class="max-w-10 max-h-10"/>
        <p class="text-white font-bold text-md">{{$props.amount}}</p>
    </div>
</template>

<script setup lang="ts">
defineProps(['amount'])
</script>