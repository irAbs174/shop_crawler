from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from logs.models import LogModel
from target.models import TargetModel
from jobs.models import JobsModel
from django.utils import timezone
from .models import (
    SiteMap,
    Product as P,
    UsProduct as us,
    BotUsers,
)
from core.sec import kavenegar_api_key
from kavenegar import *
import random
import json
import re

@csrf_exempt
def get_chat_id(request):
    ctx = []
    for i in BotUsers.objects.all():
        item = {
            'chatId': i.userId,
        }
        ctx.append(item)

    return JsonResponse({'status':ctx, 'success': True})

@csrf_exempt
def newLogs(requests):
    logs = LogModel.objects.all()
    ctx = []
    for log in logs:
        if not log.send_status:
            item = {
                'logName': log.logName,
                'logType': log.logType,
            }
            ctx.append(item)
    
    print(ctx)
    logs.update(send_status='yes')

    return JsonResponse({'status':ctx, 'success':True})


@csrf_exempt
def register(request):
    userId = request.POST.get('userId')
    username = request.POST.get('username')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    if BotUsers.objects.filter(userId=userId).exists():
        content = {'status':'کاربر از قبل موجود است', 'success': True}
    else:
        BotUsers.objects.create(
            userId = userId,
            username = username,
            first_name = first_name,
            last_name = last_name
        )
        content = {'status': 'کاربر با موفقیت ثبت شده', 'success': True}
    return JsonResponse(content)

@csrf_exempt
def single_comparison(request):
    product_name = request.POST.get('product_name')
    ctx = []
    for i in P.objects.all():
        if i.product_name:
            if product_name in i.product_name:
                item = {
                    'name': i.product_name,
                    'price': i.product_price,
                    'stock': i.product_stock,
                    'url': i.product_url,
                    'parent': i.product_parent,
                }
                ctx.append(item)
    if ctx == []:
        ctx = ['کالای مورد نظر پیدا نشد']
    return JsonResponse({'status': ctx, 'success': True})

@csrf_exempt
def perform_comparison(request):
    jobArg = request.POST.get('jobArg')
    if jobArg == 'all':
        targets = TargetModel.objects.filter(targetType='normal')
        for target in targets:
            jobArg = target.targetUrl,
            main_dic = P.objects.filter(product_type='normal')
            uss_dic = P.objects.filter(product_type = 'main')
            comparison_results = []
            try:
                for main_product in main_dic:
                    for us_dic in uss_dic:
                        pattern = r'\b[a-zA-Z]{2,}\d{2,}\b'
                        matches = re.findall(pattern, us_dic.product_name)
                        if P.objects.filter(product_type='normal' ,product_name__contains=matches):
                            print(f'Product : {us_dic.product_name} found!')
                            if int(us_dic.product_price) < int(main_product.product_price):
                                LogModel.objects.create(
                                    logName="گزارش زیر کردن قیمت:",
                                    logType=f'کالای مرجع:{us_dic.product_name} \n کالای زیر قیمت مرجع:{main_product.product_name} و با قیمت {main_product.product_price}',
                                )
                                P.objects.filter(product_name=main_product.product_name).update(
                                    product_status="down",
                                )
                                comparison_results.append({
                                    'status': 'down',
                                    'context': f'کالای {us_dic.product_name} توسط بای کیف و با قیمت {main_product.product_price} زیر شده',
                                    'success': True
                                })
                            elif int(us_dic.product_price) == int(main_product.product_price):
                                P.objects.filter(product_name=main_product.product_name).update(
                                    product_status="equals",
                                )
                                comparison_results.append({
                                    'status': 'equals',
                                    'context': f'کالای {us_dic.product_name} با کالای {main_product.product_name} برابر است در سایت {main_product.product_parent}',
                                    'success': True
                                })
                            else:
                                print(f'{us_dic.product_name} normal price')
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
                    return JsonResponse({'status': 'محصولی مقایسه نشد', 'success': False})
                
                return JsonResponse({'results': 'محصولی مقایسه نشد', 'success': True})

            except Exception as e:
                return JsonResponse({'status': 'در حال حاظر ربات در حال تکمیل اطلاعات است. لطفا کمی بعد دوباره تلاش کنید', 'success': False})
    else:
        main_dic = P.objects.filter(product_parent=jobArg)
        uss_dic = P.objects.filter(product_type = 'main')
        comparison_results = []
        
        try:
            for main_product, us_dic in zip(main_dic, uss_dic):
                print(main_product, us_dic)
                if main_product.product_name.find(us_dic.product_url.split('/')[4] ):
                    print(f'Product : {us_dic.product_name} found!')
                    if int(us_dic.product_price) < int(main_product.product_price):
                        LogModel.objects.create(
                            logName="down",
                            logType=f'{us_dic.product_name}<{main_product.product_name}',
                        )
                        P.objects.filter(product_name=main_product.product_name).update(
                            product_status="down",
                        )
                        comparison_results.append({
                            'status': 'down',
                            'context': f'کالای {us_dic.product_name} توسط بای کیف و با قیمت {main_product.product_price} زیر شده',
                            'success': True
                        })
                    elif int(us_dic.product_price) == int(main_product.product_price):
                        P.objects.filter(product_name=main_product.product_name).update(
                            product_status="equals",
                        )
                        comparison_results.append({
                            'status': 'equals',
                            'context': f'کالای {us_dic.product_name} با کالای {main_product.product_name} برابر است در سایت {main_product.product_parent}',
                            'success': True
                        })
                    else:
                        print(f'{us_dic.product_name} normal price')
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
                return JsonResponse({'status': 'محصولی مقایسه نشد', 'success': False})
            
            return JsonResponse({'results': 'محصولی مقایسه نشد', 'success': True})

        except Exception as e:
            return JsonResponse({'status': str(e), 'success': False})

@csrf_exempt
def get_down_products_price_api(request):
    down_products = P.objects.filter(product_status='down')
    content = []
    if down_products:
        for i in down_products:
            content.append({
                'name': i.product_name,
                'price': i.product_price,
                'stock': i.product_stock,
                'url': i.product_url,
                'parent': i.product_parent,
            })
    else:
        print("NOT DOWN PRODUCTS")
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
    jobArg = request.POST.get('jobArg')
    products = P.objects.filter(product_parent=jobArg)
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
    print(request.POST)
    name = request.POST.get('name')
    price = request.POST.get('price')
    print(name, price)
    us.objects.create(
        us_product_name = name,
        us_product_price = price,
    )
    return JsonResponse({'status': 'افزوده شد', 'success': True})

@csrf_exempt
def get_us_products_api(request):
    us_products = us.objects.all()
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
    logsM = LogModel.objects.all().order_by('-id')[:10]
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