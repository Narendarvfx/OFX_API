from django.contrib import admin
from profiles.models import Profile

# Register your models here.
class ProfileFields(admin.ModelAdmin):
    list_display = [f.name for f in Profile._meta.fields]
    exclude = ("user",)


admin.site.register(Profile, ProfileFields)
