#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

import io
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import FileResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from OFX_API import apiRequestManager

from hrm.models import Location, Employee, Department, OrganizationWorkingDays, OrganizationHolidayTypes, WorkingDayTypes

# Create your views here.
from ofx_statistics.models import ClientStatistics
from hrm.serializers import EmployeeSerializer, DepartmentSerializer, OrganizationWorkingDaysSerializer, RoleRelationshipBindingSerializer, EmployeeRoleBindingSerializer, OrganizationHolidayTypesSerializer, WorkingDayTypesSerializer, RoleSerializer, LocationSerializer
from hrm.models import Location, Employee, Department, OrganizationWorkingDays, RoleRelationshipBinding, EmployeeRoleBinding, Role
from ofx_dashboards.models import MandayAvailability
from production.reports.shotday_logs_report import shotday_logs_sheet_download
from production.serializers import PipelineStepsSerializer, StatusSerializer, TaskTypeSerializer
from production.models import ShotStatus, Clients, Projects, Task_Type, Locality, Shots, RolePipelineSteps, MyTask, ClientVersions
from production.reports.custom_artist_id_report import artist_sheet_download, artist_individual_sheet_download
from production.reports.custom_teamlead_report import teamleads_sheet_download, teamlead_sheet_download_2
from production.reports.custom_leads_report import leads_sheet_download, lead_sheet_download_2
from production.reports.dept_report import dept_sheet_download
from production.reports.multi_reports import reports_sheet_export
from production.reports.production_report import create_workbook
from production.reports.studio_report import studio_sheet_download
from production.reports.teamlead_report import teamlead_sheet_download
from production.reports.version_report import check_ver_filters, create_ver_workbook
from production.reports.versions_report import writeVersionreportWorksheet
from production.reports.client_report import writeClientreportWorksheet
from production.reports.department_lite_report import writeDepartmentLiteReportWorksheet
from production.reports.studio_lite_report import writeStudioLiteReportWorksheet
from production.reports.shot_daylogs_report import shot_daylogs_download
from production.reports.task_daylogs_report import task_daylogs_download
from production.reports.attendence_report import attendance_sheet_download
from production.reports.tasks_report import tasks_download
from production.reports.taskday_logs_report import taskday_logs_sheet_download
from production.reports.leaves_reports import leaves_sheet_download
from production.reports.artists_list import allartistlist_sheet_download
from production.serializers import PipelineStepsSerializer, StatusSerializer

def lead_report(request):
    return render(request, 'production/myreport_teamlead.html')

def EstimationId(request):
    return  render(request, 'production/estimation.html')

def all_reports_page(request):
    return render(request, 'production/all_reports_page.html')

def mandays_availability(request):
    return render(request, 'production/mandays_availabilty.html')

def resource_availability(request):
    # return render(request, 'home/comming_soon.html')
    return render(request, 'home/resource_availabilty.html')
    
def scheduling(request):
    return render(request, 'production/scheduling.html')

def production_reports(request):
    """
    Production Shots View
    :param request:
    :return:
    """
    status = ShotStatus.objects.all()
    clients = Clients.objects.all()
    projects = Projects.objects.exclude(status="ARCHIVED").all()
    task_type = Task_Type.objects.all()
    location = Location.objects.all()
    locality = Locality.objects.all()
    leads = Employee.objects.filter(role__name="TEAM LEAD").all()

    context = {
        'status': status,
        'clients': clients,
        'projects': projects,
        'task_type': task_type,
        'location': location,
        'locality': locality,
        'leads': leads,
        'user': request.user
    }
    # return render(request, 'production/shots.html', context)
    return render(request, 'production/shots_modified.html', context)

def shotsAssignments(request):
    """
    Production Shots View
    :param request:
    :return:
    """
    status = ShotStatus.objects.all()
    clients = Clients.objects.all()
    projects = Projects.objects.exclude(status="ARCHIVED").all()
    task_type = Task_Type.objects.all()
    location = Location.objects.all()
    locality = Locality.objects.all()
    leads = Employee.objects.filter(role__name="TEAM LEAD").all()

    context = {
        'status': status,
        'clients': clients,
        'projects': projects,
        'task_type': task_type,
        'location': location,
        'locality': locality,
        'leads': leads,
        'user': request.user
    }
    return render(request, 'production/shotsAssignments.html', context)

def shots_view(request):
    """
    Production Shots View
    :param request:
    :return:
    """
    # status = ShotStatus.objects.all()
    # clients = Clients.objects.all()
    # projects = Projects.objects.exclude(status="ARCHIVED").all()
    # task_type = Task_Type.objects.all()
    # location = Location.objects.all()
    # locality = Locality.objects.all()
    # leads = Employee.objects.filter(role__name="TEAM LEAD").all()
    #
    # context = {
    #     'status': status,
    #     'clients': clients,
    #     'projects': projects,
    #     'task_type': task_type,
    #     'location': location,
    #     'locality': locality,
    #     'leads': leads,
    #     'user': request.user
    # }
    chkPass = True if request.user.employee.role.name!='VFX ARTIST' else False
    shot_id = request.GET.get('shot_id',None)
    if chkPass is False and shot_id is not None and len(list(MyTask.objects.filter(shot__id=shot_id,artist__id=request.user.employee.id).values('id'))) > 0:
        chkPass = True
    if chkPass is True and shot_id is not None:
        return render(request, 'production/shot_details.html', {})
    else:
        return render(request, 'error_pages/pages-error-403.html', status=403)

