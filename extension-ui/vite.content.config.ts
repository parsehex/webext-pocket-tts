import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import tailwindcss from '@tailwindcss/vite';
import { resolve } from 'path';

export default defineConfig({
	plugins: [vue(), tailwindcss()],
	define: {
		'process.env': {}, // Fix for some libs relying on process
	},
	build: {
		emptyOutDir: false,
		outDir: 'dist',
		rollupOptions: {
			input: resolve(__dirname, 'src/content.ts'),
			output: {
				format: 'iife',
				entryFileNames: 'content.js',
				name: 'ContentScript',
				inlineDynamicImports: true,
				extend: true,
				globals: {
					chrome: 'chrome', // Treat chrome as global
				},
			},
		},
	},
});
