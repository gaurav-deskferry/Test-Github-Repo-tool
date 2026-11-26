<script setup>
import TagChip from "./TagChip.vue";
defineProps({ character: { type: Object, required: true } });
</script>

<template>
  <RouterLink :to="`/characters/${character.id}`" class="card character-card" data-testid="character-card">
    <div class="avatar">{{ character.emoji }}</div>
    <h3>{{ character.name }}</h3>
    <p class="muted">{{ character.tagline }}</p>
    <div class="chips"><TagChip v-for="t in character.tags" :key="t" :label="t" /></div>
  </RouterLink>
</template>
