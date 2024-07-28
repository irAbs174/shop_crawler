from django.http import JsonResponse
from django.shortcuts import render
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
import random
import json

@csrf_exempt
def perform_comparison(request):
    """Compare product prices between main and US products."""
    us_dic = UsProduct.objects.all()
    main_dic = P.objects.all()
    
    comparison_results = []
    
    try:
        for main_product, us_product in zip(main_dic, us_dic):
            if main_product.product_name.find(us_product.us_product_name):
                print(f'Product : {us_product.us_product_name} found!')
                if int(us_product.us_product_price) < int(main_product.product_price):
                    LogModel.objects.create(
                        logName="down",
                        logType=f'{us_product.us_product_name}<{main_product.product_name}',
                    )
                    P.objects.filter(product_name=main_product.product_name).update(
                        product_status="down",
                    )
                    comparison_results.append({
                        'status': 'down',
                        'context': f'کالای {us_product.us_product_name} توسط بای کیف و با قیمت {main_product.product_price} زیر شده',
                        'success': True
                    })
                elif int(us_product.us_product_price) == int(main_product.product_price):
                    P.objects.filter(product_name=main_product.product_name).update(
                        product_status="equals",
                    )
                    comparison_results.append({
                        'status': 'equals',
                        'context': f'کالای {us_product.us_product_name} با کالای {main_product.product_name} برابر است در سایت {main_product.product_parent}',
                        'success': True
                    })
                else:
                    print(f'{us_product.us_product_name} normal price')
                    P.objects.filter(product_name=main_product.product_name).update(
                        product_status="up",
                    )
                    comparison_results.append({
                        'status': 'normal',
                        'success': True
                    })
            else:
                comparison_results.append({
                    'status': 'not exist!',
                    'success': False
                })
        
        if not comparison_results:
            # This handles the case where no products were compared
            return JsonResponse({'status': 'no products compared', 'success': False})
        
        return JsonResponse({'results': comparison_results, 'success': True})

    except Exception as e:
        return JsonResponse({'status': str(e), 'success': False})

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
    count = products.count()
    content = []
    for i in products:
        content.append({
            'name': i.product_name,
            'price': i.product_price,
            'stock': i.product_stock,
            'url': i.product_url,
            'parent': i.product_parent,
            'status': i.product_status,
        })
    return JsonResponse({'status': content,'count':count,'success': True})

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
    logsM = LogModel.objects.all()[:10]
    logs = []
    for i in logsM:
        content = {
            'name': i.logName,
            'logType': i.logType
        }
        logs.append(content)
    
    response_data = {'status': logs, 'success': True}
    print(json.dumps(response_data))  # Add print statement for debugging
    return JsonResponse(response_data)

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
    if request.method == 'POST':
        data = request.POST
        # Process the data as needed
        response_data = {
            'message': 'Data received successfully',
            'received_data': data
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
'''
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone = data.get('phoneNumbers', [])
            phone_list = [
                '09129585714',
                '09121578711',
            ]
            four_digit_code = random.randint(1000, 9999)
            if phone in phone_list:
                try:
                    api = KavenegarAPI(f'{kavenegar_api_key}')
                    params = {
                        'receptor': phone,
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
            else:
                pass
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
'''