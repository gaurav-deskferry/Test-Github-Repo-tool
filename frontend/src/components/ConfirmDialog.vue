<script setup>
import { nextTick, ref, watch } from "vue";

const props = defineProps({ open: Boolean, title: String, text: String, confirmLabel: { type: String, default: "Confirm" } });
const emit = defineEmits(["confirm", "cancel"]);
const dialog = ref(null);
const cancelBtn = ref(null);
const uid = `dlg-${Math.random().toString(36).slice(2, 8)}`;
let opener = null;

watch(
  () => props.open,
  async (open) => {
    if (open) {
      opener = document.activeElement;
      await nextTick();
      cancelBtn.value?.focus();
    } else {
      opener?.focus?.();
      opener = null;
    }
  },
);

function onKeydown(e) {
  if (e.key === "Escape") {
    e.stopPropagation();
    emit("cancel");
  } else if (e.key === "Tab") {
    const items = dialog.value.querySelectorAll("button");
    const first = items[0];
    const last = items[items.length - 1];
    if (e.shiftKey && document.activeElement === first) (e.preventDefault(), last.focus());
    else if (!e.shiftKey && document.activeElement === last) (e.preventDefault(), first.focus());
  }
}
</script>

<template>
  <div v-if="open" class="overlay" @click.self="$emit('cancel')">
    <div ref="dialog" class="dialog" role="dialog" aria-modal="true" :aria-labelledby="`${uid}-t`" :aria-describedby="`${uid}-d`" @keydown="onKeydown">
      <h3 :id="`${uid}-t`">{{ title }}</h3>
      <p :id="`${uid}-d`" class="muted">{{ text }}</p>
      <div class="actions">
        <button ref="cancelBtn" class="btn" @click="$emit('cancel')">Cancel</button>
        <button class="btn danger" data-testid="confirm" @click="$emit('confirm')">{{ confirmLabel }}</button>
      </div>
    </div>
  </div>
</template>
