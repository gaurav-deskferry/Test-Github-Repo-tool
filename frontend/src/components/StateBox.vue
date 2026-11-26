<script setup>
// Loading / error / empty placeholder used by every list or detail view.
defineProps({ kind: { type: String, default: "empty" }, title: String, text: String });
</script>

<template>
  <div class="state-box" :class="kind" :role="kind === 'error' ? 'alert' : 'status'">
    <div v-if="kind === 'loading'" class="spinner" aria-hidden="true"></div>
    <h3 v-if="title">{{ title }}</h3>
    <p v-if="text" class="muted">{{ text }}</p>
    <slot />
  </div>
</template>
