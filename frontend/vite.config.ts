import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  base: '/static/',
  server: {
    port: 5173,
    strictPort: true, // Vite видасть помилку, якщо порт зайнятий, а не перестрибне на 5174
  }
})
