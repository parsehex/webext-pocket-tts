// Background service worker
console.log('TTS Extension Background Service Worker Loaded');

chrome.action.onClicked.addListener((tab: chrome.tabs.Tab) => {
	if (tab.id) {
		chrome.tabs
			.sendMessage(tab.id, { action: 'toggle_ui' })
			.catch((err: unknown) => {
				// Content script might not be loaded yet or connection failed
				// For now just log, but in prod we might want to inject if missing
				console.warn('Could not send message to content script:', err);
			});
	}
});
