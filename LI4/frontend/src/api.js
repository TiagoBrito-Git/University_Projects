export const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

const STORAGE_KEY = "sf_user";

function getToken() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) return null;
    const user = JSON.parse(stored);
    return user?.token || null;
  } catch {
    return null;
  }
}

function redirectLogin() {
  localStorage.removeItem(STORAGE_KEY);
  window.location.href = "/login";
}

export async function authFetch(url, options = {}) {
  const token = getToken();
  const res = await fetch(url, {
    ...options,
    headers: {
      ...(options.headers || {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
  });
  if (res.status === 401) {
    redirectLogin();
    throw new Error("Sessão expirada");
  }
  return res;
}

export function authHeaders() {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}
