import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
export default defineConfig({ plugins: [react()], base: '/static/', build: { outDir: 'dist', emptyOutDir: true }, server: { proxy: { '/auth': 'http://127.0.0.1:8000', '/courses': 'http://127.0.0.1:8000', '/tasks': 'http://127.0.0.1:8000', '/exams': 'http://127.0.0.1:8000', '/dashboard': 'http://127.0.0.1:8000' } } });
