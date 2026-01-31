import { $ } from "../utils/dom.js";
import { deleteEnrollmentAction } from "../controllers/enrollmentController.js";

export function renderEnrollmentTable(enrollments) {
  const body = $("enrollmentsTableBody");
  const empty = $("noEnrollments");

  body.innerHTML = "";

  if (!enrollments || enrollments.length === 0) {
    empty.classList.remove("hidden");
    return;
  }
  empty.classList.add("hidden");

  enrollments.forEach(e => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td class="px-3 py-2 border">${e.id}</td>
      <td class="px-3 py-2 border">${e.student_id}</td>
      <td class="px-3 py-2 border">${e.course_id}</td>
      <td class="px-3 py-2 border">${e.enrolled_on ?? ""}</td>
      <td class="px-3 py-2 border">
        <button class="text-red-600 underline" data-del="${e.id}">Delete</button>
      </td>
    `;
    body.appendChild(tr);
  });

  body.querySelectorAll("[data-del]").forEach(btn => {
    btn.addEventListener("click", () => deleteEnrollmentAction(Number(btn.dataset.del)));
  });
}