import json

from production.models import DayLogs, Assignments, ClientVersions, MyTask
from production.serializers import DayLogsSerializer, AssignmentSerializer, ClientVersionsSerializer


def calculate_artist_data(artist_id, start_date, end_date):

    data = {
        "total_shots": 'N/A',
        "achieved_mandays": 'N/A',
        "yts": 'N/A',
        "wip": 'N/A',
        "completed": 'N/A',
        "total_mandays" : 'N/A',
        "act_vs_ach": 'N/A',
        "retakes": 'N/A',
        "retakes_per": 'N/A',
        "yts_per": 'N/A',
        "wip_per": 'N/A',
        "comp_per": 'N/A'
    }
    return data
