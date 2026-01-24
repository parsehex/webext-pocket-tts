<script setup lang="ts">
import { ref, watch, computed } from 'vue';

const props = defineProps<{
  state: 'IDLE' | 'SELECTING' | 'PREVIEW' | 'LOADING' | 'PLAYING';
  initialText: string;
  audioUrl: string | null;
}>();

const emit = defineEmits<{
  (e: 'start-selection'): void
  (e: 'generate-audio', text: string): void
  (e: 'cancel'): void
}>();

const textContent = ref(props.initialText);
const timer = ref(0);
let timerInterval: number | null = null;

watch(() => props.initialText, (newText) => {
    textContent.value = newText;
});

watch(() => props.state, (newState) => {
    if (newState === 'LOADING') {
        startTimer();
    } else if (newState === 'PLAYING' || newState === 'PREVIEW') {
        stopTimer();
    }
});

function startTimer() {
    timer.value = 0;
    timerInterval = setInterval(() => {
        timer.value += 0.1; // 100ms
    }, 100);
}

function stopTimer() {
    if (timerInterval) clearInterval(timerInterval);
    timerInterval = null;
}

const formattedTime = computed(() => {
    return timer.value.toFixed(1) + 's';
});

function handleSubmit() {
    emit('generate-audio', textContent.value);
}

</script>

<template>
  <div class="bg-white rounded-lg shadow-xl border border-gray-200 overflow-hidden w-80 flex flex-col transition-all">

    <!-- Header -->
    <div class="bg-slate-900 text-white px-4 py-3 flex justify-between items-center">
      <h1 class="font-bold text-sm">TTS Reader</h1>
      <button @click="emit('cancel')" class="text-slate-400 hover:text-white" title="Close">
        <!-- Close Icon -->
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
      </button>
    </div>

    <!-- Content Area -->
    <div class="p-4">

      <!-- IDLE State -->
      <div v-if="state === 'IDLE'" class="text-center py-2">
        <p class="text-sm text-gray-500 mb-4">Select text on the page to read out loud.</p>
        <button
          @click="emit('start-selection')"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded transition-colors flex items-center justify-center gap-2"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"></path><polyline points="13 2 13 9 20 9"></polyline></svg>
          Select Text
        </button>
      </div>

      <!-- SELECTING State -->
      <div v-if="state === 'SELECTING'" class="text-center py-2">
        <p class="text-sm font-medium text-blue-600 animate-pulse">Select an element on the page...</p>
        <p class="text-xs text-gray-400 mt-2">Click to confirm, Esc to cancel</p>
      </div>

      <!-- PREVIEW State -->
      <div v-if="state === 'PREVIEW'" class="flex flex-col gap-3">
        <div class="flex justify-between items-center">
             <label class="text-xs font-semibold text-gray-500 uppercase">Selected Text</label>
             <span class="text-xs text-gray-400">{{ textContent.length }} chars</span>
        </div>
        <textarea
          v-model="textContent"
          class="w-full h-32 p-2 text-sm border border-gray-300 rounded focus:border-blue-500 focus:ring-1 focus:ring-blue-500 resize-none"
        ></textarea>
        <button
          @click="handleSubmit"
          class="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded transition-colors flex items-center justify-center gap-2"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>
          Generate Audio
        </button>
      </div>

      <!-- LOADING State -->
      <div v-if="state === 'LOADING'" class="text-center py-6">
         <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-200 border-t-blue-600 mb-3"></div>
         <p class="font-medium text-gray-700">Generating Audio...</p>
         <p class="text-sm text-gray-500 font-mono mt-1">{{ formattedTime }}</p>
      </div>

       <!-- PLAYING State -->
       <div v-if="state === 'PLAYING'" class="text-center">
          <audio controls :src="audioUrl || ''" class="w-full mb-3" autoplay></audio>
          <div class="flex justify-between">
              <button @click="emit('start-selection')" class="text-xs text-gray-500 hover:text-gray-800 underline">Redo Selection</button>
              <button @click="emit('cancel')" class="text-xs text-red-500 hover:text-red-700">Close</button>
          </div>
       </div>

    </div>
  </div>
</template>
