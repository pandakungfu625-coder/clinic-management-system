import { $ } from "../utils/dom.js";
import { editStudent, deleteStudentAction } from "../controllers/studentController.js";

// Renders the list of students into an HTML table
export function renderStudentTable(students) {
  const body = $("studentsTableBody");
  const noStudents = $("noStudents");

  body.innerHTML = "";

  if (students.length === 0) {
    noStudents.style.display = "block";
    return;
  }

  noStudents.style.display = "none";

  students.forEach((student) => {
    const row = document.createElement("tr");
    row.className = "border-b";

    row.innerHTML = `
      <td class="px-3 py-2">${student.id}</td>

      <!-- Name is now plain text (no profile navigation here) -->
      <td class="px-3 py-2 font-medium text-gray-900">
        ${student.name}
      </td>

      <td class="px-3 py-2">${student.email}</td>
      <td class="px-3 py-2">${student.year}</td>

      <td class="px-3 py-2 flex space-x-2">
        <button
          class="bg-yellow-400 hover:bg-yellow-500 text-black py-1 px-3 rounded"
          data-edit="${student.id}"
        >
          Edit
        </button>

        <button
          class="bg-red-500 hover:bg-red-600 text-white py-1 px-3 rounded"
          data-delete="${student.id}"
        >
          Delete
        </button>
      </td>
    `;

    row.querySelector("[data-edit]").onclick = () => editStudent(student.id);
    row.querySelector("[data-delete]").onclick = () => deleteStudentAction(student.id);

    body.appendChild(row);
  });
}