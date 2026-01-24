import { createApp } from 'vue';
import App from './App.vue';
import mainStyle from './style.css?inline';

console.log('TTS Extension Content Script Loaded');

// Function to inject the Vue app
function injectApp() {
	const id = 'tts-extension-root';
	if (document.getElementById(id)) return;

	const container = document.createElement('div');
	container.id = id;
	document.body.appendChild(container);

	// Create shadow root to isolate styles
	const shadowRoot = container.attachShadow({ mode: 'open' });

	// Inject styles
	const styleTag = document.createElement('style');
	styleTag.textContent = mainStyle;
	shadowRoot.appendChild(styleTag);

	const appRoot = document.createElement('div');
	appRoot.id = 'app';
	shadowRoot.appendChild(appRoot);

	const app = createApp(App);
	app.mount(appRoot);
}

// Listen for messages from background script
chrome.runtime.onMessage.addListener(
	(
		request: { action: string },
		_sender: chrome.runtime.MessageSender,
		_sendResponse: (response?: any) => void,
	) => {
		if (request.action === 'toggle_ui') {
			injectApp();
		}
	},
);
