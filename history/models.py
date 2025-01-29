import uuid
from django.db import models
from hrm.models import Employee
from production.models import Shots, MyTask, Assignments, Clients, Projects, DayLogs, TaskDayLogs, Sequence, ShotStatus, \
    Task_Type, Complexity, Location, Locality

historyMaping = {}
Types = (
    ("POST", "POST"),
    ("PUT", "PUT"),
    ("DELETE", "DELETE")
)


# Create your models here.
class ClientsHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    target = models.ForeignKey(Clients, on_delete=models.DO_NOTHING, null=True, blank=True)
    impact = models.CharField(max_length=100, default="")
    dataField = models.CharField(max_length=100)
    fromData = models.TextField(null=True, blank=True)
    toData = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=1024, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    requestType = models.CharField(max_length=300, null=True, choices=Types)
    who = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if len(self.impact) == 0 and self.target is not None:
            self.impact = self.target.name
            super(ClientsHistory, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Clients History"


historyMaping['ClientsHistory'] = {
    'POST': {
        'name': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'STRING',
            "title": "Client Created",
            "message": "#!to.name!# Client Created"
        },
    },
    'PUT': {
        'name': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'STRING',
            "title": "Client Name is updated",
            "message": "Name is updated from #!from.name!# to #!to.name!#"
        },
        'email': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'STRING',
            "title": "Client Email is updated",
            "message": "Email is updated from #!from.email!# to #!to.email!#"
        },
        'country': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'STRING',
            "title": "Client Country is updated",
            "message": "Country is updated from #!from.country!# to #!to.country!#"
        },
        'locality': {
            "model": Locality,
            "queryFeilds": ['locality__id', 'locality__name'],
            "dataType": 'STRING',
            "title": "Client Locality is updated",
            "message": "Locality is updated from #!from.locality__name!# to #!to.locality__name!#"
        },
        'status': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'STRING',
            "title": "Client Status is updated",
            "message": "Status is updated from #!from.status!# to #!to.status!#"
        },
    },
    'DELETE': {
        'name': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'STRING',
            "title": "Client Deleted",
            "message": "#!from.name!# Client Deleted"
        },
    },
}


# Create your models here.
class ProjectsHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    target = models.ForeignKey(Projects, on_delete=models.DO_NOTHING, null=True, blank=True)
    parent_target = models.ForeignKey(Clients, on_delete=models.DO_NOTHING, null=True, blank=True)
    impact = models.CharField(max_length=100, default="")
    dataField = models.CharField(max_length=100)
    fromData = models.TextField(null=True, blank=True)
    toData = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=1024, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    requestType = models.CharField(max_length=300, null=True, choices=Types)
    who = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if len(self.impact) == 0 and self.target is not None:
            self.impact = self.target.name
            super(ProjectsHistory, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Projects History"


historyMaping['ProjectsHistory'] = {
    'POST': {
        'name': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'STRING',
            "title": "Project Created",
            "message": "#!to.name!# Project Created"
        },
    },
    'PUT': {
        'client': {
            "model": Clients,
            "queryFeilds": ['client__id', 'client__name'],
            "dataType": 'STRING',
            "title": "Client name is updated",
            "message": "Client is updated from #!from.client__name!# to #!to.client__name!#"
        },
        'name': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'STRING',
            "title": "Project name is updated",
            "message": "Name is updated from #!from.name!# to #!to.name!#"
        },
        'org_status': {
            "model": ShotStatus,
            "queryFeilds": ['org_status__id', 'org_status__code'],
            "dataType": 'STRING',
            "title": "Shot Status is updated",
            "message": "Status is updated from #!from.org_status__code!# to #!to.org_status__code!#"
        },
        'start_date': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'DATETIME',
            "title": "Project Start Date is updated",
            "message": "Start Date is updated from #!from.start_date!# to #!to.start_date!#"
        },
        'description': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'STRING',
            "title": "Project Description is updated",
            "message": "Description is updated from #!from.description!# to #!to.description!#"
        },
        'status': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'STRING',
            "title": "Project Status is updated",
            "message": "Status is updated from #!from.status!# to #!to.status!#"
        },
    },
    'DELETE': {
        'name': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'STRING',
            "title": "Project Deleted",
            "message": "#!from.name!# Project Deleted"
        },
    },
}


