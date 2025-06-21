import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',  // Expose on all network interfaces
    port: 5173,        // Ensure Vite is running on the expected port
    watch: {
      usePolling: true,
    }
  }
})