def export_prod_report(request):
    shot_ids = []
    if request.POST.get('shot_ids'):
        for shot_id in request.POST['shot_ids'].split('|'):
            shot_ids.append(shot_id)

    buffer = io.BytesIO()
    create_workbook(buffer, shot_ids,request)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='live_production_report.xlsx')
def export_prod_sheet(request):
    buffer = io.BytesIO()
    create_workbook(buffer,request)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='live_production_report.xlsx')

def export_ver_report(request):
    client_id = int(request.GET['client'])
    project_id = int(request.GET['project'])
    taskType_id = int(request.GET['task_type'])

    buffer = io.BytesIO()
    if not client_id or not project_id or not taskType_id:
        check_ver_filters(buffer=buffer, client_id=int(client_id), project_id=int(project_id),
                          taskType_id=int(taskType_id))
    else:
        create_ver_workbook(buffer)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='version_report.xlsx')


class export_versionreport(APIView, apiRequestManager):

    def post(self, request, format=None):
        collectArguments = {"id": True, "shot__isSubShot":True, "modified_date__range":"split", "version__in":"split", "shot__sequence__project__client__id":True,"shot__sequence__project__id":True,"shot__task_type__id":True}
        query = self.readRequest(
            model=ClientVersions,
            request=request,
            readData=collectArguments
            )
        if query['POST'].get('shot__isSubShot',None) is not None:
            query['POST']['shot__isSubShot'] = True if query['POST']['shot__isSubShot']=='true' else False
        vrshots = self.getDBData(model=ClientVersions,queryFilter=query['POST'],prefetch_related=query['prefetch_related'],select_related=query['select_related'],exclude=query['exclude'],queryPerams=[
                            'id',
                            'version',
                            'shot__id',
                            'shot__name',
                            'shot__sequence__id',
                            'shot__sequence__name',
                            'shot__sequence__project__id',
                            'shot__sequence__project__name',
                            'shot__task_type__id',
                            'shot__task_type__name',
                            'shot__artist__id',
                            'shot__artist__fullName',
                            'shot__artists__id',
                            'shot__artists__fullName',
                            'shot__supervisor__id',
                            'shot__supervisor__fullName',
                            'shot__team_lead__id',
                            'shot__team_lead__fullName',
                            'shot__hod__id',
                            'shot__hod__fullName',
                            'shot__location__id',
                            'shot__location__name',
                            'shot__version',
                            'shot__bid_days',
                            'shot__package_id',
                            'modified_date'
                            ])
        reVersions = {}
        for x in vrshots:
            if reVersions.get(x["version"],None) is None:
                reVersions[x["version"]] = {
                    "name": x["version"],
                    "shots": []
                    }
            reVersions[x["version"]]["shots"].append(x.copy())
        # return Response(reVersions)
        buffer = io.BytesIO()
        writeVersionreportWorksheet(buffer,query=query['POST'],data=reVersions,isOnly= False if request.data.get('onlyOne',False) is False or request.data.get('onlyOne',False)=='false' else True)
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='{client}_{v1}_report.xlsx'.format(client=list(Clients.objects.filter(id=query['POST']['shot__sequence__project__client__id']).values('name'))[0]['name'],v1=query['POST']['version__in'][0] if request.data.get('onlyOne',None) is not None else 'versions'))
        # collectArguments = {"id": True,"shot__sequence__project__client__id":True }
        return Response(vrshots)
    
