<script setup>
import { ref } from "vue";
const hidden = ref(sessionStorage.getItem("devBannerHidden") === "1");
function dismiss() {
  hidden.value = true;
  sessionStorage.setItem("devBannerHidden", "1");
}
</script>

<template>
  <div v-if="!hidden" class="dev-banner" role="status" data-testid="dev-banner">
    <span>🚧 <strong>Under development</strong> — character replies are placeholders and features may change.</span>
    <button class="link" aria-label="Dismiss banner" @click="dismiss">✕</button>
  </div>
</template>
