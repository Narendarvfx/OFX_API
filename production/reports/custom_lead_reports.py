import json

from production.models import DayLogs, Assignments, ClientVersions
from production.serializers import DayLogsSerializer, AssignmentSerializer, ClientVersionsSerializer


def calculate_data(lead_id, start_date, end_date):
    daylogs = DayLogs.objects.filter(updated_date__range=[start_date, end_date],
                                     shot__team_lead__profile_id=lead_id).select_related('shot', 'artist', 'updated_by',
                                                                                         'shot__sequence',
                                                                                         'shot__sequence__project',
                                                                                         'shot__status',
                                                                                         'shot__task_type',
                                                                                         'shot__location',
                                                                                         'shot__team_lead',
                                                                                         'shot__artist',
                                                                                         'shot__sequence__project__client',
                                                                                         'shot__sequence__project__client__locality')
    serializer = DayLogsSerializer(daylogs, many=True)
    json_dump = json.dumps(serializer.data)
    daylog_data = json.loads(json_dump)
    ach_mandays = 0
    shots = []
    for dat in daylog_data:
        ach_mandays += dat['consumed_man_day']
        if dat['shot'] not in shots:
            shots.append(dat['shot'])
    total_retakes = 0
    retakes_per = 0
    yts_per = 0
    wip_per = 0
    comp_per = 0
    for shot in shots:
        client_version = ClientVersions.objects.select_related('status','sent_by', 'verified_by').filter(shot=shot,
                                                                                modified_date__range=[start_date,
                                                                                                      end_date])
        client_version_serializer = ClientVersionsSerializer(client_version, many=True)
        client_version_json_dump = json.dumps(client_version_serializer.data)
        client_version_data = json.loads(client_version_json_dump)
        total_retakes += len(client_version_data)

    assign_data = assign_list(start_date, end_date, lead_id)

    #### Retake Percentage Calculation ####
    total_uploaded = assign_data[4]
    total_shots = len(shots) + assign_data[0]
    act_vs_ach = assign_data[3] - ach_mandays
    try:
        yts_per = round(assign_data[0] / total_shots * 100)
        wip_per = round(assign_data[1] / total_shots * 100)
        comp_per = round(assign_data[2] / total_shots * 100)
        retakes_per = round(total_retakes / total_uploaded * 100)
    except ZeroDivisionError:
        retakes_per = "N/A"

    data = {
        "total_shots": round(total_shots),
        "achieved_mandays": round(ach_mandays),
        "yts": round(assign_data[0]),
        "wip": round(assign_data[1]),
        "completed": round(assign_data[2]),
        "total_mandays" : round(assign_data[3]),
        "act_vs_ach": round(act_vs_ach),
        "retakes": round(total_retakes),
        "retakes_per": retakes_per,
        "yts_per": round(yts_per / 5) * 5,
        "wip_per": round(wip_per / 5) * 5,
        "comp_per": round(comp_per / 5) * 5
    }
    return data

def assign_list(start_date, end_date, lead_id):
    lead = Assignments.objects.filter(lead_id=lead_id, assigned_date__range=[start_date, end_date
                                                                            ]).select_related('lead',
                                                                                              'shot',
                                                                                              'shot__sequence',
                                                                                              'shot__sequence__project',
                                                                                              'shot__sequence__project__client',
                                                                                              'shot__status',
                                                                                              'shot__task_type',
                                                                                              'assigned_by',
                                                                                              'shot__artist',
                                                                                              'shot__team_lead')

    serializer = AssignmentSerializer(lead, many=True)
    json_dump = json.dumps(serializer.data)
    assign_data = json.loads(json_dump)
    length = len(assign_data)
    n = 0
    wip = 0
    completed = 0
    uploaded = 0
    yts = 0
    total_mandays = 0
    while n < length:
        if assign_data[n]['shot']["status"]['code'] in ["YTS", "ATL"]:
            yts += 1

        if assign_data[n]['shot']["status"]['code'] in ["WIP", "STQ", "STC", "IRT", "LRT", "LAP"]:
            wip += 1

        if assign_data[n]['shot']["status"]['code'] in ["IAP", "DTC", "CAP"]:
            completed += 1

        if assign_data[n]['shot']["status"]['code'] == "DTC":
            uploaded += 1

        if n == length - 1:
            break
        total_mandays += assign_data[n]['shot']['bid_days']
        n += 1

    return yts, wip, completed, total_mandays, uploaded