class export_clientreport(APIView, apiRequestManager):

    def post(self, request, format=None):
        collectArguments = {"id": True, "client__id":True, "project__id":True, "dep__id":True }
        query = self.readRequest(
            model=ClientStatistics,
            request=request,
            readData=collectArguments
            )
        if query['POST'].get('client__id',None) is not None:
            clientStats = self.getDBData(model=ClientStatistics,queryFilter=query['POST'],prefetch_related=query['prefetch_related'],select_related=query['select_related'],exclude=query['exclude'],queryPerams=[
                "id",
                "client__id",
                "client__name",
                "project__id",
                "project__name",
                "dep__id",
                "dep__name",
                "tmd",
                "amd",
                "highest_ver",
                "highest_ver_shotCount",
                "retake_per",
                "artistcount",
                "artistTMD",
                "missedEta",
                "totalshots"])
            # return Response(clientStats)
            clientName = list(Clients.objects.filter(id=query['POST']['client__id']).values('name'))[0]['name']
            buffer = io.BytesIO()
            writeClientreportWorksheet(buffer,query=query['POST'],data=clientStats,clientName=clientName)
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename='client_{client}_report.xlsx'.format(client=clientName))
        
            return Response(clientStats)
        else:
            return Response({"msg":"Invalid Request"})
        # if query['POST'].get('shot__isSubShot',None) is not None:
        #     query['POST']['shot__isSubShot'] = True if query['POST']['shot__isSubShot']=='true' else False
        # vrshots = self.getDBData(model=ClientVersions,queryFilter=query['POST'],prefetch_related=query['prefetch_related'],select_related=query['select_related'],exclude=query['exclude'],queryPerams=[
        #                     'id',
        #                     'version',
        #                     'shot__id',
        #                     'shot__name',
        #                     'shot__sequence__id',
        #                     'shot__sequence__name',
        #                     'shot__sequence__project__id',
        #                     'shot__sequence__project__name',
        #                     'shot__task_type__id',
        #                     'shot__task_type__name',
        #                     'shot__artist__id',
        #                     'shot__artist__fullName',
        #                     'shot__artists__id',
        #                     'shot__artists__fullName',
        #                     'shot__supervisor__id',
        #                     'shot__supervisor__fullName',
        #                     'shot__team_lead__id',
        #                     'shot__team_lead__fullName',
        #                     'shot__hod__id',
        #                     'shot__hod__fullName',
        #                     'shot__location__id',
        #                     'shot__location__name',
        #                     'shot__version',
        #                     'shot__bid_days',
        #                     'shot__package_id',
        #                     'modified_date'
        #                     ])
        # reVersions = {}
        # for x in vrshots:
        #     if reVersions.get(x["version"],None) is None:
        #         reVersions[x["version"]] = {
        #             "name": x["version"],
        #             "shots": []
        #             }
        #     reVersions[x["version"]]["shots"].append(x.copy())
        # # return Response(reVersions)
        # buffer = io.BytesIO()
        # writeVersionreportWorksheet(buffer,query=query['POST'],data=reVersions,isOnly= False if request.data.get('onlyOne',False) is False or request.data.get('onlyOne',False)=='false' else True)
        # buffer.seek(0)
        # return FileResponse(buffer, as_attachment=True, filename='{client}_{v1}_report.xlsx'.format(client=list(Clients.objects.filter(id=query['POST']['shot__sequence__project__client__id']).values('name'))[0]['name'],v1=query['POST']['version__in'][0] if request.data.get('onlyOne',None) is not None else 'versions'))
        # # collectArguments = {"id": True,"shot__sequence__project__client__id":True }
        return Response(query)
    
class export_department_lite_report(APIView, apiRequestManager):

    def post(self, request, format=None):
        _pdx = request.data.copy()
        postData = {}
        dataFeilds = ['achievedMandays','monthlyAchievement','artistsReport','mandaysAvailability']
        fileNameMap = {
            'default':'department',
            'achievedMandays':'achieved_mandays',
            'monthlyAchievement':'monthly_achievement',
            'artistsReport':'artists_report',
            'mandaysAvailability':'mandays_availability'
            }
        for k,x in _pdx.items():
            if k in dataFeilds:
                postData[k] = json.loads(x)
            elif k!='csrfmiddlewaretoken':
                postData[k] = x
        buffer = io.BytesIO()
        writeDepartmentLiteReportWorksheet(buffer,data={k:postData[k] for k in dataFeilds if postData.get(k,None) is not None})
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='{name}_report.xlsx'.format(name=fileNameMap[postData.get("exportOnly",'default')]))
    
class export_studio_lite_report(APIView, apiRequestManager):

    def post(self, request, format=None):
        _pdx = request.data.copy()
        postData = {}
        dataFeilds = ['achievedMandays','monthlyAchievement','artistsReport','mandaysAvailability']
        fileNameMap = {
            'default':'department',
            'achievedMandays':'achieved_mandays',
            'monthlyAchievement':'monthly_achievement',
            'artistsReport':'artists_report',
            'mandaysAvailability':'mandays_availability'
            }
        for k,x in _pdx.items():
            if k in dataFeilds:
                postData[k] = json.loads(x)
            elif k!='csrfmiddlewaretoken':
                postData[k] = x
        # return Response(postData)
        buffer = io.BytesIO()
        writeStudioLiteReportWorksheet(buffer,data={k:postData[k] for k in dataFeilds if postData.get(k,None) is not None})
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='studio_{name}_report.xlsx'.format(name=fileNameMap[postData.get("exportOnly",'default')]))

# def export_versionreport(request):
#     collectArguments = {"id": True, "shot__isSubShot":True, "modified_date__range":"split", "version__in":"split", "shot__sequence__project__client__id":True,"shot__sequence__project__id":True,"shot__task_type__id":True}
#     vrshots = _reqManger.read(
#                 request = request,
#                 model = ClientVersions,
#                 collectArguments = collectArguments,
#                 isGet=False
#                 )
#     print(vrshots)
    # client_id = int(request.GET['client'])
    # project_id = int(request.GET['project'])
    # taskType_id = int(request.GET['task_type'])

    # buffer = io.BytesIO()
    # if not client_id or not project_id or not taskType_id:
    #     check_ver_filters(buffer=buffer, client_id=int(client_id), project_id=int(project_id),
    #                       taskType_id=int(taskType_id))
    # else:
    #     create_ver_workbook(buffer)
    # buffer.seek(0)
    # return FileResponse(buffer, as_attachment=True, filename='version_report.xlsx')

def time_card(request):
    context = {
        'user': request.user
    }
    return render(request, 'production/time_card.html', context)

def artists_statistics(request):
    context = {
        'user': request.user
    }
    return render(request, 'production/artists_statistics.html', context)

def attendance(request):
    context = {
        'user': request.user
    }
    return render(request, 'production/attendance.html', context)

def leaves(request):
    context = {
        'user': request.user
    }
    return render(request, 'production/leaves.html', context)

def calendar(request):
    context = {
        'user': request.user
    }
    return render(request, 'production/calendar.html', context)

