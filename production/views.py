from django.http import FileResponse
from django.shortcuts import render

# Create your views here.
from hrm.models import Location
from production.models import ShotStatus, Clients, Projects, Task_Type, Locality
import io
import xlsxwriter

from production.reports.production_report import create_workbook


def production_reports(request):
    """
        Employee Directory View
        :param request:
        :return:
        """
    status = ShotStatus.objects.all()
    clients = Clients.objects.all()
    projects = Projects.objects.all()
    task_type = Task_Type.objects.all()
    location = Location.objects.all()
    locality = Locality.objects.all()
    context = {
        'status': status,
        'clients': clients,
        'projects': projects,
        'task_type': task_type,
        'location': location,
        'locality': locality
    }
    return render(request, 'production/production_report.html', context)


def export_prod_report(request):
    buffer = io.BytesIO()
    create_workbook(buffer)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='live_production_report.xlsx')
