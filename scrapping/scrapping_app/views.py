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
from selenium.common.exceptions import TimeoutException

class GetAuctions(APIView):
    # permission_classes = (permissions.AllowAny, )
    def get(self, request, format=None):
        data = self.request.query_params
        try:
            company_name = data['companyName'] 
            print("=========GetAuctions Foundation=========")
            print(company_name)
            driver_path = os.path.join(settings.STATIC_ROOT, "chromedriver.exe")
            print(driver_path)
            
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
            options = webdriver.ChromeOptions()
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
            driver = webdriver.Chrome(executable_path=driver_path, options=options)
            # driver = webdriver.Chrome(executable_path=driver_path)
            t = time.time()
            driver.set_page_load_timeout(60)
            try:
                print("=======try=======")
                driver.get('https://foundation.app/artworks')
                print("===end====")
            except TimeoutException:
                print("except")
                # driver.execute_script("window.stop();")
            print('Time App foundation consuming:', time.time() - t)
            print("===============")
            # driver.implicitly_wait(30)
            # driver.get('https://foundation.app/artworks')
            print("============")
            time.sleep(40)
            print("==============")
            containers = driver.find_elements_by_xpath('//div[@class="css-1fjs75c"]/div')
            # print(containers)
            print(len(containers))
            auctions = []
            i = 0
            for container in containers:
                print(i)
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
                if i == 9:
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
            driver_path = os.path.join(settings.STATIC_ROOT, "chromedriver.exe")
            print(driver_path)
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
            options = webdriver.ChromeOptions()
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
            driver = webdriver.Chrome(executable_path=driver_path, options=options)
            t = time.time()
            driver.set_page_load_timeout(140)
            try:
                print("=======try=======")
                driver.get('http://www.superrare.co/market')
                print("===end====")
            except TimeoutException:
                print("except")
                # driver.execute_script("window.stop();")
            print('Time GetAuctionsSuperrare consuming:', time.time() - t)

            height = 0
            while True:
                print("scroll super")
                new_height = driver.execute_script("return document.body.scrollHeight")
                
                if height==new_height:
                    break
                driver.find_element_by_tag_name('body').send_keys(Keys.END)
                time.sleep(20)
                height=new_height


            containers = driver.find_elements_by_xpath('//div[@class="row new-grid-row-margin-l-r"]/div')
            print(len(containers))
            i = 1
            auctions = []
            for container in containers:
                print(i)
                
                obj = {}
                link = container.find_element_by_xpath('.//a[@class="collectible-card__name"]').get_attribute('href')
                title = container.find_element_by_xpath('.//a[@class="collectible-card__name"]').text
                prices = container.find_element_by_xpath('.//div[@class="collectible-card__price-item-container"]').get_attribute("innerText")
                print("==== Title =====")
                print(title)
                print("==== prices =====")
                print(prices)
                price_array = prices.replace('\n\n','\n').split('\n')
                print("=========== PRICES ============")
                print(price_array)
                user_detail_array = []
                timer_detail_array = []
                remaining_time1 = ""
                try:
                    user_info = container.find_element_by_xpath('.//div[@class="collectible-card__user-container"]')
                    user_detail = user_info.get_attribute("innerText")
                    print("==== user detail =======")
                    print(user_detail)
                    print(len(user_detail))
                    user_detail_array = user_detail.split('\n')
                    print("=====array ===")
                    print(user_detail_array)

                    if len(user_detail) == 0 or len(user_detail_array) < 3:
                        print("iffffffffff")
                        timer_info = container.find_element_by_xpath('.//div[@id="container"]')
                        timer_detail = timer_info.get_attribute("innerText")
                        
                        timer_detail_array = timer_detail.replace('\n\n','\n').split('\n')
                        print("==== timer_detail_array =======")
                        print(timer_detail_array)
                        remaining_time1 =  timer_detail_array[1] + "d " +  timer_detail_array[3] + "h " +  timer_detail_array[5] +  "m " + timer_detail_array[7] + "s"

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
                obj['remaining_time'] = remaining_time1
                auctions.append(obj)
                # if i == 9:
                #     break
                i = i + 1

            print(len(auctions))
            print(auctions)
            # driver.quit()
            return Response({'auctions': auctions})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno , e)
            return Response({'error': e})


