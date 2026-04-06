<script setup lang="ts">
import { ref } from 'vue';
import PlayerMenu from './components/PlayerMenu.vue';
import SelectionOverlay from './components/SelectionOverlay.vue';

// State
type AppState = 'IDLE' | 'SELECTING' | 'PREVIEW' | 'LOADING' | 'PLAYING' | 'SETTINGS';
const currentState = ref<AppState>('IDLE');
const isVisible = ref(true);

// Selection Data
const selectedText = ref('');
const selectedElement = ref<HTMLElement | null>(null);

// Audio Data
const audioUrl = ref<string | null>(null);

// Settings
const ttsEndpoint = ref('http://localhost:8000/tts');

// Listen for toggle messages
if (typeof chrome !== 'undefined' && chrome.runtime) {
  chrome.runtime.onMessage.addListener((request) => {
    if (request.action === 'toggle_ui') {
      isVisible.value = !isVisible.value;
    }
  });
}

function startSelection() {
  currentState.value = 'SELECTING';
}

function handleClose() {
  isVisible.value = false;
}

function openSettings() {
  currentState.value = 'SETTINGS';
}

function saveSettings(newEndpoint: string) {
  ttsEndpoint.value = newEndpoint;
  if (typeof chrome !== 'undefined' && chrome.storage) {
    chrome.storage.local.set({ 'tts_endpoint': newEndpoint });
  }
  currentState.value = 'IDLE';
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

    const response = await fetch(ttsEndpoint.value, {
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
    const result = await chrome.storage.local.get([key, 'tts_endpoint']);

    if (result['tts_endpoint']) {
      ttsEndpoint.value = result['tts_endpoint'] as string;
    }

    if (result[key]) {
      const data = result[key] as { text: string; timestamp: number };
      selectedText.value = data.text;
      currentState.value = 'PREVIEW';
      isVisible.value = true; // Show if we have saved data? Or respect default?
      // User said "show extension badge if there's existing audio for a page",
      // but also "re-populate the menu".
      // We'll let the user toggle it open, but if open, show preview.
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
    <div v-if="isVisible" class="fixed top-4 right-4 z-50 flex flex-col items-end gap-2">
      <!-- Main Menu / Player -->
      <PlayerMenu :state="currentState" :initial-text="selectedText" :audio-url="audioUrl"
        :initial-endpoint="ttsEndpoint" @start-selection="startSelection" @generate-audio="handleGenerateAudio"
        @cancel="handleClose" @open-settings="openSettings" @save-settings="saveSettings" @reset="handleReset" />
    </div>
    <!-- Selection Overlay (Full Screen Helper) -->
    <SelectionOverlay v-if="isVisible && currentState === 'SELECTING'" @confirm="handleSelectionConfirmed"
      @cancel="handleCancelSelection" />
  </div>
</template>
<style>
/* Global styles for the shadow DOM context */
@import "tailwindcss";
</style>