def teamlead_report(request):
    team_lead = Employee.objects.filter(role__name="TEAM LEAD").select_related('role', 'department', 'location',
                                                                               'employement_status')
    context = {
        'team_lead': team_lead
    }
    return render(request, 'production/teamleads_report.html', context)

def leads_report(request):
    return render(request, 'production/leads_report.html')

def studio_report(request):
    return render(request, 'production/studio_report.html')

def department_report(request):
    return render(request, 'production/department_report.html')

def artist_report(request):
    return render(request, 'production/artist_report.html')
    # return render(request, 'production/artist_report_2.html')

def taskday_logs_export(request):
    from_date = request.POST.get('from_date')
    to_date = request.POST.get('to_date')
    log_ids = []
    if request.POST.get("logids", None) is not None:
        for rid in request.POST["logids"].split('|'):
            log_ids.append(rid)
    # log_ids = [int(i) for i in log_ids]
    buffer = io.BytesIO()
    taskday_logs_sheet_download(buffer=buffer, from_date=from_date, to_date=to_date, logs_ids=log_ids)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='taskday_logs_Report.xlsx')

def leaves_export(request):
    from_date = request.POST.get('from_date')
    to_date = request.POST.get('to_date')
    leaves_ids = []
    if request.POST.get("leaves_ids", None) is not None:
        for rid in request.POST["leaves_ids"].split('|'):
            leaves_ids.append(rid)
    buffer = io.BytesIO()
    leaves_sheet_download(buffer=buffer, from_date=from_date, to_date=to_date, leaves_ids=leaves_ids)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='leaves_Report.xlsx')

def attendance_export(request):
    from_date = request.POST.get('from_date')
    to_date = request.POST.get('to_date')
    atd_ids = []
    if request.POST.get("atdids", None) is not None:
        for rid in request.POST["atdids"].split('|'):
            atd_ids.append(rid)
    # log_ids = [int(i) for i in log_ids]
    buffer = io.BytesIO()
    attendance_sheet_download(buffer=buffer, from_date=from_date, to_date=to_date, atd_ids=atd_ids)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='attendence_Report.xlsx')

def version_report(request):
    # status = ShotStatus.objects.all()
    # clients = Clients.objects.all()
    # projects = Projects.objects.exclude(status="ARCHIVED").all()
    # task_type = Task_Type.objects.all()
    # location = Location.objects.all()
    # locality = Locality.objects.all()
    # leads = Employee.objects.filter(role__name="TEAM LEAD").all()

    # context = {
    #     'status': status,
    #     'clients': clients,
    #     'projects': projects,
    #     'task_type': task_type,
    #     'location': location,
    #     'locality': locality,
    #     'leads': leads,
    #     'user': request.user
    # }

    # return render(request, 'production/version_report.html', context)
    return render(request, 'production/version_report.html')

def export_teamlead_report(request):
    if request.POST.get('from_date', None) is not None:
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        tl_ids = []
        tl_id = None
        if request.POST.get('employees', None) is not None:
            for rid in request.POST['employees'].split('|'):
                tl_ids.append(rid)
        else:
            tl_id = request.POST.get('employee')
        buffer = io.BytesIO()
        if tl_id is None:
            teamleads_sheet_download(buffer=buffer, from_date=from_date, to_date=to_date, tl_ids=tl_ids)
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename='TeamLeads_Report.xlsx')
        else:
            teamlead_sheet_download_2(buffer=buffer, from_date=from_date, to_date=to_date, tl_id=tl_id)
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename=request.POST.get('employee_name','Team Lead')+' Report.xlsx')
        
            # artist_individual_sheet_download(buffer=buffer, from_date=from_date, to_date=to_date, artist_id=artist_id)
            # buffer.seek(0)
            # return FileResponse(buffer, as_attachment=True, filename=request.POST.get('employee_name','TeamLead')+' Report.xlsx')
    else:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        lead_id = request.GET['lead_id']
        buffer = io.BytesIO()
        teamlead_sheet_download(buffer, start_date, end_date, lead_id)
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='TeamLead_Report.xlsx')

def export_leads_report(request):
    if request.POST.get('from_date', None) is not None:
        lead = request.POST.get('lead')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        tl_ids = []
        tl_id = None
        if request.POST.get('employees', None) is not None:
            for rid in request.POST['employees'].split('|'):
                tl_ids.append(rid)
        else:
            tl_id = request.POST.get('employee')
        buffer = io.BytesIO()
        if tl_id is None:
            leads_sheet_download(buffer=buffer, from_date=from_date, to_date=to_date, tl_ids=tl_ids, lead=lead)
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename='Leads_Report.xlsx')
        else:
            lead_sheet_download_2(buffer=buffer, from_date=from_date, to_date=to_date, tl_id=tl_id, lead=lead)
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename=request.POST.get('employee_name','Lead')+' Report.xlsx')
    else:
        return Response({"msg":"Invalid Request"})

def allartistlist(request):
    buffer = io.BytesIO()
    allartistlist_sheet_download(buffer=buffer)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='artists_list.xlsx')

