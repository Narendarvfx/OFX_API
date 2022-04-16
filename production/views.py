import io

from django.http import FileResponse
from django.shortcuts import render

# Create your views here.
from hrm.models import Location, Employee
from production.models import ShotStatus, Clients, Projects, Task_Type, Locality
from production.reports.dept_report import dept_sheet_download
from production.reports.multi_reports import reports_sheet_export
from production.reports.production_report import create_workbook, check_filters
from production.reports.studio_report import studio_sheet_download
from production.reports.teamlead_report import teamlead_sheet_download


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
    client_id = int(request.GET['client'])
    project_id = int(request.GET['project'])
    taskType_id = int(request.GET['task_type'])
    status_id = int(request.GET['statuss'])
    location_id = int(request.GET['location'])
    locality_id = int(request.GET['locality'])

    buffer = io.BytesIO()
    if not client_id or not project_id or not taskType_id or not status_id or not locality_id or not location_id:
        check_filters(buffer=buffer, client_id=int(client_id), project_id=int(project_id), status_idd=int(status_id), location_id=int(location_id), locality_id=int(locality_id), taskType_id=int(taskType_id))
    else:
        create_workbook(buffer)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='live_production_report.xlsx')


def teamlead_report(request):
    team_lead = Employee.objects.filter(role__name="TEAM LEAD").select_related('role','department','location','employement_status')
    context = {
        'team_lead': team_lead
    }
    return render(request, 'production/teamleads_report.html', context)

def studio_report(request):

    return render(request, 'production/studio_report.html')

def department_report(request):

    return render(request, 'production/department_report.html')

def artist_report(request):

    return render(request, 'production/artist_report.html')

def export_teamlead_report(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    lead_id = request.GET['lead_id']
    buffer = io.BytesIO()
    teamlead_sheet_download(buffer, start_date, end_date, lead_id)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='TeamLead_Report.xlsx')

def export_dept_report(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    dept = request.GET['dept']
    buffer = io.BytesIO()
    dept_sheet_download(buffer, start_date, end_date, dept)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='{}_Department_Report.xlsx'.format(dept))

def export_studio_report(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    buffer = io.BytesIO()
    studio_sheet_download(buffer, start_date, end_date)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='Studio_Report.xlsx')

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