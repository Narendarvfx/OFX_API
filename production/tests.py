import json
from unittest import TestCase

from production.models import Shots
from production.serializers import ShotsSerializer


class DepartmentTestCase(TestCase):
    def test_dept_version(self):
        client_version = Shots.objects.filter(task_type__name="PAINT",creation_date__range=["2022-03-04T00:00:00",
                                                                                                      "2022-04-25T23:59:59"])
        client_version_serializer = ShotsSerializer(client_version, many=True)
        assign_data = client_version_serializer.data
        length = len(assign_data)
        n = 0
        wip = 0
        completed = 0
        uploaded = 0
        yts = 0
        total_mandays = 0
        while n < length:
            if assign_data[n]["status"]['code'] in ["YTA", "YTS", "ATL"]:
                yts += 1

            if assign_data[n]["status"]['code'] in ["WIP", "STQ", "STC", "IRT", "LRT", "LAP"]:
                wip += 1

            if assign_data[n]["status"]['code'] in ["IAP", "DTC", "CAP"]:
                completed += 1

            if assign_data[n]["status"]['code'] == "DTC":
                uploaded += 1

            if n == length - 1:
                break
            total_mandays += assign_data[n]['bid_days']
            n += 1
        print("WIP:", wip)
        print("Completed: ", completed)
        print("Uploaded: ", uploaded)
        print("YTS: ", yts)
        print("Total Mandays: ", total_mandays)
# Create your tests here.
