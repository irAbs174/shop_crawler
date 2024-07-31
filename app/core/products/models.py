from django.db import models

class BotUsers(models.Model):
    userId = models.CharField(max_length=50, verbose_name='شناسه کاربر',null=True, blank=True )
    username = models.CharField(max_length=50, verbose_name='نام کاربری',null=True, blank=True )
    first_name = models.CharField(max_length=50, verbose_name='نام',null=True, blank=True )
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی',null=True, blank=True )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت نام', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی', blank=True, null=True)

    objects = models.Manager()
    
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class SiteMap(models.Model):
    target = models.CharField(max_length=50, verbose_name='هدف',null=True, blank=True )
    siteMapUrl = models.CharField(max_length=50, verbose_name='آدرس',null=True, blank=True )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی', blank=True, null=True)

    objects = models.Manager()
    
    class Meta:
        verbose_name = 'سایت مپ'
        verbose_name_plural = 'سایت مپ ها'
    

class Product(models.Model):
    product_key = models.CharField(max_length=50, verbose_name='کلید',null=True, blank=True )
    product_parent = models.CharField(max_length=50, verbose_name='سایت والد',null=True, blank=True )
    product_name = models.CharField(max_length=300, verbose_name='نام',null=True, blank=True )
    product_price = models.CharField(max_length=50, verbose_name='قیمت', blank=True, null=True)
    product_url = models.CharField(max_length=50, verbose_name='آدرس محصول',null=True, blank=True )
    product_stock = models.CharField(max_length=50, verbose_name='موجودی محصول',null=True, blank=True )
    product_type = models.CharField(max_length=50, verbose_name='محصول مرجع',null=True, blank=True )
    product_status = models.CharField(max_length=50, verbose_name='وضعیت محصول',null=True, blank=True )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی', blank=True, null=True)

    objects = models.Manager()
    
    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return f'{self.product_name}'

  # Under Supervision products
class UsProduct(models.Model):
    us_product_key = models.CharField( max_length=50, verbose_name='کلید',null=True, blank=True )
    us_product_name = models.CharField( max_length=300, verbose_name='نام',null=True, blank=True )
    us_product_price = models.CharField( max_length=50, verbose_name='قیمت', blank=True, null=True)
    us_product_status = models.CharField( max_length=50, verbose_name='وضعیت محصول تحت نظر',null=True, blank=True )
    created_at = models.DateTimeField( auto_now_add=True, verbose_name='تاریخ ایجاد', blank=True, null=True )
    updated_at = models.DateTimeField( auto_now=True, verbose_name='تاریخ بروزرسانی', blank=True, null=True )

    objects = models.Manager()

    class Meta:
        verbose_name = 'محصول تحت نظر'
        verbose_name_plural = 'محصولات تحت نظر'

    def __str__(self):
        return f'{self.us_product_name}'