# Create your models here.
class SequenceHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    target = models.ForeignKey(Sequence, on_delete=models.DO_NOTHING, null=True, blank=True)
    parent_target = models.ForeignKey(Projects, on_delete=models.DO_NOTHING, null=True, blank=True)
    impact = models.CharField(max_length=100, default=None)
    dataField = models.CharField(max_length=100)
    fromData = models.TextField(null=True, blank=True)
    toData = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=1024, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    requestType = models.CharField(max_length=300, null=True, choices=Types)
    who = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if len(self.impact) == 0 and self.target is not None:
            self.impact = self.target.name
            super(SequenceHistory, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Projects History"


historyMaping['SequenceHistory'] = {
    'POST': {
        'name': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'STRING',
            "title": "Sequence Created",
            "message": "#!to.name!# Sequence Created"
        },
    },
    'PUT': {
        'name': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'STRING',
            "title": "Sequence Name is Updated",
            "message": "#!to.name!# Sequence Name is Updated"
        },
        'project': {
            "model": Projects,
            "queryFeilds": ['project__id', 'project__name'],
            "dataType": 'STRING',
            "title": "Project name is updated",
            "message": "Project is updated from #!from.project__name!# to #!to.project__name!#"
        },
        # 'creation_date': {
        #     "model": None,
        #     "queryFeilds": None,
        #     "dataType": 'DATETIME',
        #     "title": "Sequence Creation Date is updated",
        #     "message": "Creation Date is updated from #!from.creation_date!# to #!to.creation_date!#"
        # },
        'modified_date': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'DATETIME',
            "title": "Sequence Modified Date is updated",
            "message": "Modified Date is updated from #!from.modified_date!# to #!to.modified_date!#"
        },
    },
    'DELETE': {
        'name': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'STRING',
            "title": "Sequence is Deleted",
            "message": "#!from.name!# Sequence is Deleted"
        },
    },
}


