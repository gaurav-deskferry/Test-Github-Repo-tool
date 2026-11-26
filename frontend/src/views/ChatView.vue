<script setup>
import { nextTick, onMounted, ref } from "vue";
import { api } from "../api/client";
import MessageBubble from "../components/MessageBubble.vue";
import StateBox from "../components/StateBox.vue";

const props = defineProps({ id: String });
const session = ref(null);
const character = ref(null);
const status = ref("loading");
const error = ref("");
const draft = ref("");
const sending = ref(false);
const scroller = ref(null);

const scrollDown = () => nextTick(() => scroller.value && (scroller.value.scrollTop = scroller.value.scrollHeight));

async function load() {
  status.value = "loading";
  try {
    session.value = await api.session(props.id);
    character.value = await api.character(session.value.character_id);
    status.value = "ready";
    scrollDown();
  } catch (e) {
    error.value = e.message;
    status.value = e.status === 404 ? "missing" : "error";
  }
}
async function send() {
  const content = draft.value.trim();
  if (!content || sending.value) return;
  sending.value = true;
  error.value = "";
  try {
    session.value.messages.push(...(await api.sendMessage(props.id, content)));
    draft.value = "";
    scrollDown();
  } catch (e) {
    error.value = e.message; // draft is kept so the user can retry
  } finally {
    sending.value = false;
  }
}
onMounted(load);
</script>

<template>
  <RouterLink to="/chats" class="back">← My chats</RouterLink>
  <StateBox v-if="status === 'loading'" kind="loading" text="Loading chat…" />
  <StateBox v-else-if="status === 'missing'" title="Chat not found" text="It may have been deleted.">
    <RouterLink to="/chats" class="btn">Back to my chats</RouterLink>
  </StateBox>
  <StateBox v-else-if="status === 'error'" kind="error" title="Couldn't load chat" :text="error">
    <button class="btn" @click="load">Retry</button>
  </StateBox>
  <section v-else class="chat card">
    <header class="chat-head">
      <div class="avatar small">{{ character.emoji }}</div>
      <div>
        <strong>{{ character.name }}</strong>
        <div class="muted">{{ session.title }}</div>
      </div>
      <span class="badge" title="Replies are canned placeholders until a real model is connected.">🚧 placeholder replies</span>
    </header>
    <div ref="scroller" class="messages" role="log" aria-live="polite" aria-label="Conversation">
      <MessageBubble v-for="m in session.messages" :key="m.id" :message="m" :emoji="character.emoji" />
    </div>
    <p v-if="error" class="error" role="alert">{{ error }}</p>
    <form class="composer" @submit.prevent="send">
      <input v-model="draft" @input="error = ''" placeholder="Type a message…" aria-label="Message" maxlength="4000" :disabled="sending" />
      <button class="btn primary" :disabled="sending || !draft.trim()">{{ sending ? "Sending…" : "Send" }}</button>
    </form>
  </section>
</template>
