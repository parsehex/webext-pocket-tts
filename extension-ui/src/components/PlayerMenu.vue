<script setup lang="ts">
import { ref, watch, computed } from 'vue';

const props = defineProps<{
  state: 'IDLE' | 'SELECTING' | 'PREVIEW' | 'LOADING' | 'PLAYING' | 'SETTINGS';
  initialText: string;
  audioUrl: string | null;
  initialEndpoint?: string;
}>();

const emit = defineEmits<{
  (e: 'start-selection'): void
  (e: 'generate-audio', text: string): void
  (e: 'cancel'): void
  (e: 'reset'): void
  (e: 'open-settings'): void
  (e: 'save-settings', endpoint: string): void
}>();

const textContent = ref(props.initialText);
const endpointUrl = ref(props.initialEndpoint || 'http://localhost:8000/tts');
const timer = ref(0);
let timerInterval: number | null = null;

watch(() => props.initialText, (newText) => {
  textContent.value = newText;
});

watch(() => props.initialEndpoint, (newVal) => {
  if (newVal) endpointUrl.value = newVal;
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
      <div class="flex items-center gap-2">
        <button @click="emit('open-settings')" class="text-slate-400 hover:text-white" title="Settings">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path
              d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.38a2 2 0 0 0-.73-2.73l-.15-.1a2 2 0 0 1-1-1.72v-.51a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z">
            </path>
            <circle cx="12" cy="12" r="3"></circle>
          </svg>
        </button>
        <button @click="emit('reset')" class="text-slate-400 hover:text-white" title="Reset">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2v16M12 2H12"></path>
            <path d="M12 2v16M12 2H12"></path>
          </svg>
        </button>
        <button @click="emit('cancel')" class="text-slate-400 hover:text-white" title="Close">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
    </div>
    <!-- Content Area -->
    <div class="p-4">
      <!-- IDLE State -->
      <div v-if="state === 'IDLE'" class="text-center py-2">
        <p class="text-sm text-gray-500 mb-4">Select text on the page to read out loud.</p>
        <button @click="emit('start-selection')"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded transition-colors flex items-center justify-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"></path>
            <polyline points="13 2 13 9 20 9"></polyline>
          </svg> Select Text </button>
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
        <textarea v-model="textContent"
          class="w-full h-32 p-2 text-sm border border-gray-300 rounded focus:border-blue-500 focus:ring-1 focus:ring-blue-500 resize-none"></textarea>
        <button @click="handleSubmit"
          class="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded transition-colors flex items-center justify-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
            <path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path>
          </svg> Generate Audio </button>
      </div>
      <!-- LOADING State -->
      <div v-if="state === 'LOADING'" class="text-center py-6">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-200 border-t-blue-600 mb-3">
        </div>
        <p class="font-medium text-gray-700">Generating Audio...</p>
        <p class="text-sm text-gray-500 font-mono mt-1">{{ formattedTime }}</p>
      </div>
      <!-- PLAYING State -->
      <div v-if="state === 'PLAYING'" class="text-center">
        <audio controls :src="audioUrl || ''" class="w-full mb-3" autoplay></audio>
        <div class="flex justify-between">
          <button @click="emit('start-selection')" class="text-xs text-gray-500 hover:text-gray-800 underline">Redo
            Selection</button>
          <!-- Close in playing state just closes the whole thing? Or stops playback? -->
          <!-- User said X button should close menu. This Close button here could function same as X. -->
          <button @click="emit('cancel')" class="text-xs text-red-500 hover:text-red-700">Close</button>
        </div>
      </div>
      <!-- SETTINGS State -->
      <div v-if="state === 'SETTINGS'" class="flex flex-col gap-3">
        <label class="block text-sm font-medium text-gray-700">TTS Endpoint URL</label>
        <input v-model="endpointUrl" type="text" class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm shadow-sm placeholder-gray-400
            focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
          placeholder="http://localhost:8000/tts" />
        <div class="flex justify-end gap-2 mt-2">
          <button @click="emit('cancel')" class="px-3 py-1.5 text-xs text-gray-500 hover:text-gray-700">Cancel</button>
          <button @click="emit('save-settings', endpointUrl)"
            class="px-3 py-1.5 text-xs bg-blue-600 text-white rounded hover:bg-blue-700">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>
