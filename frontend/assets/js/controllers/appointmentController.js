import { apiGetAll, apiGetOne, apiCreate, apiUpdate, apiDelete } from "../services/appointmentService.js";
import { apiGetAll as apiGetAllPatients } from "../services/patientService.js";
import { apiGetAll as apiGetAllDoctors } from "../services/doctorService.js";
import { showAlert } from "../components/Alert.js";
import { renderAppointmentTable } from "../components/AppointmentTable.js";
import { resetForm, fillForm, populateSelects } from "../components/AppointmentForm.js";
import { setState, getState } from "../state/store.js";
import { $, createElement } from "../utils/dom.js";

export async function initAppointmentController() {
  await populateSelects();
  loadAppointments();

  $("appointmentForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
      patient_id: Number($("patient_id").value),
      doctor_id: Number($("doctor_id").value),
      scheduled_at: $("scheduled_at").value,
      reason: $("reason").value.trim(),
    };

    const { editingId } = getState();
    editingId ? await updateAppointment(editingId, data) : await createNewAppointment(data);
  });

  $("cancelBtn").addEventListener("click", () => {
    setState({ editingId: null });
    resetForm();
  });
}

export async function loadAppointments() {
  const spinner = $("loadingSpinner");
  const table = $("appointmentsTableContainer");
  spinner.style.display = "block";
  table.style.display = "none";

  const appts = await apiGetAll();
  setState({ appointments: appts });
  renderAppointmentTable(appts);

  spinner.style.display = "none";
  table.style.display = "block";
}

export async function createNewAppointment(data) {
  const res = await apiCreate(data);
  if (res.ok) {
    showAlert("Appointment scheduled!");
    resetForm();
    loadAppointments();
  }
}

export async function editAppointment(id) {
  const appt = await apiGetOne(id);
  setState({ editingId: id });
  fillForm(appt);
  window.scrollTo({ top: 0, behavior: "smooth" });
}

export async function updateAppointment(id, data) {
  const res = await apiUpdate(id, data);
  if (res.ok) {
    showAlert("Updated!");
    resetForm();
    setState({ editingId: null });
    loadAppointments();
  }
}

export async function deleteAppointmentAction(id) {
  const res = await apiDelete(id);
  if (res.ok) {
    showAlert("Deleted!");
    loadAppointments();
  }
}
