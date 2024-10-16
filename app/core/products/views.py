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
from khayyam import JalaliDatetime
from django.db.models import Q
from colorama import Fore
from kavenegar import *
import random
import json
import re

@csrf_exempt
def store_products(request):
    try:
        # Get the parameters from the POST request
        jobArg = request.POST.get('jobArg')
        url = request.POST.get('url')
        info = json.loads(request.POST.get('payload'))  # Parse the payload as JSON
        
        # Access the fields from the parsed JSON
        name = info.get('name')
        price = info.get('price')
        status = info.get('status', {}).get('quantity')

        # Update the product in the database
        pro = P.objects.filter(
            product_parent=jobArg,
            product_url=url,
        ).update(
            product_name=name,
            product_price=price,
            product_stock=status,
        )

        # Set success message
        status_code = 200
        message = f'Product {name} stored to database successfully'
        success = True

    except Exception as error:
        # Handle errors
        status_code = 403
        message = str(error)
        success = False

    return JsonResponse({
        'status': status_code,
        'message': message,
        'success': success
    })

@csrf_exempt
def perform_export(request):
    fields = ['فروشگاه', 'نام محصول', 'قیمت', 'موجودی', 'آدرس محصول']
    jobArg = request.POST.get('jobArg')  # Get job argument from POST request
    products = P.objects.all()  # Query all products
    rows = []  # Initialize an empty list to store product data rows
    
    for product in products:
        stock = product.product_stock  # Access product stock
        if stock:
            try:
                # Safely load JSON from the stock string, handling single quotes
                stock_json = json.loads(stock.replace("'", '"').replace('\n', ''))
                
                # Iterate over each variant in the stock data
                for variant in stock_json:
                    rows.append({
                        'parent': product.product_parent,  # Add product parent
                        'name': f"{product.product_name} - {variant.get('color', 'N/A')}",  # Add product name and color
                        'price': product.product_price,  # Add product price
                        'quantity': variant.get('quantity', 'N/A'),  # Add product quantity
                        'url': product.product_url  # Add product URL
                    })
            except Exception as error:
                # Capture the error and append a detailed message for debugging
                rows.append({'Error': str(error)})
    
    # Return a JSON response with the rows and success status
    return JsonResponse({'status': rows, 'success': True})
            
@csrf_exempt
def get_target_products_count(request):
    targetUrl = request.POST.get('url')
    all_target_products_count = P.objects.filter(product_parent=targetUrl).count()
    stock_count = P.objects.filter(product_parent=targetUrl).count()
    out_stock_count = P.objects.filter(product_parent=targetUrl, product_stock='ناموجود').count()
    return JsonResponse({
        'status': 200,
        'all_target_products_count':all_target_products_count,
        'stock_count':stock_count,
        'out_stock_count':out_stock_count,
        'success': True
    })

@csrf_exempt
def get_main_target(request):
    main_target = TargetModel.objects.filter(targetType='main')[0].targetName
    return JsonResponse({
        'status': main_target,
        'success': main_target,
    })

