import json
from itertools import groupby

from django.http import FileResponse
from django.shortcuts import render

# Create your views here.
from hrm.models import Location, Employee
from production.models import ShotStatus, Clients, Projects, Task_Type, Locality, DayLogs, Shots, TeamLead_Week_Reports
import io
import xlsxwriter

from production.reports.multi_reports import reports_sheet_export
from production.reports.production_report import create_workbook
from production.reports.teamlead_report import teamlead_sheet_export
from production.serializers import DayLogsSerializer, ShotsSerializer, TeamReportSerializer


def production_reports(request):
    """
        Production Shots View
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


def teamlead_report(request):
    team_lead = Employee.objects.filter(role__name="TEAM LEAD").select_related('role','department','location','employement_status')

    context = {
        'team_lead': team_lead
    }
    return render(request, 'production/teamlead_report.html', context)

def export_teamlead_report(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    lead_id = request.GET['lead_id']
    buffer = io.BytesIO()
    teamlead_sheet_export(buffer, start_date, end_date, lead_id)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='TL_Weekly_Report.xlsx')

def reports(request):

    clients = Clients.objects.all()
    context = {
        'clients':clients
    }
    return render(request, 'production/reports.html', context)

def reports_export(request):
    client_id = request.GET['client_id']
    project_id = request.GET['project_id']
    task_type = None
    if 'task_type' in request.GET:
        task_type = request.GET['task_type']
    buffer = io.BytesIO()
    reports_sheet_export(buffer, client_id, project_id, task_type=task_type)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='Client_Report.xlsx')