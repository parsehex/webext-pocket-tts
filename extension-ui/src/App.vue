<script setup lang="ts">
import { ref } from 'vue';
import PlayerMenu from './components/PlayerMenu.vue';
import SelectionOverlay from './components/SelectionOverlay.vue';

// State
type AppState = 'IDLE' | 'SELECTING' | 'PREVIEW' | 'LOADING' | 'PLAYING';
const currentState = ref<AppState>('IDLE');

// Selection Data
const selectedText = ref('');
const selectedElement = ref<HTMLElement | null>(null);

// Audio Data
const audioUrl = ref<string | null>(null);

function startSelection() {
  currentState.value = 'SELECTING';
}

function handleSelectionConfirmed(element: HTMLElement, text: string) {
  selectedElement.value = element;
  selectedText.value = text;
  currentState.value = 'PREVIEW';
}

function handleCancelSelection() {
  currentState.value = 'IDLE';
  selectedElement.value = null;
  selectedText.value = '';
}

async function handleGenerateAudio(text: string) {
  currentState.value = 'LOADING';
  // TODO: Implement API call with timer
  // signal loading start

  try {
      const formData = new FormData();
      formData.append('text', text);

      const response = await fetch('http://localhost:8000/tts', {
          method: 'POST',
          body: formData
      });

      if (!response.ok) throw new Error('TTS Failed');

      const blob = await response.blob();
      audioUrl.value = URL.createObjectURL(blob);
      currentState.value = 'PLAYING';

      // Save state
      saveState(text);

  } catch (e) {
      console.error(e);
      alert('Failed to generate audio');
      currentState.value = 'PREVIEW';
  }
}

function saveState(text: string) {
    if (typeof chrome !== 'undefined' && chrome.storage) {
        const key = window.location.href;
        chrome.storage.local.set({ [key]: { text, timestamp: Date.now() } });
    }
}

async function loadState() {
    if (typeof chrome !== 'undefined' && chrome.storage) {
        const key = window.location.href;
        const result = await chrome.storage.local.get(key);
        if (result[key]) {
            const data = result[key] as { text: string; timestamp: number };
            selectedText.value = data.text;
            currentState.value = 'PREVIEW';
            // We don't auto-generate audio to save bandwidth/noise, user can click "Generate"
            // Or we could show a "Saved" badge. available in PlayerMenu logic mostly.
        }
    }
}

import { onMounted } from 'vue';
onMounted(() => {
    loadState();
});

function handleReset() {
    currentState.value = 'IDLE';
    selectedText.value = '';
    selectedElement.value = null;
    audioUrl.value = null;
    // Optional: Clear storage? Or keep it as history? User said "re-populate", likely keep.
}

</script>

<template>
  <div class="font-sans text-base text-gray-900 antialiased leading-normal">
    <!-- UI Container (Fixed Position) -->
    <div class="fixed top-4 right-4 z-50 flex flex-col items-end gap-2">

      <!-- Main Menu / Player -->
      <PlayerMenu
        :state="currentState"
        :initial-text="selectedText"
        :audio-url="audioUrl"
        @start-selection="startSelection"
        @generate-audio="handleGenerateAudio"
        @cancel="handleReset"
      />

    </div>

    <!-- Selection Overlay (Full Screen Helper) -->
    <SelectionOverlay
      v-if="currentState === 'SELECTING'"
      @confirm="handleSelectionConfirmed"
      @cancel="handleCancelSelection"
    />
  </div>
</template>

<style>
/* Global styles for the shadow DOM context */
@import "tailwindcss";
</style>
