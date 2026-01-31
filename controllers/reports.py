from core.responses import send_json
from services.report_service import service_get_enrollment_report

def get_enrollment_report(handler):
    data = service_get_enrollment_report()
    return send_json(handler, 200, data)