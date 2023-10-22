from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request


import pandas as pd
urls = []
# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36


#res = requests.get("https://search.naver.com/search.naver?where=image&sm=tab_jum&query=서울숲")
#res.raise_for_status()

#soup = BeautifulSoup(res.text, "lxml")
#images = soup.find_all("img", attrs={"class" :"_fe_image_viewer_image_fallback_target"})

#for image in images :
#    print(image["src"])
browser_path = 'C:/Users/김가연/Desktop/23-2학기/캡스톤2/chromedriver.exe'

browser = webdriver.Chrome(browser_path)
browser.get("https://www.google.co.kr/imghp?hl=ko&authuser=0&ogbl")
elem = browser.find_element_by_name("q")



elem.send_keys("서울숲")
elem.send_keys(Keys.RETURN)
time.sleep(3)
browser.find_elements_by_css_selector(".rg_i.Q4LuWd")[0].click()
time.sleep(2)
urls.append(browser.find_element_by_css_selector(".sFlh5c.pT0Scc.iPVvYb").get_attribute("src"))


time.sleep(2)
browser.find_elements_by_css_selector(".rg_i.Q4LuWd")[1].click()
time.sleep(2)
urls.append(browser.find_element_by_css_selector(".sFlh5c.pT0Scc.iPVvYb").get_attribute("src"))


time.sleep(2)
browser.find_elements_by_css_selector(".rg_i.Q4LuWd")[2].click()
time.sleep(2)
urls.append(browser.find_element_by_css_selector(".sFlh5c.pT0Scc.iPVvYb").get_attribute("src"))

for url in urls :
    print(urls)