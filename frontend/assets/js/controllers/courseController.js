import {
  apiGetAllCourses,
  apiGetCourse,
  apiCreateCourse,
  apiUpdateCourse,
  apiDeleteCourse,
} from "../services/courseService.js";

import { showAlert } from "../components/Alert.js";
import { renderCourseTable } from "../components/CourseTable.js";
import { resetCourseForm, fillCourseForm } from "../components/CourseForm.js";

import { setState, getState } from "../state/store.js";
import { $ } from "../utils/dom.js";

export function initCourseController() {
  loadCourses();

  $("courseForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
      title: $("title").value.trim(),
      code: $("code").value.trim(),
      teacher_name: $("teacher_name").value.trim(),
      fees: Number($("fees").value),
      duration_weeks: Number($("duration_weeks").value),
    };

    const { editingCourseId } = getState();
    editingCourseId
      ? await updateCourse(editingCourseId, data)
      : await createCourse(data);
  });

  $("cancelBtn").addEventListener("click", () => {
    setState({ editingCourseId: null });
    resetCourseForm();
  });
}

export async function loadCourses() {
  const spinner = $("loadingSpinner");
  const table = $("coursesTableContainer");

  // show spinner, hide table
  spinner.classList.remove("hidden");
  table.classList.add("hidden");

  const courses = await apiGetAllCourses();
  setState({ courses });
  renderCourseTable(courses);

  // hide spinner, show table
  spinner.classList.add("hidden");
  table.classList.remove("hidden");
}

export async function createCourse(data) {
  const res = await apiCreateCourse(data);
  if (res.ok) {
    showAlert("Course added!");
    resetCourseForm();
    loadCourses();
  } else {
    showAlert("Failed to add course", "error");
  }
}

export async function editCourse(id) {
  const course = await apiGetCourse(id);
  if (!course) return;

  fillCourseForm(course);
  window.scrollTo({ top: 0, behavior: "smooth" });
}

export async function updateCourse(id, data) {
  const res = await apiUpdateCourse(id, data);
  if (res.ok) {
    showAlert("Course updated!");
    resetCourseForm();
    setState({ editingCourseId: null });
    loadCourses();
  } else {
    showAlert("Failed to update course", "error");
  }
}

export async function deleteCourseAction(id) {

  const res = await apiDeleteCourse(id);
  if (res.ok) {
    showAlert("Course deleted!");
    loadCourses();
  } else {
    showAlert("Failed to delete course", "error");
  }
}