def export_artist_report(request):
    from_date = request.POST.get('from_date')
    to_date = request.POST.get('to_date')
    artist_ids = []
    artist_id = None
    if request.POST.get('employees', None) is not None:
        for rid in request.POST['employees'].split('|'):
            artist_ids.append(rid)
    else:
        artist_id = request.POST.get('employee')

    buffer = io.BytesIO()
    if artist_id is None:
        artist_sheet_download(buffer=buffer, from_date=from_date, to_date=to_date, artist_ids=artist_ids)
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='Artists_Report.xlsx')
    else:
        artist_individual_sheet_download(buffer=buffer, from_date=from_date, to_date=to_date, artist_id=artist_id)
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=request.POST.get('employee_name','Artist')+' Report.xlsx')

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
    projects = Projects.objects.all().exclude(status="ARCHIVED")
    context = {
        'clients': clients,
        'projects': projects
    }
    return render(request, 'production/client_reports.html', context)

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

def tasks_export(request):
    shot_id =None
    if 'shot_id' in request.GET:
        shot_id = request.GET['shot_id']
    # print(shot_id)
    buffer = io.BytesIO()
    tasks_download(buffer=buffer, shot_id=shot_id)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='shot_tasks.xlsx')

def shotdaylogs_export(request):
    shotdaylogs_ids =[]
    if request.POST.get('shotdaylogs_ids', None) is not None:
        for rid in request.POST['shotdaylogs_ids'].split('|'):
            shotdaylogs_ids.append(rid)
    # print(shotdaylogs_ids)
    buffer = io.BytesIO()
    shot_daylogs_download(buffer=buffer,shotdaylogs_ids=shotdaylogs_ids)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='shot_%logs_report.xlsx')

def shot_day_logs_export(request):
    from_date = request.POST.get('from_date')
    to_date = request.POST.get('to_date')
    shot_ids = []
    if request.POST.get("shot_ids", None) is not None:
        for rid in request.POST["shot_ids"].split('|'):
            shot_ids.append(rid)
    # print(shot_ids)
    buffer = io.BytesIO()
    shotday_logs_sheet_download(buffer=buffer, from_date=from_date, to_date=to_date, shot_ids=shot_ids)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='shotdays_logs_Report.xlsx')

def taskdaylogs_export(request):
    taskdaylogs_ids = []
    if request.POST.get('taskdaylogs_ids', None) is not None:
        for rid in request.POST['taskdaylogs_ids'].split('|'):
            taskdaylogs_ids.append(rid)
    buffer = io.BytesIO()
    task_daylogs_download(buffer=buffer,taskdaylogs_ids=taskdaylogs_ids)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='task_%logs_report.xlsx')

def projects(request):
    projects = Projects.objects.select_related('client', 'org_status').all()
    project_data = []
    for project in projects:
        totalshots = Shots.objects.prefetch_related('timelogs','artists','artists__role','artists__department','artists__role__permissions').select_related('sequence', 'task_type',
                                                                                 'sequence__project',
                                                                                 'sequence__project__client', 'status',
                                                                                 'complexity',
                                                                                 'team_lead', 'artist', 'location',
                                                                                 'sequence__project__client__locality','status__status_segregation','supervisor','hod').filter(
            sequence__project=project).count()
        yts = Shots.objects.prefetch_related('timelogs','artists','artists__role','artists__department','artists__role__permissions').select_related('sequence', 'task_type',
                                                                                 'sequence__project',
                                                                                 'sequence__project__client', 'status',
                                                                                 'complexity',
                                                                                 'team_lead', 'artist', 'location',
                                                                                 'sequence__project__client__locality','status__status_segregation','supervisor','hod').filter(sequence__project=project,
                                                                                         status__code__in=['ATL', 'YTS',
                                                                                                           'YTA']).count()
        wip = Shots.objects.prefetch_related('timelogs','artists','artists__role','artists__department','artists__role__permissions').select_related('sequence', 'task_type',
                                                                                 'sequence__project',
                                                                                 'sequence__project__client', 'status',
                                                                                 'complexity',
                                                                                 'team_lead', 'artist', 'location',
                                                                                 'sequence__project__client__locality','status__status_segregation','supervisor','hod').filter(sequence__project=project,
                                                                                         status__code__in=['WIP', 'LAP',
                                                                                                           'LRT', 'STQ',
                                                                                                           'STC',
                                                                                                           'IRT']).count()
        completed = Shots.objects.prefetch_related('timelogs','artists','artists__role','artists__department','artists__role__permissions').select_related('sequence', 'task_type',
                                                                                 'sequence__project',
                                                                                 'sequence__project__client', 'status',
                                                                                 'complexity',
                                                                                 'team_lead', 'artist', 'location',
                                                                                 'sequence__project__client__locality','status__status_segregation','supervisor','hod').filter(
            sequence__project=project, status__code__in=['IAP', 'DTC', 'CAP']).count()
        _dict = {'project_id': project.id,
                 'name': project.name,
                 'total_shots': totalshots,
                 'yts': yts,
                 'wip': wip,
                 'completed': completed
                 }
        project_data.append(_dict)

    context = {
        'projects': project_data,
    }
    return render(request, 'production/projects.html', context)