@csrf_exempt
def get_count_data(request):

    all_target_count = TargetModel.objects.all().count()
    main_target = TargetModel.objects.filter(targetType='main')[0].targetName
    all_products_count = P.objects.all().count()
    down_products_count = LogModel.objects.filter(logName="گزارش زیر کردن قیمت:").count()
    up_products_count = LogModel.objects.filter(logName="گزارش قیمت بالاتر:").count()
    equals_products_count = LogModel.objects.filter(logName="گزارش هم قیمت:").count()
    context = {
        'all_target_count':all_target_count,
        'main_target':main_target,
        'all_products_count': all_products_count,
        'down_products_count': down_products_count,
        'up_products_count':up_products_count,
        'equals_products_count':equals_products_count,
    }

    return JsonResponse({'status':context, 'success':True})

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
    logs = LogModel.objects.filter(logName="گزارش زیر کردن قیمت:", send_status=None)
    ctx = []
    for log in logs:
        if not log.send_status:
            item = {
                'logName': log.logName,
                'logType': log.logType,
                'lastLog': JalaliDatetime(log.lastLog).strftime('%Y-%m-%d %H:%M:%S'),
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
    # first clear log comparison logs
    print('clear old comparison')
    LogModel.objects.filter(logName="گزارش هم قیمت:").delete()
    LogModel.objects.filter(logName="گزارش قیمت بالاتر:").delete()
    LogModel.objects.filter(logName="گزارش زیر کردن قیمت:").delete()

    # now comparison :
    print("Starting perform_comparison")
    main_dic = P.objects.filter(product_type='normal')
    uss_dic = P.objects.filter(product_type='main')
    
    print(f"Main products count: {main_dic.count()}")
    print(f"USS products count: {uss_dic.count()}")
    
    try:
        for us_dic in uss_dic:
            print(f"USS product: {us_dic.product_name} - {us_dic.product_price}")
            
            if us_dic.product_name:
                pattern = r'\b[a-zA-Z]{2,}\d{2,}\b'
                matches = re.findall(pattern, us_dic.product_name)
                print(f"Matches: {matches}")
                
                if matches:
                    if P.objects.filter(product_type='normal', product_name__contains=matches[0]).exists():
                        main_product = P.objects.filter(product_type='normal', product_name__contains=matches[0])[0]
                        print(f'Product : {us_dic.product_name} found!')
                        
                        us_dic_price = int(us_dic.product_price)
                        main_product_price = int(main_product.product_price)
                        
                        if us_dic_price < main_product_price:
                            LogModel.objects.create(
                                        logName="گزارش قیمت بالاتر:",
                                        logType=f'محصول مرجع :{us_dic.product_name}\nقیمت مرجع:{us_dic.product_price}\n {main_product.product_name}:{main_product.product_price}',
                                    )
                            P.objects.filter(product_type="main", product_name=us_dic.product_name).update(
                                        product_status="up",
                                    )
                        elif us_dic_price == main_product_price:
                            LogModel.objects.create(
                                        logName="گزارش هم قیمت:",
                                        logType=f'محصول مرجع :{us_dic.product_name}\nقیمت مرجع:{us_dic.product_price}\n {main_product.product_name}:{main_product.product_price}',
                                    )
                            P.objects.filter(product_type="main", product_name=us_dic.product_name).update(
                                product_status="equals",
                            )
                        else:
                            if main_product_price != 0:
                                LogModel.objects.create(
                                            logName="گزارش زیر کردن قیمت:",
                                            logType=f'محصول مرجع :{us_dic.product_name}\nقیمت مرجع:{us_dic.product_price}\n {main_product.product_name}:{main_product.product_price}',                                        )
                                P.objects.filter(product_type="main", product_name=us_dic.product_name).update(
                                            product_status="down",
                                )
    except Exception as e:
        return JsonResponse({'status': 'در حال حاظر ربات در حال تکمیل اطلاعات است. لطفا کمی بعد دوباره تلاش کنید', 'success': False})

    return JsonResponse({'status': 'مقایسه انجام شد', 'success': True})

@csrf_exempt
def get_down_products_price_api(request):
    down_products = LogModel.objects.filter(logName="گزارش زیر کردن قیمت:")
    content = []
    if down_products:
        for i in down_products:
            content.append({
                'logName': i.logName,
                'logType': i.logType,
                'lastLog': JalaliDatetime(i.lastLog).strftime('%Y-%m-%d %H:%M:%S'),
            })
    else:
        print("NOT DOWN PRODUCTS")
    return JsonResponse({'status': content, 'success': True})

@csrf_exempt
def get_equals_products_price_api(request):
    equals_products = LogModel.objects.filter(logName="گزارش هم قیمت:")
    content = []
    for i in equals_products:
        content.append({
            'logName': i.logName,
            'logType': i.logType,
            'lastLog': JalaliDatetime(i.lastLog).strftime('%Y-%m-%d %H:%M:%S'),
        })
    return JsonResponse({'status': content, 'success': True})

@csrf_exempt
def get_normal_products_price_api(request):
    up_products = LogModel.objects.filter(logName="گزارش قیمت بالاتر:")
    content = []
    for i in up_products:
        content.append({
            'logName': i.logName,
            'logType': i.logType,
            'lastLog': JalaliDatetime(i.lastLog).strftime('%Y-%m-%d %H:%M:%S'),
        })
    return JsonResponse({'status': content, 'success': True})

@csrf_exempt
def get_products_url(request):
    # jobArg must be set and like : example.com and HTTP/HTTPS NOT REQUIRED
    jobArg = request.POST.get("jobArg")
    content = []
    if jobArg:
        # Return list of last updated products_link for specific product_parent
        # save for updated_at field must be update !
        product = P.objects.filter(product_parent=jobArg).order_by("updated_at")[0]
        product.save()
        # send response to client
        status = 200
        success = True
        content.append({
            'product_name': product.product_name,
            'product_url': product.product_url,
        })
    else:
        status = 403
        success = False

    return JsonResponse({
        'status' : status,
        'content': content,
        'success': success
    })

@csrf_exempt
def get_products_api(request):
    jobArg = request.POST.get('jobArg')
    if jobArg == "All" :
        products = P.objects.all()
    else:
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
            'logType': i.logType,
            'lastLog': JalaliDatetime(i.lastLog).strftime('%Y-%m-%d %H:%M:%S'),
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
                return JsonResponse({'status': ''کد ارسال شد',', 'phone_number': phone_number, 'success': True})
            else:
                pass
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
'''