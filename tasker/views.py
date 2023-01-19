from django.shortcuts import render,HttpResponse
from .tasks import test_func,send_mail_func
import logging
logger = logging.getLogger(__name__)
# Create your views here.
def test(request):
    logger.info("hsajwa")
    print("dfafadf")
    test_func.delay()
    return HttpResponse("Done, 12wet")

def sendingmail(request):
    send_mail_func.delay()
    return HttpResponse("Sent")