def clientProjects(request, client_id):
    projects = Projects.objects.filter(client=client_id).all()
    project_data = []
    for project in projects:
        totalshots = Shots.objects.select_related('sequence__project', 'sequence', 'task_type',
                                                  'sequence__project__client',
                                                  'status', 'complexity', 'team_lead', 'artist', 'qc_name', 'location',
                                                  'sequence__project__client__locality').filter(
            sequence__project=project).count()
        yts = Shots.objects.select_related('sequence__project', 'sequence', 'task_type', 'sequence__project__client',
                                           'status', 'complexity', 'team_lead', 'artist', 'qc_name', 'location',
                                           'sequence__project__client__locality').filter(sequence__project=project,
                                                                                         status__code__in=['ATL', 'YTS',
                                                                                                           'YTA']).count()
        wip = Shots.objects.select_related('sequence__project', 'sequence', 'task_type', 'sequence__project__client',
                                           'status', 'complexity', 'team_lead', 'artist', 'qc_name', 'location',
                                           'sequence__project__client__locality').filter(sequence__project=project,
                                                                                         status__code__in=['WIP', 'LAP',
                                                                                                           'LRT', 'STQ',
                                                                                                           'STC',
                                                                                                           'IRT']).count()
        completed = Shots.objects.select_related('sequence__project', 'sequence', 'task_type',
                                                 'sequence__project__client',
                                                 'status', 'complexity', 'team_lead', 'artist', 'qc_name', 'location',
                                                 'sequence__project__client__locality').filter(
            sequence__project=project, status__code__in=['IAP', 'DTC', 'CAP']).count()
        _dict = {'project_id': project.id,
                 'name': project.name,
                 'total_shots': totalshots,
                 'yts': yts,
                 'wip': wip,
                 'completed': completed
                 }
        project_data.append(_dict)
    context = {
        'projects': project_data
    }
    return render(request, 'production/projects.html', context)

def clients(request):
    # clients = Clients.objects.select_related('locality').all()
    # client_data = []
    # totalshots = Shots.objects.select_related('sequence__project', 'sequence', 'task_type', 'sequence__project__client',
    #                                           'status', 'complexity', 'team_lead', 'artist', 'qc_name', 'location',
    #                                           'sequence__project__client__locality').filter(
    #     sequence__project__client__in=[x.id for x in clients]).values('id', 'sequence__project__client__id')
    # yts = 0
    # yts = Shots.objects.select_related('sequence__project', 'sequence', 'task_type', 'sequence__project__client',
    #                                    'status', 'complexity', 'team_lead', 'artist', 'qc_name', 'location',
    #                                    'sequence__project__client__locality').filter(
    #     sequence__project__client__in=[x.id for x in clients],status__code__in=['YTA', 'ATL','YTS']).values('id', 'sequence__project__client__id','status__code')
    # wip = 0
    # completed = 0
    # print(totalshots)
    # for client in clients:
    #
    #     # totalCount = Shots.objects.select_related('sequence__project','sequence', 'task_type', 'sequence__project__client',
    #     #                                           'status', 'complexity', 'team_lead', 'artist', 'qc_name', 'location',
    #     #                                           'sequence__project__client__locality').filter(sequence__project__client=client).annotate(each_status = Count('status'))
    #     # print(totalCount[0].each_status)
    #     totalshots = Shots.objects.select_related('sequence__project','sequence', 'task_type', 'sequence__project__client',
    #                                               'status', 'complexity', 'team_lead', 'artist', 'qc_name', 'location',
    #                                               'sequence__project__client__locality').filter(sequence__project__client=client).count()
    #     yts = 0
    #     wip = 0
    #     completed = 0
    #     # yts = Shots.objects.select_related('sequence__project','sequence', 'task_type', 'sequence__project__client',
    #     #                                     'status', 'complexity', 'team_lead', 'artist', 'qc_name', 'location',
    #     #                                     'sequence__project__client__locality').filter(sequence__project__client=client,
    #     #                                                                                     status__code__in=['YTA', 'ATL', 'YTS']).count()
    #     # wip = Shots.objects.select_related('sequence__project','sequence', 'task_type', 'sequence__project__client',
    #     #                                     'status', 'complexity', 'team_lead', 'artist','qc_name', 'location',
    #     #                                     'sequence__project__client__locality').filter(sequence__project__client=client,
    #     #                                                                                     status__code__in=['WIP', 'STC', 'LRT', 'STQ', 'IRT', 'LAP']).count()
    #     # completed = Shots.objects.select_related('sequence__project','sequence', 'task_type', 'sequence__project__client',
    #     #                                          'status', 'complexity', 'team_lead', 'artist', 'qc_name', 'location',
    #     #                                          'sequence__project__client__locality').filter(sequence__project__client=client,
    #     #                                                                                        status__code__in=['CAP', 'DTC', 'IAP']).count()
    #     _dict = {
    #         'client_id': client.id,
    #         'client_name': client.name,
    #         'total_shots': totalshots,
    #         'yts': yts,
    #         'wip': wip,
    #         'completed': completed,
    #     }
    #     client_data.append(_dict)
    #     break;
    clients = Clients.objects.select_related('locality').all()
    # status = Shots.objects.values('status__code').annotate(status_count=Count('status')).values('status__code','status_count')
    # print(status)
    totalshots_i = Shots.objects.select_related('sequence__project', 'sequence', 'task_type',
                                                'sequence__project__client',
                                                'status', 'complexity', 'team_lead', 'artist', 'qc_name', 'location',
                                                'sequence__project__client__locality').filter(
        sequence__project__client__in=[x.id for x in clients]).values('id', 'sequence__project__client__id','sequence__project__client__name')
    yts_i = Shots.objects.select_related('sequence__project', 'sequence', 'task_type', 'sequence__project__client',
                                         'status', 'complexity', 'team_lead', 'artist', 'qc_name', 'location',
                                         'sequence__project__client__locality').filter(
        sequence__project__client__in=[x.id for x in clients], status__code__in=['YTA', 'ATL', 'YTS']).values('id',
                                                                                                              'sequence__project__client__id','sequence__project__client__name')
    wip_i = Shots.objects.select_related('sequence__project', 'sequence', 'task_type', 'sequence__project__client',
                                         'status', 'complexity', 'team_lead', 'artist', 'qc_name', 'location',
                                         'sequence__project__client__locality').filter(
        sequence__project__client__in=[x.id for x in clients],
        status__code__in=['WIP', 'STC', 'LRT', 'STQ', 'IRT', 'LAP']).values('id',
                                                                            'sequence__project__client__id','sequence__project__client__name')
    completed_i = Shots.objects.select_related('sequence__project', 'sequence', 'task_type',
                                               'sequence__project__client',
                                               'status', 'complexity', 'team_lead', 'artist', 'qc_name', 'location',
                                               'sequence__project__client__locality').filter(
        sequence__project__client__in=[x.id for x in clients], status__code__in=['CAP', 'DTC', 'IAP']).values('id',
                                                                                                              'sequence__project__client__id','sequence__project__client__name')
    r_data = {}

    for x in totalshots_i:
        ClinetKey = 'key' + str(x['sequence__project__client__id']);
        if r_data.get(ClinetKey, None) is None:
            r_data[ClinetKey] = {
                'client_id': x['sequence__project__client__id'],
                'client_name': x['sequence__project__client__name'],
                'totalshots': 0,
                'yts': 0,
                'wip': 0,
                'completed': 0,
            }
        r_data[ClinetKey]['totalshots'] = r_data[ClinetKey]['totalshots'] + 1
    for x in yts_i:
        ClinetKey = 'key' + str(x['sequence__project__client__id']);
        if r_data.get(ClinetKey, None) is None:
            r_data[ClinetKey] = {
                'client_id': x['sequence__project__client__id'],
                'client_name': x['sequence__project__client__name'],
                'totalshots': 0,
                'yts': 0,
                'wip': 0,
                'completed': 0,
            }
        r_data[ClinetKey]['yts'] = r_data[ClinetKey]['yts'] + 1
    for x in wip_i:
        ClinetKey = 'key' + str(x['sequence__project__client__id']);
        if r_data.get(ClinetKey, None) is None:
            r_data[ClinetKey] = {
                'client_id': x['sequence__project__client__id'],
                'client_name': x['sequence__project__client__name'],
                'totalshots': 0,
                'yts': 0,
                'wip': 0,
                'completed': 0,
            }
        r_data[ClinetKey]['wip'] = r_data[ClinetKey]['wip'] + 1
    for x in completed_i:
        ClinetKey = 'key' + str(x['sequence__project__client__id']);
        if r_data.get(ClinetKey, None) is None:
            r_data[ClinetKey] = {
                'client_id': x['sequence__project__client__id'],
                'client_name': x['sequence__project__client__name'],
                'totalshots': 0,
                'yts': 0,
                'wip': 0,
                'completed': 0,
            }
        r_data[ClinetKey]['completed'] = r_data[ClinetKey]['completed'] + 1
    context = {
        # 'clients': client_data
    }
    return render(request, 'production/clients.html', context)