class GetAuctionsRarible(APIView):
    # permission_classes = (permissions.AllowAny, )
    def get(self, request, format=None):
        data = self.request.query_params
        try:
            company_name = data['companyName'] 
            print("=========GetAuctionsRarible=========")
            print(company_name)
            driver_path = os.path.join(settings.STATIC_ROOT, "chromedriver.exe")
            print(driver_path)
            
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
            options = webdriver.ChromeOptions()

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
            driver = webdriver.Chrome(executable_path=driver_path, options=options)
            # driver = webdriver.Chrome(executable_path=driver_path)
            t = time.time()
            driver.set_page_load_timeout(60)
            try:
                print("=======try=======")
                driver.get('https://rarible.com/')
                print("===end====")
            except TimeoutException:
                print("except")
            print('Time GetAuctionsRarible consuming:', time.time() - t)

            print("===============")
            print("============")
            time.sleep(15)
            print("==============")
            count = 1
            while True:
                print("true")
                print(count)
                count = count + 1
                try:
                    #  button = driver.find_element_by_xpath('//div[@class="sc-iCoHVE sc-fujyUd sc-bkbjAj sc-dIvqjp knnrxv gJJgrO jjJFtn faljwD sc-dSnYFs bmCrBR slick-arrow slick-next"]')
                    #  print(driver.title)
                    time.sleep(4)
                    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@class='sc-iCoHVE sc-fujyUd sc-bkbjAj sc-dIvqjp knnrxv gJJgrO jjJFtn faljwD sc-dSnYFs bmCrBR slick-arrow slick-next']")))
                    button.click()
                    print("==============================")
                    
                    if count == 10:
                        break
                    
                    #  break
                except Exception as ex:
                    print("except")
                    if 'intercepted' in str(ex):
                        print(str(ex))
                        pass
                    else:
                        break
            element = driver.find_element_by_xpath('//div[@class="slick-track"]')
            print(element)
            i = 1
            containers = element.find_elements_by_xpath('.//div[@class="slick-slide slick-active slick-current"] | .//div[@class="slick-slide slick-active"] | .//div[@class="slick-slide"]')
            print(len(containers))
            auctions = []
            for container in containers:
                obj = {}
                print(i)
                
                user_detail = container.get_attribute("innerText")
                print("==========")
                user_detail = user_detail.split("\n")
                print(user_detail)
                title = user_detail[1]
                name = user_detail[2]
                eth = user_detail[3]
                remaining_time = user_detail[0].split(" ")[0]
                remaining_time1 = ""
                for c in remaining_time:
                    if c == 'd' or c == 'h' or c == 'm':
                        remaining_time1 =  remaining_time1 + c + " "
                    else:
                        remaining_time1 =  remaining_time1 + c
                image_or_video = container.find_element_by_xpath('.//img[@class="sc-eirseW sc-lbVuaH sc-gGLyOc sc-ckTRkR evgNzS jMUgzO hSJDWM gCHypS sc-fbIXFq geecTj"]').get_attribute('src')
                print("========= Image =========")
                print(image_or_video)
                link = container.find_element_by_xpath('.//a[@class="sc-dlnjPT sc-hKFyIo sc-fKgIGh sc-bCwgka cuIYFB bElGhV PAjGx hGXmdA"]').get_attribute('href')
                print("link")
                print(link)
                print("\n")
                obj['link'] = link
                obj['image_or_video'] = image_or_video
                obj['title'] = title
                obj['name'] = name
                obj['eth'] = eth
                obj['remaining_time'] = remaining_time1
                auctions.append(obj)
                if i == 9:
                    break
                i = i + 1

            print(len(auctions))
            print(auctions)
            driver.quit()
            return Response({'auctions': auctions})
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno , e)
            return Response({'error': e})

class GetAuctionsMakersplace(APIView):
    def get(self, request, format=None):
        data = self.request.query_params
        try:
            company_name = data['companyName'] 
            print("=========GetAuctionsMakersplace=========")
            print(company_name)
            driver_path = os.path.join(settings.STATIC_ROOT, "chromedriver.exe")
            print(driver_path)
            
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
            options = webdriver.ChromeOptions()

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
            driver = webdriver.Chrome(executable_path=driver_path, options=options)
            # driver = webdriver.Chrome(executable_path=driver_path)
            t = time.time()
            try:
                print("=======try=======")
                driver.get('https://makersplace.com/discover/activity/')
                print("===end====")
            except TimeoutException:
                print("except")
            print('Time makersplace consuming:', time.time() - t)
            print("============")
            time.sleep(20)
            print("==============")
            containers = driver.find_elements_by_xpath('//div[@class="product-grid muuri"]/div')
            print(len(containers))
            i = 1
            auctions = []
            for container in containers:
                obj = {}
                print(i)
                user_detail = container.get_attribute("innerText")
                link = container.find_element_by_xpath('.//a[@class="muted product_url overlay_handler"]').get_attribute('href')
                img = container.find_element_by_xpath('.//img[@class="overlay_handler img-fluid item_image"]').get_attribute('src')
                price_detail = container.find_element_by_xpath('.//div[@class="overlay_handler row hover_details"]').get_attribute("innerText")
                print("===========")
                print(user_detail)
                user_detail = user_detail.split('\n')
                print(user_detail)
                print("==========")
                title = user_detail[0]
                name = user_detail[1]
                time1 = user_detail[len(user_detail)-1]
                print("title")
                print(title)
                print("name")
                print(name)
                print("link")
                print(link)
                print("img")
                print(img)
                print("detail")
                print(price_detail)
                
                print("\n")
                i=i+1
                obj['link'] = link
                obj['image'] = img
                obj['title'] = title
                obj['name'] = name
                obj['price'] = price_detail
                obj['time'] = time1
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

class GetAuctionsOpensea(APIView):
    def get(self, request, format=None):
        data = self.request.query_params
        try:
            company_name = data['companyName'] 
            print("=========GetAuctionsOpensea=========")
            print(company_name)
            url = "https://api.opensea.io/api/v1/assets"
            querystring = {"order_direction":"acs","offset":"0","limit":"20"}
            response = requests.request("GET", url, params=querystring)
            response = response.json()

            # print(response)
            auctions = response['assets']
            print(len(auctions ))
            return Response({'auctions': auctions})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno , e)
            return Response({'error': e})