import { apiGetAll, apiGetOne, apiCreate, apiUpdate, apiDelete } from "../services/billingService.js";
import { apiGetAll as apiGetAllPatients } from "../services/patientService.js";
import { showAlert } from "../components/Alert.js";
import { renderBillingTable } from "../components/BillingTable.js";
import { resetForm, fillForm, populateSelects } from "../components/BillingForm.js";
import { setState, getState } from "../state/store.js";
import { $, createElement } from "../utils/dom.js";

export async function initBillingController() {
  await populateSelects();
  loadInvoices();

  $("billingForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
      patient_id: Number($("patient_id").value),
      amount: Number($("amount").value),
      issued_on: $("issued_on").value || null,
      paid_on: $("paid_on").value || null,
      description: $("description").value.trim(),
      status: $("paid_on").value ? "paid" : "unpaid",
    };

    const { editingId } = getState();
    editingId ? await updateInvoice(editingId, data) : await createNewInvoice(data);
  });

  $("cancelBtn").addEventListener("click", () => {
    setState({ editingId: null });
    resetForm();
  });
}

export async function loadInvoices() {
  const spinner = $("loadingSpinner");
  const table = $("billingTableContainer");
  spinner.style.display = "block";
  table.style.display = "none";

  const invoices = await apiGetAll();
  setState({ invoices });
  renderBillingTable(invoices);

  spinner.style.display = "none";
  table.style.display = "block";
}

export async function createNewInvoice(data) {
  const res = await apiCreate(data);
  if (res.ok) {
    showAlert("Invoice created!");
    resetForm();
    loadInvoices();
  }
}

export async function editInvoice(id) {
  const invoice = await apiGetOne(id);
  setState({ editingId: id });
  fillForm(invoice);
  window.scrollTo({ top: 0, behavior: "smooth" });
}

export async function updateInvoice(id, data) {
  const res = await apiUpdate(id, data);
  if (res.ok) {
    showAlert("Updated!");
    resetForm();
    setState({ editingId: null });
    loadInvoices();
  }
}

export async function deleteInvoiceAction(id) {
  if (!confirm("Delete this invoice?")) return;

  const res = await apiDelete(id);
  if (res.ok) {
    showAlert("Deleted!");
    loadInvoices();
  }
}
