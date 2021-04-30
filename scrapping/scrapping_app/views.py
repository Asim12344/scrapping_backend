from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
import sys, os
from django.conf import settings
import json
import requests
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options  

class GetAuctions(APIView):
    # permission_classes = (permissions.AllowAny, )
    def get(self, request, format=None):
        data = self.request.query_params
        try:
            company_name = data['companyName'] 
            print("=========GetAuctions Foundation=========")
            print(company_name)
            # driver_path = os.path.join(settings.STATIC_ROOT, "chromedriver.exe")
            # print(driver_path)
            
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
            options = webdriver.ChromeOptions()
            options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')

            options.headless = True
            options.add_argument(f'user-agent={user_agent}')
            options.add_argument("--window-size=1920,1080")
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--allow-running-insecure-content')
            options.add_argument("--disable-extensions")
            options.add_argument("--proxy-server='direct://'")
            options.add_argument("--proxy-bypass-list=*")
            options.add_argument("--start-maximized")
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(executable_path=str(os.environ.get('CHROMEDRIVER_PATH')), options=options)
            # driver = webdriver.Chrome(executable_path=driver_path)
            print("===============")
            driver.implicitly_wait(60)
            driver.get('https://foundation.app/artworks')
            print("============")
            # time.sleep(30)
            print("==============")
            containers = driver.find_elements_by_xpath('//div[@class="css-1fjs75c"]/div')
            # print(containers)
            print(len(containers))
            auctions = []
            i = 0
            for container in containers:
                
                print(i)
                # time.sleep(3)
                i = i + 1
                obj = {}
                link = container.find_element_by_xpath('.//a[@class="css-5d4gsw"]').get_attribute('href')
                image_or_video = container.find_element_by_xpath('.//div[@class="css-zgakko"]/*').get_attribute('src')
                title = container.find_element_by_xpath('.//div[@class="css-wh23de"]').text
                name = container.find_element_by_xpath('.//div[@class="css-1rqrie9"]').text
                eth = container.find_element_by_xpath('.//div[@class="css-1nivzx7"]').text
                count = container.find_elements_by_xpath('.//div[@class="css-vurnku"]')
                remaining_time = ''
                video = ""
                if image_or_video:
                    temp = image_or_video.split('.')
                    print("temp")
                    print(temp)
                    video = "image"
                    if 'mp4' in temp:
                        video = "video"
                

                if len(count) == 3:
                    remaining_time = str(count[2].text)

                if len(count) == 5:
                    remaining_time = str(count[2].text) + " " + str(count[4].text)
    
                if len(count) == 7:
                    remaining_time = str(count[2].text) + " " + str(count[4].text) + " " +  str(count[6].text)
                
                obj['link'] = link
                obj['image_or_video'] = image_or_video
                obj['title'] = title
                obj['name'] = name
                obj['eth'] = eth
                obj['remaining_time'] = remaining_time
                obj['video'] = video

                auctions.append(obj)
                if i == 30:
                    break

            print(len(auctions))
            print(auctions)

            driver.quit()
            return Response({'auctions': auctions})
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno , e)
            return Response({'error': e})


class GetAuctionsSuperrare(APIView):
    # permission_classes = (permissions.AllowAny, )
    def get(self, request, format=None):
        data = self.request.query_params
        try:
            company_name = data['companyName'] 
            print("========GetAuctionsSuperrare==========")
            print(company_name)
            # driver_path = os.path.join(settings.STATIC_ROOT, "chromedriver.exe")
            # print(driver_path)
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
            options = webdriver.ChromeOptions()
            options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
            options.headless = True
            options.add_argument(f'user-agent={user_agent}')
            options.add_argument("--window-size=1920,1080")
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--allow-running-insecure-content')
            options.add_argument("--disable-extensions")
            options.add_argument("--proxy-server='direct://'")
            options.add_argument("--proxy-bypass-list=*")
            options.add_argument("--start-maximized")
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(executable_path=str(os.environ.get('CHROMEDRIVER_PATH')), options=options)
            # driver = webdriver.Chrome(executable_path=driver_path)
            print("==============")
            # driver.implicitly_wait(60)
            driver.get('http://www.superrare.co/market')
            print("============")
            time.sleep(30)
            print("==============")

            containers = driver.find_elements_by_xpath('//div[@class="row new-grid-row-margin-l-r"]/div')
            print(len(containers))
            i = 1
            auctions = []
            for container in containers:
                print(i)
                i = i + 1
                obj = {}
                link = container.find_element_by_xpath('.//a[@class="collectible-card__name"]').get_attribute('href')
                title = container.find_element_by_xpath('.//a[@class="collectible-card__name"]').text
                prices = container.find_element_by_xpath('.//div[@class="collectible-card__price-item-container"]').get_attribute("innerText")
                print("==== Title =====")
                print(title)
                price_array = prices.replace('\n\n','\n').split('\n')
                print("=========== PRICES ============")
                print(price_array)
                user_detail_array = []
                timer_detail_array = []
                try:
                    user_info = container.find_element_by_xpath('.//div[@class="collectible-card__user-container"]')
                    user_detail = user_info.get_attribute("innerText")
                    print("==== user detail =======")
                    print(user_detail)
                    user_detail_array = user_detail.split('\n')
                    print("=====array ===")
                    print(user_detail_array)

                    if len(user_detail) == 0 or len(user_detail_array) < 3:
                        timer_info = container.find_element_by_xpath('.//div[@class="AuctionCountdownContainer-ll8ha7-24 bVKXwZ"]')
                        timer_detail = timer_info.get_attribute("innerText")
                        
                        timer_detail_array = timer_detail.replace('\n\n','\n').split('\n')
                        print("==== timer_detail_array =======")
                        print(timer_detail_array)
                except:
                    print("Not Exist")
               
                image = container.find_element_by_xpath('.//section[@class="md-media md-media--1-1"]')
                image_found = False
                image_or_video = ""
                video = ""

                try:
                    image_or_video = image.find_element_by_xpath('.//img').get_attribute('src')
                    print("========= Image =========")
                    print(image_or_video)
                    image_found = True
                    video = "image"
                except:
                    print("No image")
                
                if image_found == False:
                    try:
                        print("========= Video =========")
                        image_or_video = image.find_element_by_xpath('.//video').get_attribute('src')
                        print(image_or_video)
                        video = "video"
                    except: 
                        print("No Video")

                print("\n\n")

                obj['link'] = link
                obj['image_or_video'] = image_or_video
                obj['title'] = title
                obj['prices'] = price_array
                obj['user_info'] = user_detail_array
                obj['timer_info'] = timer_detail_array
                obj['video'] = video
                auctions.append(obj)

            print(len(auctions))
            print(auctions)
            driver.quit()
            return Response({'auctions': auctions})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno , e)
            return Response({'error': e})
