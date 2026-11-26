<script setup>
import { computed, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuth } from "../stores/auth";

const auth = useAuth();
const route = useRoute();
const router = useRouter();
const mode = ref("login");
const username = ref("");
const password = ref("");
const error = ref("");
const busy = ref(false);
const isRegister = computed(() => mode.value === "register");

function switchMode(m) {
  mode.value = m;
  error.value = "";
}
function useDemo() {
  username.value = "demo";
  password.value = "demo1234";
  mode.value = "login";
}
async function submit() {
  error.value = "";
  if (username.value.length < 3) return (error.value = "Username must be at least 3 characters.");
  if (password.value.length < 8) return (error.value = "Password must be at least 8 characters.");
  busy.value = true;
  try {
    await (isRegister.value ? auth.register : auth.login)(username.value, password.value);
    router.push(route.query.redirect || "/characters");
  } catch (e) {
    error.value = e.message;
  } finally {
    busy.value = false;
  }
}
</script>

<template>
  <section class="auth-card card">
    <h1>{{ isRegister ? "Create your account" : "Welcome back" }}</h1>
    <p class="muted">{{ isRegister ? "Sign up to chat with characters." : "Log in to see your chats." }}</p>
    <div class="tabs" role="tablist">
      <button role="tab" :class="{ active: !isRegister }" @click="switchMode('login')">Log in</button>
      <button role="tab" :class="{ active: isRegister }" @click="switchMode('register')">Sign up</button>
    </div>
    <form @submit.prevent="submit">
      <label>Username
        <input v-model.trim="username" name="username" autocomplete="username" required />
      </label>
      <label>Password
        <input v-model="password" name="password" type="password" required
               :autocomplete="isRegister ? 'new-password' : 'current-password'" />
      </label>
      <p v-if="error" class="error" role="alert">{{ error }}</p>
      <button class="btn primary block" :disabled="busy">{{ busy ? "Please wait…" : isRegister ? "Sign up" : "Log in" }}</button>
    </form>
    <p class="muted center">Just exploring? <button class="link" type="button" data-testid="use-demo" @click="useDemo">Use the demo account</button></p>
  </section>
</template>
