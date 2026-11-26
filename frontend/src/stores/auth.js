import { defineStore } from "pinia";
import { api } from "../api/client";

export const useAuth = defineStore("auth", {
  state: () => ({ token: localStorage.getItem("token"), user: null }),
  getters: { isLoggedIn: (s) => !!s.token },
  actions: {
    async login(username, password) {
      const { access_token } = await api.login(username, password);
      this.token = access_token;
      localStorage.setItem("token", access_token);
      this.user = await api.me();
    },
    async register(username, password) {
      await api.register(username, password);
      await this.login(username, password);
    },
    async loadUser() {
      if (this.token && !this.user) this.user = await api.me();
    },
    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem("token");
    },
  },
});
