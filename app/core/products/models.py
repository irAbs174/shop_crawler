from django.db import models

class Product(models.Model):
    product_key = models.CharField(max_length=50, verbose_name='کلید',null=True, blank=True )
    product_parent = models.CharField(max_length=50, verbose_name='سایت والد',null=True, blank=True )
    product_name = models.CharField(max_length=300, verbose_name='نام',null=True, blank=True )
    product_price = models.CharField(max_length=50, verbose_name='قیمت', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی', blank=True, null=True)

    objects = models.Manager()
    
    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return self.product_name