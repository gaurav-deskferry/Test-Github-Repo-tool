<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { api } from "../api/client";
import { useAuth } from "../stores/auth";
import StateBox from "../components/StateBox.vue";
import TagChip from "../components/TagChip.vue";

const props = defineProps({ id: String });
const auth = useAuth();
const router = useRouter();
const character = ref(null);
const status = ref("loading");
const error = ref("");
const starting = ref(false);

async function load() {
  status.value = "loading";
  try {
    character.value = await api.character(props.id);
    status.value = "ready";
  } catch (e) {
    error.value = e.message;
    status.value = e.status === 404 ? "missing" : "error";
  }
}
async function startChat() {
  if (!auth.isLoggedIn) return router.push({ name: "login", query: { redirect: `/characters/${props.id}` } });
  starting.value = true;
  try {
    const s = await api.createSession(character.value.id);
    router.push(`/chats/${s.id}`);
  } catch (e) {
    error.value = e.message;
  } finally {
    starting.value = false;
  }
}
onMounted(load);
</script>

<template>
  <RouterLink to="/characters" class="back">← All characters</RouterLink>
  <StateBox v-if="status === 'loading'" kind="loading" text="Loading…" />
  <StateBox v-else-if="status === 'missing'" title="Character not found" text="It may have been removed.">
    <RouterLink to="/characters" class="btn">Back to characters</RouterLink>
  </StateBox>
  <StateBox v-else-if="status === 'error'" kind="error" title="Couldn't load character" :text="error">
    <button class="btn" @click="load">Retry</button>
  </StateBox>
  <article v-else class="card detail">
    <div class="avatar large">{{ character.emoji }}</div>
    <div>
      <h1>{{ character.name }}</h1>
      <p class="tagline">{{ character.tagline }}</p>
      <p>{{ character.description }}</p>
      <h3>Personality</h3>
      <div class="chips"><TagChip v-for="p in character.personality" :key="p" :label="p" active /></div>
      <h3>Opens with</h3>
      <blockquote>“{{ character.greeting }}”</blockquote>
      <div class="chips"><TagChip v-for="t in character.tags" :key="t" :label="t" /></div>
      <p v-if="error" class="error" role="alert">{{ error }}</p>
      <button class="btn primary" data-testid="start-chat" :disabled="starting" @click="startChat">
        {{ auth.isLoggedIn ? (starting ? "Starting…" : "Start chat") : "Log in to chat" }}
      </button>
    </div>
  </article>
</template>
