from django.contrib import admin
from .models import TargetModel

@admin.register(TargetModel)
class TargetModelAdmin(admin.ModelAdmin):
    list_display = ('targetName', 'targetUrl', 'targetType', 'created_at', 'lastScan')
    search_fields = ('targetName', 'targetUrl', 'targetType')
    list_filter = ('targetType', 'created_at', 'lastScan')
    ordering = ('-created_at',)

    def lastScan_display(self, obj):
        return obj.lastScan
    lastScan_display.short_description = 'تاریخ آخرین اسکن'
