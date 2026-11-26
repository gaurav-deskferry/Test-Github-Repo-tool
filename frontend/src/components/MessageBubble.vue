<script setup>
defineProps({ message: { type: Object, required: true }, emoji: String });
</script>

<template>
  <div class="bubble-row" :class="message.role">
    <div v-if="message.role === 'character'" class="avatar small">{{ emoji }}</div>
    <div class="bubble" data-testid="message" :data-role="message.role">
      {{ message.content }}
      <time class="muted">{{ new Date(message.created_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }) }}</time>
    </div>
  </div>
</template>
