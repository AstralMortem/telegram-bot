<template>
    <div class="flex flex-row justify-start items-center gap-4">
        <img src="/img/gold_coin.png"/>
        <p class="text-white font-bold text-md">{{amount}}</p>
    </div>
</template>

<script setup lang="ts">
defineProps(['amount'])
</script>