from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import urllib.request as ur
from bs4 import BeautifulSoup

main_url = 'https://vtop.vit.ac.in/student/stud_login.asp'

web_data = str(ur.urlopen(main_url).read())
#print(web_data)

browser = webdriver.Firefox()
browser.get(main_url)
assert "FFCS" in browser.title

reg_tb = browser.find_element_by_class_name("textbox2")
pass_tb = browser.find_element_by_name("passwd")

reg_no = input('Enter your registration number - ')
password = input('Enter your password - ')

reg_tb.send_keys(reg_no)
pass_tb.send_keys(password)
