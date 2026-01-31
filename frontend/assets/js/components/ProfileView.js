// frontend/assets/js/components/ProfileView.js
import { $ } from "../utils/dom.js";

function show(id, yes) {
  const el = $(id);
  if (!el) return;
  el.classList[yes ? "remove" : "add"]("hidden");
}

function setText(id, value) {
  const el = $(id);
  if (el) el.textContent = value ?? "";
}

export function setProfileLoading(isLoading) {
  // Basic
  show("basicLoading", isLoading);
  show("basicDetails", !isLoading);

  // Enrollments
  show("joinLoading", isLoading);
  show("joinTableContainer", !isLoading);
}

export function renderStudentBasic(student) {
  setText("studentId", student?.id ?? "—");
  setText("studentName", student?.name ?? "—");
  setText("studentEmail", student?.email ?? "—");
  setText("studentYear", student?.year ?? "—");
}

export function renderEnrollmentCount(count) {
  const totalEl = $("totalEnrollments");
  if (totalEl) totalEl.textContent = `Total: ${count ?? 0}`;
}

export function renderEnrollmentsTable(rows) {
  const body = $("joinTableBody");
  if (body) body.innerHTML = "";

  if (!rows || rows.length === 0) {
    show("noEnrollments", true);
    return;
  }

  show("noEnrollments", false);

  rows.forEach((r) => {
    const tr = document.createElement("tr");
    tr.className = "border-b";
    tr.innerHTML = `
      <td class="px-3 py-2">${r.enrollment_id ?? "-"}</td>
      <td class="px-3 py-2">${r.course_title ?? "-"}</td>
      <td class="px-3 py-2">${r.course_code ?? r.code ?? "-"}</td>
      <td class="px-3 py-2">${r.teacher_name ?? "-"}</td>
      <td class="px-3 py-2">${r.fees ?? "-"}</td>
      <td class="px-3 py-2">${r.duration_weeks ?? "-"}</td>
      <td class="px-3 py-2">${r.enrolled_on ?? "-"}</td>
    `;
    body.appendChild(tr);
  });
}

export function renderProfileError() {
  setProfileLoading(false);
  renderEnrollmentCount(0);
}
