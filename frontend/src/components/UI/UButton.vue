<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({
    color:{
        type: String,
        default: "white"
    }
})

const colorComp = computed(()=>{
    switch (props.color) {
        case "white":
            return "text-slate-900 bg-white"

        


        default:
            return "text-slate-900 bg-white";
    }
})

</script>

<template>
    <div class="flex justify-start w-max py-2.5 px-3 rounded-lg" :class="[colorComp]">
        <slot/>
    </div>
</template>