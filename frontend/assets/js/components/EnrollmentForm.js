import { $ } from "../utils/dom.js";

export function fillEnrollmentDropdowns(students, courses) {
  const studentSel = $("student_id");
  const courseSel = $("course_id");

  studentSel.innerHTML = `<option value="">Select Student</option>`;
  courseSel.innerHTML = `<option value="">Select Course</option>`;

  (students || []).forEach(s => {
    const opt = document.createElement("option");
    opt.value = s.id;
    opt.textContent = `${s.name} (ID: ${s.id})`;
    studentSel.appendChild(opt);
  });

  (courses || []).forEach(c => {
    const opt = document.createElement("option");
    opt.value = c.id;
    opt.textContent = `${c.title} (ID: ${c.id})`;
    courseSel.appendChild(opt);
  });
}