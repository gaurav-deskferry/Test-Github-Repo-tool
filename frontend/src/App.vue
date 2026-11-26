<script setup>
import DevBanner from "./components/DevBanner.vue";
import AppHeader from "./components/AppHeader.vue";
</script>

<template>
  <DevBanner />
  <AppHeader />
  <main class="container">
    <RouterView />
  </main>
</template>
