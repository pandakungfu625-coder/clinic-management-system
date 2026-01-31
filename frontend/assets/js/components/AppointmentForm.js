import { $ } from "../utils/dom.js";
import { apiGetAll as apiGetAllPatients } from "../services/patientService.js";
import { apiGetAll as apiGetAllDoctors } from "../services/doctorService.js";

export async function populateSelects() {
  const patients = await apiGetAllPatients();
  const doctors = await apiGetAllDoctors();

  const pSelect = $("patient_id");
  const dSelect = $("doctor_id");

  pSelect.innerHTML = "<option value=''>Select patient</option>";
  dSelect.innerHTML = "<option value=''>Select doctor</option>";

  (patients || []).forEach((p) => {
    const opt = document.createElement("option");
    opt.value = p.id;
    opt.textContent = `${p.first_name} ${p.last_name}`;
    pSelect.appendChild(opt);
  });

  (doctors || []).forEach((d) => {
    const opt = document.createElement("option");
    opt.value = d.id;
    opt.textContent = d.name;
    dSelect.appendChild(opt);
  });
}

export function resetForm() {
  $("appointmentForm").reset();
  $("submitBtn").textContent = "Schedule";
  $("cancelBtn").style.display = "none";
}

export function fillForm(appt) {
  $("patient_id").value = appt.patient_id;
  $("doctor_id").value = appt.doctor_id;
  $("scheduled_at").value = appt.scheduled_at || "";
  $("reason").value = appt.reason || "";

  $("submitBtn").textContent = "Update";
  $("cancelBtn").style.display = "inline-block";
}
