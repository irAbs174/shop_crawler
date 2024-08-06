from django.urls import path
from .views import (
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
    perform_comparison,
    register,
    single_comparison,
    newLogs,
    get_chat_id,
    get_count_data,
    get_main_target,
    get_target_products_count
)

urlpatterns = [
    path('register', register),
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
    path('perform_comparison', perform_comparison),
    path('single_comparison', single_comparison),
    path('newLogs', newLogs),
    path('get_chat_id', get_chat_id),
    path('get_count_data', get_count_data),
    path('get_main_target', get_main_target),
    path('get_target_products_count', get_target_products_count)
]