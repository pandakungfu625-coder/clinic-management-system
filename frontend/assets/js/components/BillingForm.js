import { $ } from "../utils/dom.js";
import { apiGetAll as apiGetAllPatients } from "../services/patientService.js";

export async function populateSelects() {
  const patients = await apiGetAllPatients();
  const pSelect = $("patient_id");
  pSelect.innerHTML = "<option value=''>Select patient</option>";
  (patients || []).forEach((p) => {
    const opt = document.createElement("option");
    opt.value = p.id;
    opt.textContent = `${p.first_name} ${p.last_name}`;
    pSelect.appendChild(opt);
  });
}

export function resetForm() {
  $("billingForm").reset();
  $("submitBtn").textContent = "Create Invoice";
  $("cancelBtn").style.display = "none";
}

export function fillForm(inv) {
  $("patient_id").value = inv.patient_id;
  $("amount").value = inv.amount;
  $("issued_on").value = inv.issued_on || "";
  $("paid_on").value = inv.paid_on || "";
  $("description").value = inv.description || "";

  $("submitBtn").textContent = "Update Invoice";
  $("cancelBtn").style.display = "inline-block";
}
