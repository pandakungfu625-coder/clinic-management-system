// frontend/assets/js/controllers/profilesController.js

import { $ } from "../utils/dom.js";
import { filterList, sortList } from "../utils/listTools.js";
import { exportToCSV, exportToPDF } from "../utils/exportTools.js";

import { fetchAllProfiles } from "../services/profilesService.js";
import { renderProfilesTable } from "../components/ProfilesTable.js";
import { buildPrintableTableHTML } from "../utils/printTable.js";

const COLUMNS = [
  { key: "id", label: "ID" },
  { key: "name", label: "Name" },
  { key: "email", label: "Email" },
  { key: "year", label: "Year" },
];

let allStudents = [];

export function initProfilesController() {
  loadProfiles();

  $("searchInput")?.addEventListener("input", refresh);
  $("sortBy")?.addEventListener("change", refresh);
  $("sortDir")?.addEventListener("change", refresh);

  $("exportCsvBtn")?.addEventListener("click", () => {
    exportToCSV("students.csv", getRows(), COLUMNS);
  });

  $("exportPdfBtn")?.addEventListener("click", () => {
    const rows = getRows();
    const html = buildPrintableTableHTML("Student Directory", rows, COLUMNS);
    exportToPDF("Student Directory", html);
  });
}

async function loadProfiles() {
  const spinner = $("loadingSpinner");
  const container = $("profilesTableContainer");

  if (spinner) spinner.style.display = "block";
  if (container) container.style.display = "none";

  allStudents = await fetchAllProfiles();

  refresh();

  if (spinner) spinner.style.display = "none";
  if (container) container.style.display = "block";
}

function getRows() {
  const q = $("searchInput")?.value?.trim() ?? "";
  const sortKey = $("sortBy")?.value ?? "id";
  const sortDir = $("sortDir")?.value ?? "asc";

  const filtered = filterList(allStudents, q, ["id", "name", "email", "year"]);
  return sortList(filtered, sortKey, sortDir);
}

function refresh() {
  renderProfilesTable(getRows());
}
