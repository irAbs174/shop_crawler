from django.urls import path
from .views import (
    auth,
    auth_send_otp,
    get_products_api,
    get_us_products_api,
    get_jobs_api,
    get_logs_api,
    get_target_api,
    get_down_products_price_api,
    get_equals_products_price_api,
    get_normal_products_price_api,
    add_us_products_api,
    add_jobs_api,
)

urlpatterns = [
    path('auth', auth),
    path('auth_send_otp', auth_send_otp),
    path('get_products_api', get_products_api),
    path('get_us_products_api',get_us_products_api ),
    path('get_jobs_api', get_jobs_api),
    path('get_logs_api', get_logs_api),
    path('get_target_api', get_target_api),
    path('get_down_products_price_api', get_down_products_price_api),
    path('get_equals_products_price_api', get_equals_products_price_api),
    path('get_normal_products_price_api', get_normal_products_price_api),
    path('add_us_products_api', add_us_products_api),
    path('add_jobs_api', add_jobs_api),
]