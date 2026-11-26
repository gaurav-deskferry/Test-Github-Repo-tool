<script setup>
import { onMounted, ref } from "vue";
import { api } from "../api/client";
import ConfirmDialog from "../components/ConfirmDialog.vue";
import StateBox from "../components/StateBox.vue";

const sessions = ref([]);
const characters = ref({});
const status = ref("loading");
const error = ref("");
const toDelete = ref(null);

async function load() {
  status.value = "loading";
  try {
    const [s, c] = await Promise.all([api.sessions(), api.characters()]);
    sessions.value = s.sort((a, b) => b.updated_at.localeCompare(a.updated_at));
    characters.value = Object.fromEntries(c.map((x) => [x.id, x]));
    status.value = "ready";
  } catch (e) {
    error.value = e.message;
    status.value = "error";
  }
}
async function confirmDelete() {
  const id = toDelete.value.id;
  try {
    await api.deleteSession(id);
    sessions.value = sessions.value.filter((s) => s.id !== id);
  } catch (e) {
    error.value = e.message;
  }
  toDelete.value = null;
}
onMounted(load);
</script>

<template>
  <h1>My chats</h1>
  <StateBox v-if="status === 'loading'" kind="loading" text="Loading your chats…" />
  <StateBox v-else-if="status === 'error'" kind="error" title="Couldn't load chats" :text="error">
    <button class="btn" @click="load">Retry</button>
  </StateBox>
  <StateBox v-else-if="!sessions.length" title="No chats yet" text="Pick a character to start your first conversation.">
    <RouterLink to="/characters" class="btn primary">Browse characters</RouterLink>
  </StateBox>
  <ul v-else class="list">
    <li v-for="s in sessions" :key="s.id" class="card row" data-testid="chat-item">
      <RouterLink :to="`/chats/${s.id}`" class="row-main">
        <div class="avatar small">{{ characters[s.character_id]?.emoji }}</div>
        <div>
          <strong>{{ s.title }}</strong>
          <div class="muted">{{ characters[s.character_id]?.name }} · {{ s.message_count }} messages · {{ new Date(s.updated_at).toLocaleString() }}</div>
        </div>
      </RouterLink>
      <button class="btn small danger-text" :aria-label="`Delete ${s.title}`" @click="toDelete = s">Delete</button>
    </li>
  </ul>
  <p v-if="error && status === 'ready'" class="error" role="alert">{{ error }}</p>
  <ConfirmDialog :open="!!toDelete" title="Delete this chat?" confirm-label="Delete"
                 :text="`“${toDelete?.title}” and its messages will be removed permanently.`"
                 @confirm="confirmDelete" @cancel="toDelete = null" />
</template>
