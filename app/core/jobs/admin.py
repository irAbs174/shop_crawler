from django.contrib import admin
from .models import JobsModel

@admin.register(JobsModel)
class JobsModelAdmin(admin.ModelAdmin):
    list_display = ('jobName', 'jobArg', 'jobStatus', 'lastjob')
    search_fields = ('jobName', 'jobArg', 'jobStatus')
    list_filter = ('jobStatus', 'lastjob')
    ordering = ('-lastjob',)
