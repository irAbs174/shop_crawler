from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register),
    path('get_products_api', views.get_products_api),
    path('get_us_products_api',views.get_us_products_api ),
    path('get_jobs_api', views.get_jobs_api),
    path('get_logs_api', views.get_logs_api),
    path('get_target_api', views.get_target_api),
    path('get_down_products_price_api', views.get_down_products_price_api),
    path('get_equals_products_price_api', views.get_equals_products_price_api),
    path('get_normal_products_price_api', views.get_normal_products_price_api),
    path('add_us_products_api', views.add_us_products_api),
    path('add_jobs_api', views.add_jobs_api),
    path('perform_comparison', views.perform_comparison),
    path('single_comparison', views.single_comparison),
    path('newLogs', views.newLogs),
    path('get_chat_id', views.get_chat_id),
    path('get_count_data', views.get_count_data),
    path('get_main_target', views.get_main_target),
    path('get_target_products_count', views.get_target_products_count),
    path('get_products_url', views.get_products_url),
    path('perform_export', views.perform_export),
    path('store_products', views.store_products)
]