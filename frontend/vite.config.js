import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// In dev the API runs on :8000; `/api/*` is proxied there.
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: { "/api": "http://127.0.0.1:8000" },
  },
  test: { environment: "jsdom" },
});
