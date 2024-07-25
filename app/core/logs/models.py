from django.db import models

class LogModel(models.Model):
    logName = models.CharField(max_length=50, verbose_name='نام گزارش', null=True, blank=True)
    logType = models.CharField(max_length=40, verbose_name='وضعیت گزارش', null=True, blank=True)
    lastLog = models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین گزارش', blank=True, null=True)
    scanedProducts = models.DateTimeField(auto_now=True, verbose_name='تعداد محصولات اسکن شده', blank=True, null=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'گزارش'
        verbose_name_plural = 'گزارشات'

    
    def __str__(self):
        return f'{self.logName}'