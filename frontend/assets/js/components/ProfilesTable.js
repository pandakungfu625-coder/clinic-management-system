// frontend/assets/js/components/ProfilesTable.js
import { $ } from "../utils/dom.js";

export function renderProfilesTable(students) {
  const body = $("profilesTableBody");
  const noProfiles = $("noProfiles");

  if (!body) return;

  body.innerHTML = "";

  if (!students || students.length === 0) {
    if (noProfiles) noProfiles.style.display = "block";
    return;
  }

  if (noProfiles) noProfiles.style.display = "none";

  students.forEach((s) => {
    const tr = document.createElement("tr");
    tr.className = "border-b";

    tr.innerHTML = `
      <td class="px-3 py-2">${s.id}</td>

      <td class="px-3 py-2">
        <a href="/profiles/${s.id}" data-link class="text-blue-600 hover:underline font-medium">
          ${s.name}
        </a>
      </td>

      <td class="px-3 py-2">${s.email}</td>
      <td class="px-3 py-2">${s.year}</td>

      <td class="px-3 py-2">
        <a href="/profiles/${s.id}" data-link
          class="inline-flex items-center justify-center px-3 py-1 rounded bg-blue-600 text-white hover:bg-blue-700">
          View
        </a>
      </td>
    `;

    body.appendChild(tr);
  });
}
