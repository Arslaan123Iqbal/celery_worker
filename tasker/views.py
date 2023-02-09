from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from celery.result import AsyncResult
from .tasks import test_func,scrape_page,scrape_amazon
from celery import group
import logging
logger = logging.getLogger(__name__)
# Create your views here.
def test(request):
    logger.info("hsajwa")
    print("dfafadf")
    test_func.delay()
    return HttpResponse("Done, 12wet")

# def sendingmail(request):
#     send_mail_func.delay()
#     return HttpResponse("Sent")

def scrape_view(request):
    url = 'https://www.amazon.com/s?i=specialty-aps&bbn=16225009011&rh=n%3A%2116225009011%2Cn%3A281407&ref=nav_em__nav_desktop_sa_intl_accessories_and_supplies_0_2_5_2'
    result = scrape_page.delay(url)
    data = result.get()
    return JsonResponse({'data': data})

def test2(request, pk):
    result = scrape_amazon.apply_async(args=[pk])
    task_id = result.task_id
    return JsonResponse({'task_id': task_id})

def task_status(request, task_id):
    result = AsyncResult(task_id)
    if result.state == 'PENDING':
        response = {
            'state': result.state,
            'status': 'Pending...'
        }
    elif result.state == 'PROGRESS':
        response = {
            'state': result.state,
            'status': 'In progress...'
        }
    elif result.state == 'SUCCESS':
        response = {
            'state': result.state,
            'status': 'Success!',
            'data': result.get()
        }
    else:
        response = {
            'state': result.state,
            'status': 'An error occurred.'
        }
    return JsonResponse(response, safe=False)