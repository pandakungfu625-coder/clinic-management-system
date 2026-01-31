import { $ } from "../utils/dom.js";
import { setState } from "../state/store.js";

export function resetCourseForm() {
  $("courseForm").reset();
  $("cancelBtn").classList.add("hidden");
  $("submitBtn").textContent = "Add Course";
}

export function fillCourseForm(course) {
  $("title").value = course.title ?? "";
  $("code").value = course.code ?? "";
  $("teacher_name").value = course.teacher_name ?? "";
  $("fees").value = course.fees ?? "";
  $("duration_weeks").value = course.duration_weeks ?? "";

  $("cancelBtn").classList.remove("hidden");
  $("submitBtn").textContent = "Update Course";
  setState({ editingCourseId: course.id });
}