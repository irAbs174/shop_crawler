from django.db import models

class JobsModel(models.Model):
    jobName = models.CharField(max_length=50, verbose_name='نام کار', null=True, blank=True)
    jobArg = models.CharField(max_length=50, verbose_name='آرگومان کار', null=True, blank=True)
    jobStatus = models.CharField(max_length=40, verbose_name='وضعیت کار', null=True, blank=True)
    lastjob = models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین کار', blank=True, null=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'کار'
        verbose_name_plural = 'کار ها'

    
    def __str__(self):
        return f'{self.jobName}'