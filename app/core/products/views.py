from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from logs.models import LogModel
from target.models import TargetModel
from jobs.models import JobsModel
from .models import (
    SiteMap,
    Product as P,
    UsProduct,
)
from core.sec import kavenegar_api_key
from kavenegar import *

@csrf_exempt
def get_down_products_price_api(request):
    down_products = P.objects.filter(product_status='down')
    content = []
    for i in down_products:
        content.append({
            'name': i.product_name,
            'price': i.product_price,
            'stock': i.product_stock,
            'url': i.product_url,
            'parent': i.product_parent,
        })
    return JsonResponse({'status': content, 'success': True})

@csrf_exempt
def get_equals_products_price_api(request):
    equals_products = P.objects.filter(product_status='equals')
    content = []
    for i in equals_products:
        content.append({
            'name': i.product_name,
            'price': i.product_price,
            'stock': i.product_stock,
            'url': i.product_url,
            'parent': i.product_parent,
        })
    return JsonResponse({'status': content, 'success': True})

@csrf_exempt
def get_normal_products_price_api(request):
    up_products = P.objects.filter(product_status='up')
    content = []
    for i in up_products:
        content.append({
            'name': i.product_name,
            'price': i.product_price,
            'stock': i.product_stock,
            'url': i.product_url,
            'parent': i.product_parent,
        })
    return JsonResponse({'status': content, 'success': True})

@csrf_exempt
def get_products_api(request):
    products = P.objects.all()
    content = []
    for i in products:
        content.append({
            'name': i.product_name,
            'price': i.product_price,
            'stock': i.product_stock,
            'url': i.product_url,
            'parent': i.product_parent,
        })
    return JsonResponse({'status': content, 'success': True})

@csrf_exempt
def add_us_products_api(request):
    name = request.POST.get('name')
    price = request.POST.get('price')
    p.objects.create(
        us_product_name = name,
        us_product_price = price,
    )
    return JsonResponse({'status': 'افزوده شد', 'success': True})

@csrf_exempt
def get_us_products_api(request):
    us_products = UsProduct.objects.all()
    content = []
    for i in us_products:
        content.append({
            'name': i.us_product_name,
            'price': i.us_product_price
        })
    return JsonResponse({'status': content, 'success': True})

@csrf_exempt
def get_jobs_api(request):
    jobs = JobsModel.objects.all()
    content = []
    for i in jobs:
        content.append({
            'name': i.jobName,
            'price': i.jobArg
        })
    return JsonResponse({'status': content, 'success': True})

@csrf_exempt
def add_jobs_api(request):
    jobName = request.POST.get('jobName')
    jobArg = request.POST.get('jobArg')
    JobsModel.objects.create(
        jobName = jobName,
        jobArg = jobArg,
    )
    return JsonResponse({'status':  'افزوده شد', 'success': True})

@csrf_exempt
def get_logs_api(request):
    logs = LogModel.objects.all()
    content = []
    for i in logs:
        content.append({
            'name': i.logName,
            'price': i.logType
        })
    return JsonResponse({'status': content, 'success': True})

@csrf_exempt
def get_target_api(request):
    target = TargetModel.objects.all()
    content = []
    for i in target:
        content.append({
            'name': i.targetName,
            'url': i.targetUrl,
            'type': i.targetType
        })
    return JsonResponse({'status': content, 'success': True})

@csrf_exempt
def add_target_api(request):
    name = request.POST.get('name')
    url = request.POST.get('price')
    target_type = request.POST.get('taget_type')
    TargetModel.objects.create(
        targetName = name,
        targetUrl = url,
        targetType = target_type
    )
    return JsonResponse({'status': 'افزوده شد', 'success': True})

@csrf_exempt
def auth(request):
    opt = request.POST.get('otp-code')
    if opt == '1745':
        return JsonResponse({'status': '200', 'success': True})
    else:
        return JsonResponse({'status': '401', 'success': False})

@csrf_exempt
def auth_send_otp(request):
    four_digit_code = '1745'
    phone_number = request.POST.get('phone_number')
    try:
        api = KavenegarAPI(f'{kavenegar_api_key}')
        params = {
            'receptor': phone_number,
            'template': 'kikpickLogin',
            'token': four_digit_code,
            'type': 'sms',
        }   
        response = api.verify_lookup(params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)
    return JsonResponse({'status': 'کد ارسال شد', 'phone_number': phone_number, 'success': True})