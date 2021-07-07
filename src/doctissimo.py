from random import expovariate
from requests.api import get
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options as Firefox_Options
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
import time

import os
from sys import platform as p_os

import requests
from bs4 import BeautifulSoup as bs

import random
import string
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OS_ENV = "windows" if p_os == "win32" else "osx" if p_os == "darwin" else "linux"

class Settings:

    chromedriver_min_version = 2.36

    specific_chromedriver = "chromedriver_{}".format(OS_ENV)
    chromedriver_location = os.path.join(BASE_DIR, "assets", specific_chromedriver)

    if not os.path.exists(chromedriver_location):
        chromedriver_location = os.path.join(BASE_DIR, 'assets', 'chromedriver.exe')

chromedriver_location = Settings.chromedriver_location
#print(chromedriver_location)

def get_address():
    try:
        url = 'https://generator.email'
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Cache-Control": "no-cache",
#            "Connection": "keep-alive, Upgrade",
            "Upgrade": "websocket",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0"
        }
        res = requests.get(url, headers=headers)
        soup = bs(res.text, 'html.parser')

        email_name = soup.find('span', attrs={'id': 'email_ch_text'}).text
        return email_name
    except Exception as e:
        return e

def random_name():  return ''.join(random.choice(string.ascii_letters) for i in range(8))
def random_password(): return ''.join(random.choice(string.digits + string.ascii_lowercase + string.ascii_uppercase+ string.digits) for i in range(12))
def real_name():
    try:
        url = 'https://api.namefake.com/french-france/male'
        return json.loads(requests.get(url).text)['name'].replace(' ', '').replace("'", '').replace('.', '') + random.choice(string.digits) + random.choice(string.digits) + random.choice(string.digits)
    except Exception as e:
        pass

def create_account(EMAIL):
    email = EMAIL
    name = real_name()
    password = random_password()
    try:
        url = 'https://forum.doctissimo.fr/inscription-1.html'
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
#            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0"
        }
        data = {
            "email": email,
            "pseudo": name,
            "name": name,
            "password": password,
            "repeatpassword": password,
            "sex": "1",
            "birthdate": "01/01/1987",
            "module[]": "doctissimo_core",
            "data_collect": "1",
            "fifteen_years_old": "1",
            "data_nl_hebdo": "1",
            "offers": "1",
            "offer_partner": "1",
            "referer_url": "https://club.doctissimo.fr",
            "register": "1"
        }
        res = requests.post(url,headers=headers, data=data)
        if res.status_code == 200:
            print('Done!')
    except Exception as e:
        print(str(e) + '\terror in creating')

def get_mail(address):
    url_m = f'https://generator.email/{address}'
    res = requests.get(str(url_m))
    soup = bs(res.text, 'html.parser')

    links = soup.find_all('a', attrs={'rel': 'nofollow'})
    for link in links:
        if 'https://club.doctissimo.fr' in link['href']:
            print('Verified!')
            return requests.get(link.text)

def doing(title, desc):

    email_v = get_address()
    create_account(email_v)

    chrome_options = Options()
    #chrome_options.add_argument('headless')
    chrome_options.add_argument('Content-Type="text/html"')
    chrome_options.add_argument('chartset=utf-8')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-crash-reporter")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-in-process-stack-traces")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--output=/dev/null")
    driver = webdriver.Chrome(executable_path=chromedriver_location, chrome_options=chrome_options)

    url_m = f'https://generator.email/{email_v}'
    driver.get(url_m)
    time.sleep(5)
    link = driver.find_elements_by_xpath('//a[@rel="nofollow"]')[2].get_attribute('href')
    print(link)
    driver.get(str(link))
    #driver.get('https://forum.doctissimo.fr/login.html')
    time.sleep(10)
    try:
        driver.find_element_by_xpath('//span[contains(text(), "accepte tout")]').click()
    except:
        pass

    try:
        driver.get('https://forum.doctissimo.fr/sante/Troubles-de-l-erection/nouveau_sujet.htm')
        time.sleep(5)

        sujet = driver.find_element_by_xpath('//input[@name="sujet"]')
        sujet.send_keys(title)

        time.sleep(5)

        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_xpath('//div[@id="content_form_base_switch_wysiwyg"]'))

        time.sleep(2)

        change = driver.find_element_by_xpath('//div[@id="content_form_base_switch_wysiwyg"]')
        change.click()

        time.sleep(5)

        content = driver.find_element_by_xpath('//textarea[@name="content_form"]')
        content.click()
        content.send_keys(desc)
        time.sleep(5)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(3)

        f = driver.find_element_by_xpath('//input[@name="submit_form"]')
        f.click()

        time.sleep(5)

        print('Posted!')

        driver.quit()
    except Exception as e:
        print(e)