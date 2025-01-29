from django.contrib import admin

from shotassignments.models import AssignmentsRoles, ShotAssignmentsOrder


# Register your models here.
@admin.register(AssignmentsRoles)
class AssignmentsRolesAdmin(admin.ModelAdmin):
    # list_display = [f.name for f in AssignmentsRoles._meta.fields]
    list_display = [ "id","name","location","department","role","shotStatus","employee","roleIndex","created_by","updated_by","creation_date","modified_date" ]
    list_per_page = 15
    list_filter = ('department','role','location','employee')
    search_fields = ['department__name', 'role__name', 'location__name','employee__fullName','employee__employee_id','shotStatus__code']
    
    def name(self, obj):
        return obj.location.name+'_'+obj.department.name+'_'+obj.role.name if obj.employee is None else obj.employee.fullName
    
    def location(self, obj):
        return obj.location.name if obj.location is not None else 'N/A'

    def department(self, obj):
        return obj.department.name if obj.department is not None else 'N/A'
    
    def role(self, obj):
        return obj.role.name if obj.role is not None else 'N/A'
    
    def shotStatus(self, obj):
        return obj.shotStatus.code if obj.shotStatus is not None else 'N/A'

    def employee(self, obj):
        return obj.employee.fullName if obj.employee is not None else 'N/A'

    def created_by(self, obj):
        return obj.created_by.fullName if obj.created_by is not None else 'N/A'
    
    def updated_by(self, obj):
        return obj.updated_by.fullName if obj.updated_by is not None else 'N/A'

@admin.register(ShotAssignmentsOrder)
class ShotAssignmentsOrderAdmin(admin.ModelAdmin):
    list_display = ["id","location","department","shotStatus","acceptCase","rejectCase","authorized","allowed","statusIndex","isBeforeArtist","isSubShot","created_by","updated_by","creation_date","modified_date"]
    list_per_page = 15
    list_filter = ('department','location', 'shotStatus')
    search_fields = ['department__name', 'location__name', 'shotStatus__code']
    filter_horizontal = ('authorizedRoles','allowedSteps')
    save_as = True

    def location(self, obj):
        return obj.location.name if obj.location is not None else 'N/A'

    def department(self, obj):
        return obj.department.name if obj.department is not None else 'N/A'
    
    def shotStatus(self, obj):
        return obj.shotStatus.code if obj.shotStatus is not None else 'N/A'
    
    def acceptCase(self, obj):
        return obj.acceptCase.code if obj.acceptCase is not None else 'N/A'
    
    def rejectCase(self, obj):
        return obj.rejectCase.code if obj.rejectCase is not None else 'N/A'

    def authorized(self, obj):
        return [authorizedRole.location.name+'_'+authorizedRole.department.name+'_'+authorizedRole.role.name if authorizedRole.employee is None else authorizedRole.employee.fullName for authorizedRole in obj.authorizedRoles.all()]
    
    def allowed(self, obj):
        return [allowedStep.location.name+'_'+allowedStep.department.name+'_'+allowedStep.role.name if allowedStep.employee is None else allowedStep.employee.fullName for allowedStep in obj.allowedSteps.all()]
    
    def created_by(self, obj):
        return obj.created_by.fullName if obj.created_by is not None else 'N/A'
    
    def updated_by(self, obj):
        return obj.updated_by.fullName if obj.updated_by is not None else 'N/A'