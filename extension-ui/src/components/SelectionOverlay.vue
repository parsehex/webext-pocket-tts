<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue';

const emit = defineEmits<{
  (e: 'confirm', element: HTMLElement, text: string): void
  (e: 'cancel'): void
}>();

const hoveredElement = ref<HTMLElement | null>(null);
const highlighterStyle = ref({ top: '0px', left: '0px', width: '0px', height: '0px' });

function updateHighlight(target: HTMLElement) {
    const rect = target.getBoundingClientRect();
    // We need to account for scroll because the overlay is in a fixed container or standard flow inside shadow DOM
    // Actually, since this component is inside the shadow DOM, showing a highlight *over* the page requires
    // either using fixed positioning relative to viewport, or absolute relative to document.
    // simpler to just use fixed and getBoundingClientRect.

    highlighterStyle.value = {
        top: `${rect.top}px`,
        left: `${rect.left}px`,
        width: `${rect.width}px`,
        height: `${rect.height}px`
    };
}

function onMouseMove(e: MouseEvent) {
    const target = e.target as HTMLElement;
    // Ignored elements: The extension UI itself.
    // Since we are in Shadow DOM, e.target might be tricky if we listen on window.
    // We need to listen on the *host* document to capture page elements.

    // Check if target is part of our extension container
    if (target.closest('#tts-extension-root')) return;

    if (target !== hoveredElement.value) {
        hoveredElement.value = target;
        updateHighlight(target);
    }
}

function onClick(e: MouseEvent) {
    e.preventDefault();
    e.stopPropagation();

    if (hoveredElement.value) {
        emit('confirm', hoveredElement.value, hoveredElement.value.innerText);
    }
}

function onKeyDown(e: KeyboardEvent) {
    if (e.key === 'Escape') {
        emit('cancel');
    }
}

onMounted(() => {
    document.addEventListener('mousemove', onMouseMove, true);
    document.addEventListener('click', onClick, true); // Capture phase to prevent default links
    document.addEventListener('keydown', onKeyDown);
});

onUnmounted(() => {
    document.removeEventListener('mousemove', onMouseMove, true);
    document.removeEventListener('click', onClick, true);
    document.removeEventListener('keydown', onKeyDown);
});
</script>

<template>
  <div
    class="fixed pointer-events-none z-[9999] border-2 border-blue-500 bg-blue-500/20 transition-all duration-75 ease-out"
    :style="highlighterStyle"
  >
    <div class="absolute -top-6 left-0 bg-blue-500 text-white text-xs px-2 py-0.5 rounded-t">
      Click to select
    </div>
  </div>
</template>