def my_task(request):
    """
    Production Shots View
    :param request:
    :return:
    """
    status = ShotStatus.objects.all()
    clients = Clients.objects.all()
    projects = Projects.objects.exclude(status="ARCHIVED").all()
    task_type = Task_Type.objects.all()
    location = Location.objects.all()
    locality = Locality.objects.all()
    leads = Employee.objects.filter(role__name="TEAM LEAD").all()

    context = {
        'status': status,
        'clients': clients,
        'projects': projects,
        'task_type': task_type,
        'location': location,
        'locality': locality,
        'leads': leads,
        'user': request.user
    }
    return render(request, 'production/my_task.html', context)

class DefaultJson(APIView):
    def get(self, request, format=None):
        return Response({
                "user" : json.loads(json.dumps(EmployeeSerializer(Employee.objects.get(pk=request.user.employee.id)).data, default=str)),
                "userRole" : json.loads(json.dumps(RoleSerializer(Role.objects.get(name=request.user.employee.role)).data, default=str)),
                "userParents": json.loads(json.dumps(EmployeeRoleBindingSerializer(EmployeeRoleBinding.objects.filter(employee=request.user.employee.id), many=True).data, default=str)),
                "userCrossBinding": json.loads(json.dumps(RoleRelationshipBindingSerializer(RoleRelationshipBinding.objects.filter(employee__id=request.user.employee.id), many=True).data, default=str)),
                "roleCrossBinding": json.loads(json.dumps(RoleRelationshipBindingSerializer(RoleRelationshipBinding.objects.filter(department=request.user.employee.department,role=request.user.employee.role), many=True).data, default=str)),
                "departmentCrossBinding": json.loads(json.dumps(RoleRelationshipBindingSerializer(RoleRelationshipBinding.objects.filter(department=request.user.employee.department,role=None), many=True).data, default=str)),
                # "assignmentStepsOrder": json.loads(json.dumps(AssignmentStepsOrderSerializer(AssignmentStepsOrder.objects.filter(department=request.user.employee.department), many=True).data, default=str)),
                "workingDays": json.loads(json.dumps(OrganizationWorkingDaysSerializer(OrganizationWorkingDays.objects.all(), many=True).data, default=str)),
                "departments": json.loads(json.dumps(DepartmentSerializer(Department.objects.all(), many=True).data, default=str)),
                "rolePipelineSteps" : json.loads(json.dumps(PipelineStepsSerializer(RolePipelineSteps.objects.filter(department=request.user.employee.department,role=request.user.employee.role),many=True).data, default=str)),
                "StatusCodes" : json.loads(json.dumps(StatusSerializer(ShotStatus.objects.all(), many=True).data, default=str)),
                'ignoreStatusCodes': [], #['IAP','DTC'],
                "organizationHolidayTypes" : json.loads(json.dumps(OrganizationHolidayTypesSerializer(OrganizationHolidayTypes.objects.all(), many=True).data, default=str)),
                "workingDayTypes" : json.loads(json.dumps(WorkingDayTypesSerializer(WorkingDayTypes.objects.all(), many=True).data, default=str)),
                })

