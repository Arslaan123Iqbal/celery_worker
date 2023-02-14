from celery import shared_task
from selenium.webdriver.chrome.options import Options
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from selenium import webdriver
from selenium.webdriver.common.by import By
from celerytask import settings
import datetime
import logging
import os
import csv
logger = logging.getLogger(__name__)

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

@shared_task(bind=True)
def test_func(self):
    #operations
    for i in range(10):
        print(i)
    return "Done"

# @shared_task(bind=True)
# def send_mail_func(self):
#     users = get_user_model().objects.all()
#     #timezone.localtime(users.date_time) + timedelta(days=2)
#     for user in users:
#         mail_subject = "Hi! Celery Testing"
#         message = "It worked"
#         to_email = user.email
#         logger.info(to_email)
#         send_mail(
#             subject = mail_subject,
#             message=message,
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[to_email],
#             fail_silently=True,
#         )
#     return "Done"

@shared_task
def scrape_page(url):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    product_titles = driver.find_element('span.a-size-medium.a-color-base.a-text-normal')
    product_prices = driver.find_elements('span.a-offscreen')
    products = []
    for title, price in zip(product_titles, product_prices):
        products.append({
            'title': title.text,
            'price': price.text
        })
    driver.quit()
    return products

def scraper(URL, title, price):
    products = []
    driver.get(URL)
    product_titles = driver.find_elements(By.CLASS_NAME, 'a-size-medium.a-color-base.a-text-normal')
    product_prices = driver.find_elements(By.CLASS_NAME, 'a-price-whole')
    for title, price in  zip(product_titles, product_prices):
       dictPro  = {
      "title":title.text,
       "price": price.text
       }
       products.append(dictPro)

    return products
@shared_task
def scrape_amazon(search):
    products = []
    driver.get(f"https://www.amazon.com/s?k={search}&crid=3PQNRF6AM6CIA&sprefix=mobil%2Caps%2C425&ref=nb_sb_noss_2")
    product_titles = driver.find_elements(By.CLASS_NAME, 'a-size-medium.a-color-base.a-text-normal')
    product_prices = driver.find_elements(By.CLASS_NAME, 'a-price-whole')
    for title, price in  zip(product_titles, product_prices):
       dictPro  = {
      "title":title.text,
       "price": price.text
       }
       products.append(dictPro)
    # fileDate = datetime.datetime.now()
    # filename = f"{fileDate}.csv"

    # # get current working directory
    # current_directory = os.getcwd()

    # # full path to csv file
    # filepath = os.path.join(current_directory, filename)

    # # writing to csv file
    # with open(filepath, 'w', newline='') as csvfile:
    #     # creating a csv writer object
    #     fieldnames = ['title', 'price']
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
    #     # writing the header row
    #     writer.writeheader()
        
    #     # writing the rows
    #     for row in products:
    #         writer.writerow(row)
    return products

@shared_task
def scrape_daraz(search):
    print("Here")
    
    products = []
    driver.get(f"https://www.alibaba.com/trade/search?tab=all&searchText={search}")
    product_titles = driver.find_elements(By.CLASS_NAME, 'elements-title-normal__content.large')
    product_prices = driver.find_elements(By.CLASS_NAME, 'elements-offer-price-normal__price')
    

    for title, price in  zip(product_titles, product_prices):
       dictPro  = {
      "title":title.text,
       "price": price.text
       }
       products.append(dictPro)

    # fileDate = datetime.datetime.now()
    # filename = f"{fileDate}.csv"

    # get current working directory
    # current_directory = os.getcwd()

    # full path to csv file
    # filepath = os.path.join(current_directory, filename)

    # # writing to csv file
    # with open(filepath, 'w', newline='') as csvfile:
    #     # creating a csv writer object
    #     fieldnames = ['title', 'price']
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
    #     # writing the header row
    #     writer.writeheader()
        
    #     # writing the rows
    #     for row in products:
    #         writer.writerow(row)
    
    return products
