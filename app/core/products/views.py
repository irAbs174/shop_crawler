from djangp.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_products_api(request):
    return JsonResponse({'status': '200-OK', 'success': True})

@csrf_exempt
def get_us_products_api(request):
    return JsonResponse({'status': '200-OK', 'success': True})

@csrf_exempt
def get_jobs_api(request):
    return JsonResponse({'status': '200-OK', 'success': True})

@csrf_exempt
def get_logs_api(request):
    return JsonResponse({'status': '200-OK', 'success': True})

@csrf_exempt
def get_target_api(request):
    return JsonResponse({'status': '200-OK', 'success': True})

@csrf_exempt
def auth(request):
    return JsonResponse({'status': '200-OK', 'success': True})



