<script setup lang="ts">
import { ref } from 'vue'

defineEmits(['confirm', 'cancel'])
import UButton from '@/components/UI/UButton.vue'
import UInput from './UInput.vue'

const input = ref()
</script>

<template>
  <div class="relative z-50">
    <div class="fixed inset-0 transition-opacity bg-gray-200/75 dark:bg-neutral-800/75"></div>
    <div class="fixed inset-0 overflow-y-auto">
      <div class="flex min-h-full items-center justify-center text-center p-4 sm:p-0">
        <div
          class="relative text-left rtl:text-right flex flex-col bg-white dark:bg-neutral-900 shadow-xl w-full sm:max-w-lg rounded-lg sm:my-8"
        >
          <div class="flex flex-col p-4 gap-4">
            <p class="text-lg">Please input your amount</p>
            <UInput v-model="input" />
            <div class="flex flex-row justify-start gap-4">
              <UButton label="Confirm" color="green" @click="$emit('confirm', input)" />
              <UButton label="Cancel" color="red" @click="$emit('cancel'), (input = 0)" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
