from database.queries import (
    appointments_get_all,
    appointments_get_one,
    appointments_create,
    appointments_update,
    appointments_delete,
)


def service_get_all():
    return appointments_get_all()


def service_get_one(appointment_id):
    return appointments_get_one(appointment_id)


def service_create(data):
    return appointments_create(data)


def service_update(appointment_id, data):
    return appointments_update(appointment_id, data)


def service_delete(appointment_id):
    return appointments_delete(appointment_id)
