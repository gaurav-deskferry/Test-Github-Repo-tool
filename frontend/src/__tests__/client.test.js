import { beforeEach, describe, expect, it, vi } from "vitest";
import { ApiError, request, setUnauthorizedHandler } from "../api/client";

const respond = (status, body) => vi.fn().mockResolvedValue({ status, ok: status < 400, json: async () => body });

describe("api client", () => {
  beforeEach(() => localStorage.clear());

  it("sends the bearer token", async () => {
    localStorage.setItem("token", "abc");
    globalThis.fetch = respond(200, []);
    await request("/sessions");
    expect(fetch.mock.calls[0][1].headers.Authorization).toBe("Bearer abc");
  });

  it("raises ApiError with the server detail", async () => {
    globalThis.fetch = respond(409, { detail: "Username already taken" });
    await expect(request("/auth/register", { method: "POST", json: {}, auth: false })).rejects.toThrow(ApiError);
    await expect(request("/x", { auth: false })).rejects.toMatchObject({ status: 409, message: "Username already taken" });
  });

  it("calls the unauthorized handler on 401 with a stored token", async () => {
    const h = vi.fn();
    setUnauthorizedHandler(h);
    localStorage.setItem("token", "expired");
    globalThis.fetch = respond(401, { detail: "Invalid or expired token" });
    await expect(request("/auth/me")).rejects.toThrow();
    expect(h).toHaveBeenCalled();
  });
});
