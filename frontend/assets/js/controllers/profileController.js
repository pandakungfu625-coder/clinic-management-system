// frontend/assets/js/controllers/profileController.js

import { $ } from "../utils/dom.js";
import { exportToCSV, exportToPDF } from "../utils/exportTools.js";

import { fetchStudentById, fetchEnrollmentsForStudent } from "../services/profileService.js";
import {
  setProfileLoading,
  renderStudentBasic,
  renderEnrollmentCount,
  renderEnrollmentsTable,
  renderProfileError,
} from "../components/ProfileView.js";

import {
  PROFILE_CSV_COLUMNS,
  normalizeProfileRows,
  buildProfilePDFHtml,
} from "../utils/profileExport.js";

export async function initProfileController(studentId) {
  setProfileLoading(true);

  try {
    // Fetch data (service)
    const [student, rows] = await Promise.all([
      fetchStudentById(studentId),
      fetchEnrollmentsForStudent(studentId),
    ]);

    if (!student) throw new Error("Student not found");

    // Render UI (view)
    renderStudentBasic(student);
    renderEnrollmentCount(rows.length);
    renderEnrollmentsTable(rows);

    // Wire export buttons (controller)
    $("profileExportCsvBtn")?.addEventListener("click", () => {
      const safeRows = normalizeProfileRows(rows);
      const filename = `student_${student.id}_enrollments.csv`;
      exportToCSV(filename, safeRows, PROFILE_CSV_COLUMNS);
    });

    $("profileExportPdfBtn")?.addEventListener("click", () => {
      const html = buildProfilePDFHtml(student, rows);
      exportToPDF(`Student ${student.id} Profile`, html);
    });

    setProfileLoading(false);
  } catch (err) {
    console.error("[profileController] error:", err);
    renderProfileError();
  }
}

export default { initProfileController };
