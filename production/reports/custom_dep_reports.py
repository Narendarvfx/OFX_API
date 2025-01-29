#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

from production.models import Shots, ClientVersions
from production.serializers import ShotsSerializer, ClientVersionsSerializer


def calculate_dept_data(dept, start_date, end_date):
    shot_queryset = Shots.objects.select_related('sequence', 'task_type', 'sequence__project',
                                                    'sequence__project__client', 'status', 'complexity', 'team_lead',
                                                'artist', 'location').filter(task_type__name=dept, creation_date__range=[start_date,
                                                                                         end_date])
    shot_serializer = ShotsSerializer(shot_queryset, many=True)
    shot_data = shot_serializer.data
    length = len(shot_data)
    n = 0
    wip = 0
    completed = 0
    uploaded = 0
    yts = 0
    total_mandays = 0
    achieved_mandays = 0
    total_retakes = 0
    retakes_per = 0
    yts_per = 0
    wip_per = 0
    comp_per = 0
    while n < length:
        if shot_data[n]["status"]['code'] in ["YTA", "YTS", "ATL"]:
            yts += 1

        if shot_data[n]["status"]['code'] in ["WIP", "STQ", "STC", "IRT", "LRT", "LAP"]:
            wip += 1

        if shot_data[n]["status"]['code'] in ["IAP", "DTC", "CAP"]:
            completed += 1

        if shot_data[n]["status"]['code'] == "DTC":
            uploaded += 1

        if n == length - 1:
            break
        achieved_mandays += shot_data[n]['achieved_mandays']
        total_mandays += shot_data[n]['bid_days']

        client_version = ClientVersions.objects.select_related('shot','sent_by','verified_by','status').filter(shot=shot_data[n]['id'],
                                                                                modified_date__range=[start_date,
                                                                                                      end_date])
        client_version_serializer = ClientVersionsSerializer(client_version, many=True)
        client_version_data = client_version_serializer.data
        total_retakes += len(client_version_data)
        n += 1

    act_vs_ach = total_mandays - achieved_mandays
    try:
        yts_per = round(yts / length * 100)
        wip_per = round(wip / length * 100)
        comp_per = round(completed / length * 100)
        retakes_per = round(total_retakes / uploaded * 100)
    except ZeroDivisionError:
        retakes_per = "N/A"

    data = {
        "yts" : round(yts),
        "wip": round(wip),
        "completed": round(completed),
        "total_mandays": round(total_mandays),
        "total_shots": round(length),
        "achieved_mandays": round(achieved_mandays),
        "act_vs_ach": round(act_vs_ach),
        "retakes": round(total_retakes),
        "retakes_per": retakes_per,
        "yts_per": round(yts_per/5)*5,
        "wip_per": round(wip_per/5)*5,
        "comp_per": round(comp_per/5)*5
    }

    return data