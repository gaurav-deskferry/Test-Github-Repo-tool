<script setup>
import { computed, onMounted, ref } from "vue";
import { api } from "../api/client";
import CharacterCard from "../components/CharacterCard.vue";
import StateBox from "../components/StateBox.vue";
import TagChip from "../components/TagChip.vue";

const characters = ref([]);
const status = ref("loading");
const error = ref("");
const query = ref("");
const activeTag = ref(null);

const tags = computed(() => [...new Set(characters.value.flatMap((c) => c.tags))].sort());
const filtered = computed(() => {
  const q = query.value.toLowerCase();
  return characters.value.filter(
    (c) =>
      (!activeTag.value || c.tags.includes(activeTag.value)) &&
      (!q || `${c.name} ${c.tagline}`.toLowerCase().includes(q)),
  );
});

async function load() {
  status.value = "loading";
  try {
    characters.value = await api.characters();
    status.value = "ready";
  } catch (e) {
    error.value = e.message;
    status.value = "error";
  }
}
function clearFilters() {
  query.value = "";
  activeTag.value = null;
}
onMounted(load);
</script>

<template>
  <h1>Pick a character</h1>
  <p class="muted">Browse the cast and start a conversation.</p>
  <StateBox v-if="status === 'loading'" kind="loading" text="Loading characters…" />
  <StateBox v-else-if="status === 'error'" kind="error" title="Couldn't load characters" :text="error">
    <button class="btn" @click="load">Retry</button>
  </StateBox>
  <template v-else>
    <div class="toolbar">
      <input v-model="query" type="search" placeholder="Search by name or tagline…" aria-label="Search characters" />
    </div>
    <div class="chips filter">
      <button class="plain" @click="activeTag = null"><TagChip label="all" :active="!activeTag" /></button>
      <button v-for="t in tags" :key="t" class="plain" :data-testid="`tag-${t}`" @click="activeTag = activeTag === t ? null : t">
        <TagChip :label="t" :active="activeTag === t" />
      </button>
    </div>
    <StateBox v-if="!filtered.length" title="No characters match" text="Try a different search or tag.">
      <button class="btn" @click="clearFilters">Clear filters</button>
    </StateBox>
    <div v-else class="grid">
      <CharacterCard v-for="c in filtered" :key="c.id" :character="c" />
    </div>
  </template>
</template>
