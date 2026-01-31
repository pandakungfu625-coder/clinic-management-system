// frontend/assets/js/components/CourseTable.js

import { $ } from "../utils/dom.js";
import { editCourse, deleteCourseAction } from "../controllers/courseController.js";

export function renderCourseTable(courses) {
  const body = $("coursesTableBody");
  const noCourses = $("noCourses");

  if (!body) return;

  body.innerHTML = "";

  if (!courses || courses.length === 0) {
    if (noCourses) noCourses.classList.remove("hidden");
    return;
  }

  if (noCourses) noCourses.classList.add("hidden");

  courses.forEach((c) => {
    const tr = document.createElement("tr");
    tr.className = "border-b";

    tr.innerHTML = `
      <td class="px-3 py-2">${c.id ?? "-"}</td>
      <td class="px-3 py-2">${c.title ?? "-"}</td>
      <td class="px-3 py-2">${c.code ?? "-"}</td>
      <td class="px-3 py-2">${c.teacher_name ?? "-"}</td>
      <td class="px-3 py-2">${c.fees ?? "-"}</td>
      <td class="px-3 py-2">${c.duration_weeks ?? "-"}</td>
      <td class="px-3 py-2">
        <div class="flex gap-2">
          <button
            type="button"
            class="px-3 py-1 rounded border text-blue-600 hover:bg-blue-50"
            data-edit
          >
            Edit
          </button>
          <button
            type="button"
            class="px-3 py-1 rounded border text-red-600 hover:bg-red-50"
            data-delete
          >
            Delete
          </button>
        </div>
      </td>
    `;

    tr.querySelector("[data-edit]").addEventListener("click", () => editCourse(c.id));
    tr.querySelector("[data-delete]").addEventListener("click", () => deleteCourseAction(c.id));

    body.appendChild(tr);
  });
}