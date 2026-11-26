// The API lives under /api both behind the vite dev proxy and when FastAPI serves the build.
export const BASE = "/api";

export class ApiError extends Error {
  constructor(status, message) {
    super(message);
    this.status = status;
  }
}

let onUnauthorized = () => {};
export const setUnauthorizedHandler = (fn) => (onUnauthorized = fn);

export function getToken() {
  return localStorage.getItem("token");
}

export async function request(path, { method = "GET", json, form, auth = true } = {}) {
  const headers = {};
  if (auth && getToken()) headers.Authorization = `Bearer ${getToken()}`;
  let body;
  if (json !== undefined) {
    headers["Content-Type"] = "application/json";
    body = JSON.stringify(json);
  } else if (form) {
    body = new URLSearchParams(form);
  }
  const res = await fetch(BASE + path, { method, headers, body });
  if (res.status === 204) return null;
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    if (res.status === 401 && auth && getToken()) onUnauthorized();
    const detail = Array.isArray(data.detail) ? data.detail.map((d) => d.msg).join("; ") : data.detail;
    throw new ApiError(res.status, detail || `Request failed (${res.status})`);
  }
  return data;
}

export const api = {
  login: (username, password) => request("/auth/login", { method: "POST", form: { username, password }, auth: false }),
  register: (username, password) => request("/auth/register", { method: "POST", json: { username, password }, auth: false }),
  me: () => request("/auth/me"),
  characters: () => request("/characters", { auth: false }),
  character: (id) => request(`/characters/${id}`, { auth: false }),
  sessions: () => request("/sessions"),
  session: (id) => request(`/sessions/${id}`),
  createSession: (character_id) => request("/sessions", { method: "POST", json: { character_id } }),
  sendMessage: (id, content) => request(`/sessions/${id}/messages`, { method: "POST", json: { content } }),
  deleteSession: (id) => request(`/sessions/${id}`, { method: "DELETE" }),
};
