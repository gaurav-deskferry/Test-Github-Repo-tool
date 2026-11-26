<script setup>
defineProps({ label: String, active: Boolean });
</script>

<template>
  <span class="chip" :class="{ active }">{{ label }}</span>
</template>
