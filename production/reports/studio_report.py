import datetime
import json

import xlsxwriter

from production.models import DayLogs, Assignments, Shots, ShotVersions, QCVersions, ClientVersions
from production.serializers import DayLogsSerializer, AssignmentSerializer, ShotsSerializer, ShotVersionsSerializer, \
    QcVersionsSerializer, ClientVersionsSerializer


def studio_sheet_download(buffer, start_date, end_date):
    workbook = xlsxwriter.Workbook(buffer)

    worksheet = workbook.add_worksheet()

    shot_queryset = Shots.objects.select_related('sequence', 'task_type', 'sequence__project',
                                                 'sequence__project__client', 'status', 'complexity', 'team_lead',
                                                 'artist', 'location').filter(
                                                                              creation_date__range=[start_date,
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

    while n < length:
        if shot_data[n]["status"]['code'] in ["YTA", "YTS", "ATL"]:
            yts += 1

        if shot_data[n]["status"]['code'] in ["WIP", "STQ", "STC", "IRT", "LRT", "LAP"]:
            wip += 1

        if shot_data[n]["status"]['code'] in ["IAP", "DTC", "CAP"]:
            completed += 1

        if shot_data[n]["status"]['code'] == "DTC":
            uploaded += 1

        achieved_mandays += shot_data[n]['achieved_mandays']
        total_mandays += shot_data[n]['bid_days']
        if n == length - 1:
            break
        n += 1

    act_vs_ach = total_mandays - achieved_mandays
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow'})
    fmerge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#22B2E2'})

    # Merge 3 cells.
    worksheet.merge_range('A1:Q1', 'STUDIO REPORT', merge_format)
    worksheet.merge_range('A2:Q3', str(start_date) + "  ---  " + str(end_date), merge_format)
    worksheet.merge_range('A4:D6', "Total Shots : " + str(length), fmerge_format)
    worksheet.merge_range('E4:G6', "Actual ManDays : " + str(round(total_mandays)), fmerge_format)
    worksheet.merge_range('H4:J6', "Achieved ManDays : " + str(round(achieved_mandays)), fmerge_format)
    worksheet.merge_range('K4:M6', "Actual vs Achieved : " + str(round(act_vs_ach)), fmerge_format)
    worksheet.merge_range('N4:Q6', "Total Artists : 10", fmerge_format)

    worksheet.merge_range('A7:D8', "YTS : " + str(round(yts)), fmerge_format)
    worksheet.merge_range('E7:G8', "WIP : " + str(round(wip)), fmerge_format)
    worksheet.merge_range('H7:J8', "HOLD : 0", fmerge_format)
    worksheet.merge_range('K7:M8', "COMPLETED : " + str(round(completed)), fmerge_format)
    worksheet.merge_range('N7:Q8', "RETAKES : " + str(total_retakes), fmerge_format)

    workbook.close()
    return buffer