<script setup>
defineProps({ open: Boolean, title: String, text: String, confirmLabel: { type: String, default: "Confirm" } });
defineEmits(["confirm", "cancel"]);
</script>

<template>
  <div v-if="open" class="overlay" @click.self="$emit('cancel')">
    <div class="dialog" role="dialog" aria-modal="true">
      <h3>{{ title }}</h3>
      <p class="muted">{{ text }}</p>
      <div class="actions">
        <button class="btn" @click="$emit('cancel')">Cancel</button>
        <button class="btn danger" data-testid="confirm" @click="$emit('confirm')">{{ confirmLabel }}</button>
      </div>
    </div>
  </div>
</template>
