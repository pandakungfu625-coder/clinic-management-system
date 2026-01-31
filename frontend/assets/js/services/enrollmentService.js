// frontend/assets/js/services/enrollmentService.js

const API_URL = "/api/enrollments";

async function safeJson(res) {
  try { return await res.json(); } catch { return null; }
}

export async function apiGetAll() {
  const res = await fetch(API_URL);
  if (!res.ok) return [];
  return safeJson(res);
}

export function apiCreate(data) {
  return fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
}

export function apiDelete(id) {
  return fetch(`${API_URL}/${id}`, { method: "DELETE" });
}