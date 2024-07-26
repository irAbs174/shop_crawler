from django.urls import path
from .views import (
    auth,
    get_products_api,
    get_us_products_api,
    get_jobs_api,
    get_logs_api,
    get_target_api
)

urlpatterns = [
    path('get_products_api', get_products_api),
    path('get_us_products_api',get_us_products_api ),
    path('get_jobs_api', get_jobs_api),
    path('get_logs_api', get_logs_api),
    path('get_target_api', get_target_api),
]