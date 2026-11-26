<script setup>
import { useRouter } from "vue-router";
import { useAuth } from "../stores/auth";

const auth = useAuth();
const router = useRouter();
function logout() {
  auth.logout();
  router.push({ name: "characters" });
}
</script>

<template>
  <header class="app-header">
    <div class="container bar">
      <RouterLink to="/" class="brand">🎭 Character Cards</RouterLink>
      <nav>
        <RouterLink to="/characters">Characters</RouterLink>
        <RouterLink v-if="auth.isLoggedIn" to="/chats">My chats</RouterLink>
      </nav>
      <div class="user">
        <template v-if="auth.isLoggedIn">
          <span class="muted" data-testid="username">{{ auth.user?.username }}</span>
          <button class="btn small" @click="logout">Log out</button>
        </template>
        <RouterLink v-else to="/login" class="btn small primary">Log in</RouterLink>
      </div>
    </div>
  </header>
</template>
