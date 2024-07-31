from django.db import models

class TargetModel(models.Model):
    targetName = models.CharField(max_length=50, verbose_name='نام هدف', null=True, blank=True)
    targetUrl = models.CharField(max_length=40, verbose_name='آدرس هدف', null=True, blank=True)
    target_sitemap = models.CharField(max_length=40, verbose_name='سایت مپ هدف', null=True, blank=True)
    targetType = models.CharField(max_length=40, verbose_name='نوع هدف', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد', blank=True, null=True)
    lastScan = models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین اسکن', blank=True, null=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'هدف'
        verbose_name_plural = 'اهداف'

    
    def __str__(self):
        return f'{self.targetName}'