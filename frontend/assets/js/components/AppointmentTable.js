import { $ } from "../utils/dom.js";
import { editAppointment, deleteAppointmentAction } from "../controllers/appointmentController.js";

export function renderAppointmentTable(appts) {
  const body = $("appointmentsTableBody");
  const noAppts = $("noAppointments");

  body.innerHTML = "";

  if (!appts || appts.length === 0) {
    noAppts.style.display = "block";
    return;
  }

  noAppts.style.display = "none";

  appts.forEach((a) => {
    const row = document.createElement("tr");
    row.className = "border-b";

    row.innerHTML = `
      <td class="px-3 py-2">${a.id}</td>
      <td class="px-3 py-2 font-medium text-gray-900">${a.patient_name || a.patient_id}</td>
      <td class="px-3 py-2">${a.doctor_name || a.doctor_id}</td>
      <td class="px-3 py-2">${a.scheduled_at || ""}</td>
      <td class="px-3 py-2">${a.status || ""}</td>
      <td class="px-3 py-2 flex space-x-2">
        <button class="bg-yellow-400 hover:bg-yellow-500 text-black py-1 px-3 rounded" data-edit="${a.id}">Edit</button>
        <button class="btn-danger text-white py-1 px-3 rounded" data-delete="${a.id}">Delete</button>
      </td>
    `;

    row.querySelector("[data-edit]").onclick = () => editAppointment(a.id);
    row.querySelector("[data-delete]").onclick = () => deleteAppointmentAction(a.id);

    body.appendChild(row);
  });
}