# def srtReplace(data={},fr=[['"',""]]):
#     for x in data:
#         try:
#             if isinstance(data[x], list) or isinstance(data[x], dict):
#                 if isinstance(data[x], list):
#                     for xj in range(len(data[x])):
#                         data[x][xj] = srtReplace(data=data[x][xj],fr=fr)
#                 else:
#                     data[x] = srtReplace(data=data[x],fr=fr)

#             elif isinstance(data[x], str):
#                 for xi in fr:
#                     data[x] = data[x].replace(xi[0], xi[1])
#         except Exception as e:
#             print(e,x,data[x])
#     return data


def default_js(request):
    """
    """
    context = {
        'page_data': {
            "user" : json.loads(json.dumps(EmployeeSerializer(Employee.objects.get(pk=request.user.employee.id)).data, default=str)),
            "userRole" : json.loads(json.dumps(RoleSerializer(Role.objects.get(name=request.user.employee.role)).data, default=str)),
            "userParents": json.loads(json.dumps(EmployeeRoleBindingSerializer(EmployeeRoleBinding.objects.filter(employee=request.user.employee.id), many=True).data, default=str)),
            "userCrossBinding": json.loads(json.dumps(RoleRelationshipBindingSerializer(RoleRelationshipBinding.objects.filter(employee__id=request.user.employee.id), many=True).data, default=str)),
            "roleCrossBinding": json.loads(json.dumps(RoleRelationshipBindingSerializer(RoleRelationshipBinding.objects.filter(department=request.user.employee.department,role=request.user.employee.role), many=True).data, default=str)),
            "departmentCrossBinding": json.loads(json.dumps(RoleRelationshipBindingSerializer(RoleRelationshipBinding.objects.filter(department=request.user.employee.department,role=None), many=True).data, default=str)),
            # "assignmentStepsOrder": json.loads(json.dumps(AssignmentStepsOrderSerializer(AssignmentStepsOrder.objects.filter(department=request.user.employee.department), many=True).data, default=str)),
            "workingDays": json.loads(json.dumps(OrganizationWorkingDaysSerializer(OrganizationWorkingDays.objects.all(), many=True).data, default=str)),
            "departments": json.loads(json.dumps(DepartmentSerializer(Department.objects.all(), many=True).data, default=str)),
            "taskTypes": json.loads(json.dumps(TaskTypeSerializer(Task_Type.objects.all(), many=True).data, default=str)),
            "locations": json.loads(json.dumps(LocationSerializer(Location.objects.all(), many=True).data, default=str)),
            "rolePipelineSteps" : json.loads(json.dumps(PipelineStepsSerializer(RolePipelineSteps.objects.filter(department=request.user.employee.department,role=request.user.employee.role),many=True).data, default=str)),
            "StatusCodes" : json.loads(json.dumps(StatusSerializer(ShotStatus.objects.all(), many=True).data, default=str)),
            'ignoreStatusCodes': [], #['IAP','DTC'],
            "organizationHolidayTypes" : json.loads(json.dumps(OrganizationHolidayTypesSerializer(OrganizationHolidayTypes.objects.all(), many=True).data, default=str)),
            "workingDayTypes" : json.loads(json.dumps(WorkingDayTypesSerializer(WorkingDayTypes.objects.all(), many=True).data, default=str)),
            }
        }
    if context['page_data']["user"].get("address",None) is not None:
        del context['page_data']["user"]["address"]
        del context['page_data']["user"]["profile"]["password"]

    return render(request, 'production/defaults.js', context, 'text/javascript' )
    # return render(request, 'production/defaults.js', {}, 'text/javascript' )

def my_team(request):
    """
    My Team
    """
    context = {
        'user': request.user
    }

    return render(request, 'production/my_team.html', context)

def task_daylogs(request):
    context = {
        'user': request.user
    }
    return render(request, 'production/taskday_logs.html', context)

def shot_daylogs(request):
    context = {
        'user': request.user
    }

    return render(request, 'production/shotday_logs.html', context)