from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import urllib.request as ur
from bs4 import BeautifulSoup

main_url = 'https://vtop.vit.ac.in/student/stud_login.asp'

#web_data = str(ur.urlopen(main_url).read())
#print(web_data)

browser = webdriver.Firefox()
