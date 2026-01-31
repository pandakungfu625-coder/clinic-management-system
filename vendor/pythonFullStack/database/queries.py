# database/queries.py
# Actual SQL queries — Create, Read, Update, Delete (CRUD)

from datetime import datetime
from .connection import get_connection


# -----------------------------
# STUDENTS CRUD
# -----------------------------

def students_get_all():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def students_get_one(student_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def students_create(data: dict):
    conn = get_connection()
    now = datetime.now().isoformat()
    cur = conn.execute(
        "INSERT INTO students (name, email, year, created_at) VALUES (?, ?, ?, ?)",
        (data["name"], data["email"], data["year"], now)
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return students_get_one(new_id)

def students_update(student_id: int, data: dict):
    conn = get_connection()
    now = datetime.now().isoformat()
    conn.execute("""
        UPDATE students
        SET name=?, email=?, year=?, updated_at=?
        WHERE id=?
    """, (data["name"], data["email"], data["year"], now, student_id))
    conn.commit()
    conn.close()
    return students_get_one(student_id)

def students_delete(student_id: int):
    student = students_get_one(student_id)
    if not student:
        return None

    conn = get_connection()
    conn.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    conn.close()
    return student


# -----------------------------
# COURSES CRUD
# -----------------------------

# -----------------------------
# COURSES CRUD (UPDATED)
# -----------------------------

def courses_get_all():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM courses ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def courses_get_one(course_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM courses WHERE id = ?", (course_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def courses_create(data: dict):
    conn = get_connection()
    now = datetime.now().isoformat()

    cur = conn.execute(
        """
        INSERT INTO courses (title, code, teacher_name, fees, duration_weeks, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            data["title"],
            data.get("code"),
            data.get("teacher_name"),
            data.get("fees"),
            data.get("duration_weeks"),
            now,
        ),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return courses_get_one(new_id)

def courses_update(course_id: int, data: dict):
    conn = get_connection()
    now = datetime.now().isoformat()

    conn.execute(
        """
        UPDATE courses
        SET title=?, code=?, teacher_name=?, fees=?, duration_weeks=?, updated_at=?
        WHERE id=?
        """,
        (
            data["title"],
            data.get("code"),
            data.get("teacher_name"),
            data.get("fees"),
            data.get("duration_weeks"),
            now,
            course_id,
        ),
    )
    conn.commit()
    conn.close()
    return courses_get_one(course_id)

def courses_delete(course_id: int):
    course = courses_get_one(course_id)
    if not course:
        return None

    conn = get_connection()
    conn.execute("DELETE FROM courses WHERE id=?", (course_id,))
    conn.commit()
    conn.close()
    return course


# -----------------------------
# ENROLLMENTS CRUD
# -----------------------------

def enrollments_get_all():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM enrollments ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def enrollments_get_one(enrollment_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM enrollments WHERE id = ?", (enrollment_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def enrollments_create(data: dict):
    """
    Expected data:
      - student_id (int)
      - course_id (int)
      - enrolled_on (optional)
    """
    conn = get_connection()
    now = datetime.now().isoformat()
    enrolled_on = data.get("enrolled_on") or now

    cur = conn.execute(
        "INSERT INTO enrollments (student_id, course_id, enrolled_on, created_at) VALUES (?, ?, ?, ?)",
        (data["student_id"], data["course_id"], enrolled_on, now)
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return enrollments_get_one(new_id)

def enrollments_delete(enrollment_id: int):
    enrollment = enrollments_get_one(enrollment_id)
    if not enrollment:
        return None

    conn = get_connection()
    conn.execute("DELETE FROM enrollments WHERE id=?", (enrollment_id,))
    conn.commit()
    conn.close()
    return enrollment


# -----------------------------
# JOIN REPORT
# -----------------------------

def enrollment_report():
    """
    Returns joined rows: enrollment + student + course (full course details)
    """
    conn = get_connection()
    rows = conn.execute("""
        SELECT
            e.id AS enrollment_id,
            e.enrolled_on,

            s.id AS student_id,
            s.name AS student_name,
            s.email AS student_email,
            s.year AS student_year,

            c.id AS course_id,
            c.title AS course_title,
            c.code AS course_code,
            c.teacher_name AS teacher_name,
            c.fees AS fees,
            c.duration_weeks AS duration_weeks
        FROM enrollments e
        JOIN students s ON s.id = e.student_id
        JOIN courses c ON c.id = e.course_id
        ORDER BY e.id DESC;
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# -----------------------------
# PATIENTS CRUD
# -----------------------------

def patients_get_all():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM patients ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def patients_get_one(patient_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM patients WHERE id = ?", (patient_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def patients_create(data: dict):
    conn = get_connection()
    now = datetime.now().isoformat()

    cur = conn.execute(
        """
        INSERT INTO patients (first_name, last_name, dob, phone, email, address, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("first_name"),
            data.get("last_name"),
            data.get("dob"),
            data.get("phone"),
            data.get("email"),
            data.get("address"),
            now,
        ),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return patients_get_one(new_id)


def patients_update(patient_id: int, data: dict):
    conn = get_connection()
    now = datetime.now().isoformat()
    conn.execute(
        """
        UPDATE patients
        SET first_name=?, last_name=?, dob=?, phone=?, email=?, address=?, updated_at=?
        WHERE id=?
        """,
        (
            data.get("first_name"),
            data.get("last_name"),
            data.get("dob"),
            data.get("phone"),
            data.get("email"),
            data.get("address"),
            now,
            patient_id,
        ),
    )
    conn.commit()
    conn.close()
    return patients_get_one(patient_id)


def patients_delete(patient_id: int):
    patient = patients_get_one(patient_id)
    if not patient:
        return None

    conn = get_connection()
    conn.execute("DELETE FROM patients WHERE id=?", (patient_id,))
    conn.commit()
    conn.close()
    return patient


# -----------------------------
# DOCTORS CRUD
# -----------------------------

def doctors_get_all():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM doctors ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def doctors_get_one(doctor_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def doctors_create(data: dict):
    conn = get_connection()
    now = datetime.now().isoformat()
    cur = conn.execute(
        "INSERT INTO doctors (name, specialty, phone, email, created_at) VALUES (?, ?, ?, ?, ?)",
        (data.get("name"), data.get("specialty"), data.get("phone"), data.get("email"), now),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return doctors_get_one(new_id)


def doctors_update(doctor_id: int, data: dict):
    conn = get_connection()
    now = datetime.now().isoformat()
    conn.execute(
        """
        UPDATE doctors
        SET name=?, specialty=?, phone=?, email=?, updated_at=?
        WHERE id=?
        """,
        (data.get("name"), data.get("specialty"), data.get("phone"), data.get("email"), now, doctor_id),
    )
    conn.commit()
    conn.close()
    return doctors_get_one(doctor_id)


def doctors_delete(doctor_id: int):
    doctor = doctors_get_one(doctor_id)
    if not doctor:
        return None

    conn = get_connection()
    conn.execute("DELETE FROM doctors WHERE id=?", (doctor_id,))
    conn.commit()
    conn.close()
    return doctor


# -----------------------------
# APPOINTMENTS CRUD
# -----------------------------

def appointments_get_all():
    conn = get_connection()
    rows = conn.execute("""
        SELECT
            a.*,
            p.first_name || ' ' || p.last_name AS patient_name,
            d.name AS doctor_name
        FROM appointments a
        LEFT JOIN patients p ON p.id = a.patient_id
        LEFT JOIN doctors d ON d.id = a.doctor_id
        ORDER BY a.id DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def appointments_get_one(appointment_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM appointments WHERE id = ?", (appointment_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def appointments_create(data: dict):
    conn = get_connection()
    now = datetime.now().isoformat()
    cur = conn.execute(
        "INSERT INTO appointments (patient_id, doctor_id, scheduled_at, reason, status, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (data["patient_id"], data["doctor_id"], data["scheduled_at"], data.get("reason"), data.get("status", "scheduled"), now),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return appointments_get_one(new_id)


def appointments_update(appointment_id: int, data: dict):
    conn = get_connection()
    now = datetime.now().isoformat()
    conn.execute(
        """
        UPDATE appointments
        SET patient_id=?, doctor_id=?, scheduled_at=?, reason=?, status=?, updated_at=?
        WHERE id=?
        """,
        (
            data.get("patient_id"),
            data.get("doctor_id"),
            data.get("scheduled_at"),
            data.get("reason"),
            data.get("status"),
            now,
            appointment_id,
        ),
    )
    conn.commit()
    conn.close()
    return appointments_get_one(appointment_id)


def appointments_delete(appointment_id: int):
    appt = appointments_get_one(appointment_id)
    if not appt:
        return None

    conn = get_connection()
    conn.execute("DELETE FROM appointments WHERE id=?", (appointment_id,))
    conn.commit()
    conn.close()
    return appt


# -----------------------------
# APPOINTMENT REPORT (JOIN)
# -----------------------------

def appointment_report():
    conn = get_connection()
    rows = conn.execute("""
        SELECT
            a.id AS appointment_id,
            a.scheduled_at,
            a.reason,
            a.status,

            p.id AS patient_id,
            p.first_name || ' ' || p.last_name AS patient_name,
            p.phone AS patient_phone,
            p.email AS patient_email,

            d.id AS doctor_id,
            d.name AS doctor_name,
            d.specialty AS doctor_specialty
        FROM appointments a
        JOIN patients p ON p.id = a.patient_id
        JOIN doctors d ON d.id = a.doctor_id
        ORDER BY a.id DESC;
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# -----------------------------
# INVOICES / BILLING CRUD
# -----------------------------

def invoices_get_all():
    conn = get_connection()
    rows = conn.execute("SELECT i.*, p.first_name || ' ' || p.last_name AS patient_name FROM invoices i LEFT JOIN patients p ON p.id = i.patient_id ORDER BY i.id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def invoices_get_one(invoice_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM invoices WHERE id = ?", (invoice_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def invoices_create(data: dict):
    conn = get_connection()
    now = datetime.now().isoformat()
    cur = conn.execute(
        "INSERT INTO invoices (patient_id, amount, issued_on, paid_on, status, description, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            data["patient_id"],
            data["amount"],
            data.get("issued_on"),
            data.get("paid_on"),
            data.get("status", "unpaid"),
            data.get("description"),
            now,
        ),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return invoices_get_one(new_id)


def invoices_update(invoice_id: int, data: dict):
    conn = get_connection()
    now = datetime.now().isoformat()
    conn.execute(
        """
        UPDATE invoices
        SET patient_id=?, amount=?, issued_on=?, paid_on=?, status=?, description=?, updated_at=?
        WHERE id=?
        """,
        (
            data.get("patient_id"),
            data.get("amount"),
            data.get("issued_on"),
            data.get("paid_on"),
            data.get("status"),
            data.get("description"),
            now,
            invoice_id,
        ),
    )
    conn.commit()
    conn.close()
    return invoices_get_one(invoice_id)


def invoices_delete(invoice_id: int):
    inv = invoices_get_one(invoice_id)
    if not inv:
        return None

    conn = get_connection()
    conn.execute("DELETE FROM invoices WHERE id=?", (invoice_id,))
    conn.commit()
    conn.close()
    return inv


def invoice_report():
    conn = get_connection()
    rows = conn.execute("""
        SELECT
            i.id AS invoice_id,
            i.amount,
            i.issued_on,
            i.paid_on,
            i.status,
            i.description,

            p.id AS patient_id,
            p.first_name || ' ' || p.last_name AS patient_name,
            p.phone AS patient_phone,
            p.email AS patient_email
        FROM invoices i
        JOIN patients p ON p.id = i.patient_id
        ORDER BY i.id DESC;
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]
