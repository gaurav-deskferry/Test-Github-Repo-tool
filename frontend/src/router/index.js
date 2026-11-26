import { createRouter, createWebHistory } from "vue-router";
import { useAuth } from "../stores/auth";
import { setUnauthorizedHandler } from "../api/client";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/characters" },
    { path: "/login", name: "login", component: () => import("../views/LoginView.vue"), meta: { guest: true } },
    { path: "/characters", name: "characters", component: () => import("../views/CharactersView.vue") },
    { path: "/characters/:id", name: "character", component: () => import("../views/CharacterDetailView.vue"), props: true },
    { path: "/chats", name: "chats", component: () => import("../views/ChatsView.vue"), meta: { auth: true } },
    { path: "/chats/:id", name: "chat", component: () => import("../views/ChatView.vue"), props: true, meta: { auth: true } },
    { path: "/:rest(.*)*", name: "not-found", component: () => import("../views/NotFoundView.vue") },
  ],
});

router.beforeEach(async (to) => {
  const auth = useAuth();
  if (to.meta.auth && !auth.isLoggedIn) return { name: "login", query: { redirect: to.fullPath } };
  if (to.meta.guest && auth.isLoggedIn) return { name: "characters" };
  if (auth.isLoggedIn) {
    try {
      await auth.loadUser();
    } catch {
      auth.logout();
      if (to.meta.auth) return { name: "login", query: { redirect: to.fullPath } };
    }
  }
});

// Expired/invalid token on any API call -> back to login.
setUnauthorizedHandler(() => {
  useAuth().logout();
  router.push({ name: "login", query: { redirect: router.currentRoute.value.fullPath } });
});

export default router;