# Create your models here.
class ShotsHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    target = models.ForeignKey(Shots, on_delete=models.SET_NULL, null=True, blank=True)
    parent_target = models.ForeignKey(Sequence, on_delete=models.SET_NULL, null=True, blank=True)
    impact = models.CharField(max_length=100, default="")
    dataField = models.CharField(max_length=100)
    fromData = models.TextField(null=True, blank=True)
    toData = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=1024, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    requestType = models.CharField(max_length=300, null=True, choices=Types)
    who = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if len(self.impact) == 0 and self.target is not None:
            self.impact = self.target.name
            super(ShotsHistory, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Shots History"


historyMaping['ShotsHistory'] = {
    'POST': {
        'name': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'STRING',
            "title": "Shot Created",
            "message": "#!to.name!# Shot Created"
        },
    },
    'PUT': {
        'name': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'STRING',
            "title": "Shot Name is updated",
            "message": "Name is updated from #!from.name!# to #!to.name!#"
        },
        'sequence': {
            "model": Sequence,
            "queryFeilds": ['sequence__id', 'sequence__name'],
            "dataType": 'STRING',
            "title": "Shot Sequence name is updated",
            "message": "Sequence name is updated from #!from.sequence__name!# to #!to.sequence__name!#"
        },
        'status': {
            "model": ShotStatus,
            "queryFeilds": ['status__id', 'status__code'],
            "dataType": 'STRING',
            "title": "Status Update",
            "message": "#_who_# updated Status to #!to.status__code!#"
        },
        'type': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'STRING',
            "title": "Type Changed",
            "message": "#_who_# updated the Type to #!to.type!#"
        },
        'task_type': {
            "model": Task_Type,
            "queryFeilds": ['task_type__id', 'task_type__name'],
            "dataType": 'STRING',
            "title": "Task Type Updated",
            "message": "#_who_# has updated the Task Type from #!from.task_type__name!# to #!to.task_type__name!#"
        },
        'actual_start_frame': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'INT',
            "title": "Frame Range Updated",
            "message": "Start Frame is updated from #!from.actual_start_frame!# to #!to.actual_start_frame!#"
        },
        'actual_end_frame': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'INT',
            "title": "Frame Range Updated",
            "message": "End Frame is updated from #!from.actual_end_frame!# to #!to.actual_end_frame!#"
        },
        'work_start_frame': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'INT',
            "title": "Shot Work Start Frame is updated",
            "message": "Work Start Frame is updated from #!from.work_start_frame!# to #!to.work_start_frame!#"
        },
        'work_end_frame': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'INT',
            "title": "Shot Work End Frame is updated",
            "message": "Work End Frame is updated from #!from.work_end_frame!# to #!to.work_end_frame!#"
        },
        'eta': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'DATETIME',
            "title": "Shot ETA is updated",
            "message": "ETA is updated from #!from.eta!# to #!to.eta!#"
        },
        'internal_eta': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'DATETIME',
            "title": "Shot Internal ETA is updated",
            "message": "Internal ETA is updated from #!from.internal_eta!# to #!to.internal_eta!#"
        },
        'start_date': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'DATETIME',
            "title": "Shot Start Date is updated",
            "message": "Start Date is updated from #!from.start_date!# to #!to.start_date!#"
        },
        'end_date': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'DATETIME',
            "title": "Shot End Date is updated",
            "message": "End Date is updated from #!from.end_date!# to #!to.end_date!#"
        },
        'bid_days': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'FLOAT',
            "title": "Shot Bid Days is updated",
            "message": "Bid Days is updated from #!from.bid_days!# to #!to.bid_days!#"
        },
        'internal_bid_days': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'FLOAT',
            "title": "Shot Internal Bid Days are updated",
            "message": "Internal Bid Days is updated from #!from.internal_bid_days!# to #!to.internal_bid_days!#"
        },
        'progress': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'INT',
            "title": "Shot Progress is updated",
            "message": "Progress is updated from #!from.progress!# to #!to.progress!#"
        },
        'description': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'INT',
            "title": "Shot Description is updated",
            "message": "Description is updated from #!from.description!# to #!to.description!#"
        },
        'complexity': {
            "model": Complexity,
            "queryFeilds": ['complexity__id', 'complexity__name'],
            "dataType": 'STRING',
            "title": "Shot Complexity is updated",
            "message": "Complexity is updated from #!from.complexity__name!# to #!to.complexity__name!#"
        },
        'duplicate': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'BOOL',
            "title": "Shot Duplicate is updated",
            "message": "Duplicate is updated from #!from.duplicate!# to #!to.duplicate!#"
        },
        'parentShot': {
            "model": Shots,
            "queryFeilds": ['parentShot__id', 'parentShot__name'],
            "dataType": 'STRING',
            "title": "Parent Shot is updated",
            "message": "Parent Shot is updated from #!from.duplicate!# to #!to.duplicate!#"
        },
        'supervisor': {
            "model": Employee,
            "queryFeilds": ['supervisor__id', 'supervisor__fullName'],
            "dataType": 'STRING',
            "title": "Shot Supervisor is updated",
            "message": "Supervisor is updated from #!from.supervisor__fullName!# to #!to.supervisor__fullName!#"
        },
        'team_lead': {
            "model": Employee,
            "queryFeilds": ['team_lead__id', 'team_lead__fullName'],
            "dataType": 'STRING',
            "title": "Shot Team Lead is updated",
            "message": "Team Lead is updated from #!from.team_lead__fullName!# to #!to.team_lead__fullName!#"
        },
        'artist': {
            "model": Employee,
            "queryFeilds": ['artist__id','artist__fullName'],
            "dataType":'STRING',
            "title": "",
            "message": "Captain is Changed from #!from.artist__fullName!# to #!to.artist__fullName!#"
            },
        'scope_of_work': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'STRING',
            "title": "Shot Scope of Work is updated",
            "message": "Scope of Work is updated from #!from.scope_of_work!# to #!to.scope_of_work!#"
        },
        'qc_name': {
            "model": Employee,
            "queryFeilds": ['qc_name__id', 'qc_name__fullName'],
            "dataType": 'STRING',
            "title": "Shot QC name is Changed",
            "message": "QC name is Changed from #!from.qc_name__fullName!# to #!to.qc_name__fullName!#"
        },
        'pending_mandays': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'FLOAT',
            "title": "Shot Pending Mandays are updated",
            "message": "Pending Mandays are updated from #!from.pending_mandays!# to #!to.pending_mandays!#"
        },
        'achieved_mandays': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'FLOAT',
            "title": "Shot Achieved Mandays are updated",
            "message": "Achieved Mandays are updated from #!from.achieved_mandays!# to #!to.achieved_mandays!#"
        },
        'package_id': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'STRING',
            "title": "Shot Package Id is updated",
            "message": "Package Id is updated from #!from.package_id!# to #!to.package_id!#"
        },
        'estimate_id': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'STRING',
            "title": "Shot Estimate Id is updated",
            "message": "Estimate Id is updated from #!from.estimate_id!# to #!to.estimate_id!#"
        },
        'estimate_date': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'DATETIME',
            "title": "Shot Estimate Date is updated",
            "message": "Estimate Date is updated from #!from.estimate_date!# to #!to.estimate_date!#"
        },
        'location': {
            "model": Location,
            "queryFeilds": ['location__id', 'location__name'],
            "dataType": 'STRING',
            "title": "Shot Location is updated",
            "message": "Location is updated from #!from.location__name!# to #!to.location__name!#"
        },
        'input_path': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'STRING',
            "title": "Shot Input Path is updated",
            "message": "Input Path is updated from #!from.input_path!# to #!to.input_path!#"
        },
        'retake_path': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'STRING',
            "title": "Shot Re-Take Path is updated",
            "message": "Re-Take Path is updated from #!from.retake_path!# to #!to.retake_path!#"
        },
        'output_path': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'STRING',
            "title": "Shot Output Path is updated",
            "message": "Output Path is updated from #!from.output_path!# to #!to.output_path!#"
        },
        'comments': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'STRING',
            "title": "Shot Comments are updated",
            "message": "Comments are updated from #!from.comments!# to #!to.comments!#"
        },
        'version': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'STRING',
            "title": "Shot Version is updated",
            "message": "Version is updated from #!from.version!# to #!to.version!#"
        },
        'submitted_date': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'DATETIME',
            "title": "Shot Submitted Date is updated",
            "message": "Submitted Date is updated from #!from.submitted_date!# to #!to.submitted_date!#"
        },
    },
    'DELETE': {
        'name': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'STRING',
            "title": "Shot is Deleted",
            "message": "#!from.name!# Shot is Deleted"
        },
    },
}
historyMaping['ShotsHelpHistory'] = {
    'POST': {
        'task_type': {
            "model": Task_Type,
            "queryFeilds": ['task_type__id', 'task_type__name'],
            "dataType": 'STRING',
            "title": "Help Shot Created",
            "message": "#!to.task_type__name!# Help Shot Created"
            },
        },
    'PUT': {
        'eta': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'DATETIME',
            "title": "Help Shot ETA is updated",
            "message": "ETA is updated from #!from.eta!# to #!to.eta!#"
        },
        'bid_days': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'FLOAT',
            "title": "Help Shot Bid Days is updated",
            "message": "Bid Days is updated from #!from.bid_days!# to #!to.bid_days!#"
        },
    },
    'DELETE': {
        'task_type': {
            "model": Task_Type,
            "queryFeilds": ['task_type__id', 'task_type__name'],
            "dataType": 'STRING',
            "title": "Help Shot Deleted",
            "message": "#!to.task_type__name!# Help Shot Deleted"
            },
        },
    }


class AssignmentsHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    target = models.ForeignKey(Assignments, on_delete=models.SET_NULL, null=True, blank=True)
    parent_target = models.ForeignKey(Shots, on_delete=models.SET_NULL, null=True, blank=True)
    impact = models.CharField(max_length=100, default="")
    dataField = models.CharField(max_length=100)
    fromData = models.TextField(null=True, blank=True)
    toData = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=1024, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    requestType = models.CharField(max_length=300, null=True, choices=Types)
    who = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if len(self.impact) == 0 and self.target is not None:
            self.impact = self.target.lead.fullName
            super(AssignmentsHistory, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Assignments History"


historyMaping['AssignmentsHistory'] = {
    'POST': {
        'lead': {
            "model": Employee,
            "queryFeilds": ['lead__id', 'lead__fullName'],
            "dataType": 'STRING',
            "title": "Task Assigned",
            "message": "#!to.lead__fullName!# Assignment Created"
        },
    },
    'PUT': {
        'lead': {
            "model": Employee,
            "queryFeilds": ['lead__id', 'lead__fullName'],
            "dataType": 'STRING',
            "title": "Assignment Lead is updated",
            "message": "Lead is updated from #!from.lead__fullName!# to #!to.lead__fullName!#"
        },
        'shot': {
            "model": Shots,
            "queryFeilds": ['shot__id', 'shot__name'],
            "dataType": 'STRING',
            "title": "shot is updated",
            "message": "Shot is updated from #!from.shot__name!# to #!to.shot__name!#"
        },
        'assigned_by': {
            "model": Employee,
            "queryFeilds": ['assigned_by__id', 'assigned_by__fullName'],
            "dataType": 'STRING',
            "title": "Shot Assigned By is updated",
            "message": "Assigned By is updated from #!from.assigned_by__fullName!# to #!to.assigned_by__fullName!#"
        },
        'assigned_date': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'DATETIME',
            "title": "Assignment Assigned Date is updated",
            "message": "Assigned Date is updated from #!from.assigned_date!# to #!to.assigned_date!#"
        },
    },

    'DELETE': {
        'lead': {
            "model": Employee,
            "queryFeilds": ['lead__id', 'lead__fullName'],
            "dataType": 'STRING',
            "title": "Assignment Deleted",
            "message": "#!to.lead__fullName!# Assignment Deleted"
        },
    },
}


class MyTaskHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    target = models.ForeignKey(MyTask, on_delete=models.DO_NOTHING, null=True, blank=True)
    parent_target = models.ForeignKey(Shots, on_delete=models.DO_NOTHING, null=True, blank=True)
    impact = models.CharField(max_length=100, default="")
    dataField = models.CharField(max_length=100)
    fromData = models.TextField(null=True, blank=True)
    toData = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=1024, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    requestType = models.CharField(max_length=300, null=True, choices=Types)
    who = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if len(self.impact) == 0 and self.target is not None:
            self.impact = self.target.artist.fullName
            super(MyTaskHistory, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "MyTask History"


historyMaping['MyTaskHistory'] = {
    'POST': {
        'artist': {
            "model": Employee,
            "queryFeilds": ['artist__id', 'artist__fullName'],
            "dataType": 'STRING',
            "title": "Assigned to $impact$",
            "message": ""
        },
    },
    'PUT': {
        # 'artist': {
        #     "model": Employee,
        #     "queryFeilds": ['artist__id', 'artist__fullName'],
        #     "dataType": 'STRING',
        #     "title": "",
        #     "message": "Captain is Changed from #!from.artist__fullName!# to #!to.artist__fullName!#"
        # },
        'art_percentage': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'INT',
            "title": "$impact$ Task Captain Percentage is updated",
            "message": "Captain Percentage is updated from #!from.art_percentage!# to #!to.art_percentage!#"
        },
        'assigned_bids': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'FLOAT',
            "title": "$impact$ Task Assigned Bids are updated",
            "message": "Assigned Bids are updated from #!from.assigned_bids!# to #!to.assigned_bids!#"
        },
        'start_date': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'DATETIME',
            "title": "$impact$ Task Start Date is updated",
            "message": "Start Date is updated from #!from.start_date!# to #!to.start_date!#"
        },
        'end_date': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'DATETIME',
            "title": "$impact$ Task End Date is updated",
            "message": "End Date is updated from #!from.end_date!# to #!to.end_date!#"
        },
        'eta': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'DATETIME',
            "title": "$impact$ Task ETA is updated",
            "message": "ETA is updated from #!from.eta!# to #!to.eta!#"
        },
        'task_status': {
            "model": ShotStatus,
            "queryFeilds": ['task_status__id', 'task_status__code'],
            "dataType": 'STRING',
            "title": "$impact$ Task Status is updated",
            "message": "Status is updated from #!from.task_status__code!# to #!to.task_status__code!#"
        },
        # 'compiler': {
        #     "model": None,
        #     "queryFeilds": None,
        #     "dataType": 'INT',
        #     "title": "$impact$ Task Compiler is updated",
        #     "message": "Compiler is updated from #!from.compiler!# to #!to.compiler!#"
        # },
        'version': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'STRING',
            "title": "$impact$ Task Version is updated",
            "message": "Version is updated from #!from.version!# to #!to.version!#"
        },
    },
    'DELETE': {
        'artist': {
            "model": Employee,
            "queryFeilds": ['artist__id', 'artist__fullName'],
            "dataType": 'STRING',
            "title": "$impact$ Task Deleted",
            "message": "'#!from.artist__fullName!#' Task deleted"
        },
    },
}


class DayLogsHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    target = models.ForeignKey(DayLogs, on_delete=models.DO_NOTHING, null=True, blank=True)
    parent_target = models.ForeignKey(Shots, on_delete=models.DO_NOTHING, null=True, blank=True)
    impact = models.CharField(max_length=100, default="")
    dataField = models.CharField(max_length=100)
    fromData = models.TextField(null=True, blank=True)
    toData = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=1024, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    requestType = models.CharField(max_length=300, null=True, choices=Types)
    who = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if len(self.impact) == 0 and self.target is not None:
            self.impact = self.target.shot.name
            super(DayLogsHistory, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "DayLogs History"


historyMaping['DayLogsHistory'] = {
    'POST': {
        'shot ': {
            "model": Shots,
            "queryFeilds": ['shot__id', 'shot__name'],
            "dataType": 'STRING',
            "title": "DayLogs Created",
            "message": "'#!to.shot__name!#' DayLogs Created"
        },
    },
    'PUT': {
        'shot ': {
            "model": Shots,
            "queryFeilds": ['shot__id', 'shot__name'],
            "dataType": 'STRING',
            "title": "Shot Updated",
            "message": "'#!to.shot__name!#' Shot Updated"
        },
        ' shot_biddays ': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'FLOAT',
            "title": "#impact# Shot Bid Days is updated",
            "message": "Bid Days is updated from #!from.shot_biddays!# to #!to.shot_biddays!#"
        },
        # 'updated_shot_biddays': {
        #     "model": None,
        #     "queryFeilds": None,
        #     "dataType":'FLOAT',
        #     "title": "DayLogs Updated Shot Bid Days is updated",
        #     "message": "DayLogs Updated Shot Bid Days is updated from #!from.updated_shot_biddays!# to #!to.updated_shot_biddays!#"
        #     },
        'percentage': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'FLOAT',
            "title": "Shot Percentage is updated",
            "message": "Percentage is updated from #!from.percentage!# to #!to.percentage!#"
        },
        'day_percentage': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'FLOAT',
            "title": "Shot Day Percentage is updated",
            "message": "Day Percentage is updated from #!from.day_percentage!# to #!to.day_percentage!#"
        },
        'consumed_man_day': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'FLOAT',
            "title": "Shot Consumed Man Day is updated",
            "message": "Consumed Man Day is updated from #!from.consumed_man_day!# to #!to.consumed_man_day!#"
        },
        'artist': {
            "model": Employee,
            "queryFeilds": ['artist__id', 'artist__fullName'],
            "dataType": 'STRING',
            "title": "Shot Captain is Changed",
            "message": "Shot Captain is Changed from #!from.artist__fullName!# to #!to.artist__fullName!#"
        },
        # 'updated_by': {
        #     "model": Employee,
        #     "queryFeilds": ['updated_by__id', 'updated_by__fullName'],
        #     "dataType": 'STRING',
        #     "title": "Shot Updated By is updated",
        #     "message": "Updated By is updated from #!from.updated_by__fullName!# to #!to.updated_by__fullName!#"
        # },
        # 'updated_date ': {
        #     "model": None,
        #     "queryFeilds": None,
        #     "dataType": 'DATETIME',
        #     "title": "Updated Date is updated",
        #     "message": "Updated Date is updated from #!from.updated_date!# to #!to.updated_date!#"
        # },
        # 'last_updated_date': {
        #     "model": None,
        #     "queryFeilds": None,
        #     "dataType": 'DATETIME',
        #     "title": "Last Updated Date is updated",
        #     "message": "Last Updated Date is updated from #!from.last_updated_date!# to #!to.last_updated_date!#"
        # },
    },
    'DELETE': {
        'shot': {
            "model": Shots,
            "queryFeilds": ['shot__id', 'shot__name'],
            "dataType": 'STRING',
            "title": "DayLogs Deleted",
            "message": "'#!from.shot__name!#' DayLogs deleted"
        },
    },
}


class TaskDayLogsHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    target = models.ForeignKey(TaskDayLogs, on_delete=models.DO_NOTHING, null=True, blank=True)
    parent_target = models.ForeignKey(MyTask, on_delete=models.DO_NOTHING, null=True, blank=True)
    impact = models.CharField(max_length=100, default="")
    dataField = models.CharField(max_length=100)
    fromData = models.TextField(null=True, blank=True)
    toData = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=1024, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    requestType = models.CharField(max_length=300, null=True, choices=Types)
    who = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if len(self.impact) == 0 and self.target is not None:
            self.impact = self.target.task.artist.fullName
            super(TaskDayLogsHistory, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "TaskDayLogs History"


historyMaping['TaskDayLogsHistory'] = {
    'POST': {
        'task': {
            "model": MyTask,
            "queryFeilds": ['task__id', 'task__artist__id', 'task__artist__fullName'],
            "dataType": 'STRING',
            "title": "$impact$ TaskDayLogs Created",
            "message": "#!to.task__artist__fullName!# TaskDayLogs Created"
        },
    },
    'PUT': {
        'task': {
            "model": MyTask,
            "queryFeilds": ['task__id', 'task__artist__id', 'task__artist__fullName'],
            "dataType": 'STRING',
            "title": "$impact$ Task is updated",
            "message": "Task is updated from #!from.task__artist__fullName!# to #!to.task__artist__fullName!#"
        },
        'task_biddays': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'FLOAT',
            "title": "#impact# Task Bid Days is updated",
            "message": "Bid Days is updated from #!from.task_biddays!# to #!to.task_biddays!#"
        },
        # 'updated_task_biddays': {
        #     "model": None,
        #     "queryFeilds": None,
        #     "dataType":'FLOAT',
        #     "title": "TaskDayLogs Updated Task Bid Days is updated",
        #     "message": "TaskDayLogs Updated Task Bid Days is updated from #!from.updated_task_biddays!# to #!to.updated_task_biddays!#"
        #     },
        'percentage ': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'FLOAT',
            "title": "$impact$ Task Percentage  is updated",
            "message": "Percentage is updated from #!from.percentage!# to #!to.percentage!#"
        },
        'day_percentage': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'FLOAT',
            "title": "$impact$ Task Day Percentage is updated",
            "message": "Day Percentage is updated from #!from.day_percentage!# to #!to.day_percentage!#"
        },
        'consumed_man_day': {
            "model": None,
            "queryFeilds": None,
            "dataType": 'FLOAT',
            "title": "$impact$ Task Consumed Man Day is updated",
            "message": "Consumed Man Day is updated from #!from.consumed_man_day!# to #!to.consumed_man_day!#"
        },
        'artist': {
            "model": Employee,
            "queryFeilds": ['artist__id', 'artist__fullName'],
            "dataType": 'STRING',
            "title": "$impact$ Task captain is created",
            "message": "Task captain is created #!from.artist__fullName!# to #!to.artist__fullName!#"
        },

        # 'updated_by': {
        #     "model": Employee,
        #     "queryFeilds": ['updated_by__id', 'updated_by__fullName'],
        #     "dataType": 'STRING',
        #     "title": "$impact$ Task Updated By is updated",
        #     "message": "Updated By is updated from #!from.updated_by__fullName!# to #!to.updated_by__fullName!#"
        # },
        # 'updated_date ': {
        #     "model": None,
        #     "queryFeilds": None,
        #     "dataType": 'DATETIME',
        #     "title": "$impact$ Task Updated Date is updated",
        #     "message": "Updated Date is updated from #!from.updated_date!# to #!to.updated_date!#"
        # },
        # 'last_updated_date': {
        #     "model": None,
        #     "queryFeilds": None,
        #     "dataType": 'DATETIME',
        #     "title": "$impact$ Task Last Updated Date is updated",
        #     "message": "Last Updated Date is updated from #!from.last_updated_date!# to #!to.last_updated_date!#"
        # },
    },
    'DELETE': {
        'task': {
            "model": MyTask,
            "queryFeilds": ['task__id', 'task__artist__id', 'task__artist__fullName'],
            "dataType": 'STRING',
            "title": "$impact$ TaskDayLogs Deleted",
            "message": "#!from.task__artist__fullName!# TaskDayLogs Deleted"
        },
    },
}
