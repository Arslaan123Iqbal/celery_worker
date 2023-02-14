from django.shortcuts import render,HttpResponse
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import ScrapeTask
from celery.result import AsyncResult
from .tasks import test_func,scrape_page,scrape_amazon,scrape_daraz
from.serializers import ScraperSerializer
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
@api_view(['GET'])
def test2(request, search):
    data = ScrapeTask.objects.filter(search__contains=search)
    serializer = ScraperSerializer(data=data, many=True)
    serializer.is_valid()
    task_id = [item['task_id'] for item in serializer.data]
    searchIndex = ([item['search'] for item in serializer.data])
    if len(searchIndex) == 0:
        resultdata = scrape_amazon.apply_async(args=[search])
        serializer  = ScraperSerializer(data= {"task_id":resultdata.id,"search":search})
        serializer.is_valid()
        serializer.save()
        return Response({"state":"INITIATED"})
    if searchIndex[0] == search:
        result = AsyncResult(task_id[0])
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
        return Response(response)
    # task_ids = [d['task_id'] for d in ordered_dict_list]
    # searches = [d['search'] for d in ordered_dict_list]
    # result1 = None
    # if search not in searches:
    #     # task1 = scrape_daraz.s(search)
    #     # task2 = scrape_amazon.s(search) 
    #     # result = group(task1,task2).apply_async()
    #     result1 = scrape_daraz.apply_async(args=[search])
        
    #     # task_ids = [task.id for task in result]
    #     # result.join()
    #     result = AsyncResult(result1.id)    
    #     if result.state == 'PENDING':
    #         response = {
    #             'state': result.state,
    #             'status': 'Pending...'
    #         }
    #     elif result.state == 'PROGRESS':
    #         response = {
    #             'state': result.state,
    #             'status': 'In progress...'
    #         }
    #     elif result.state == 'SUCCESS':
    #         response = {
    #             'state': result.state,
    #             'status': 'Success!',
    #             'data': result.get()
    #         }
    #     else:
    #         response = {
    #             'state': result.state,
    #             'status': 'An error occurred.'
    #         }
    #     return JsonResponse(response, safe=False)
            

    # if search in searches:
    #     index = searches.index(search)
    #     return Response({'task_id_of':result1.id})
    

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
@api_view(['GET'])
def getData(request):
    data = ScrapeTask.objects.all()
    serializers = ScraperSerializer(data=data, many=True)
    serializers.is_valid()
    return Response({
        "data":serializers.data
    })


