from django.contrib import admin
from .models import LogModel

@admin.register(LogModel)
class LogModelAdmin(admin.ModelAdmin):
    list_display = ('logName', 'logType', 'lastLog', 'scanedProducts')
    search_fields = ('logName', 'logType')
    list_filter = ('logType', 'lastLog')
    ordering = ('-lastLog',)

    def scanedProducts_display(self, obj):
        return obj.scanedProducts
    scanedProducts_display.short_description = 'تعداد محصولات اسکن شده'
