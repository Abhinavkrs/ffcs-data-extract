from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import urllib.request as ur
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
import urllib.parse as up
import tkinter 
import getpass
import time

main_url = 'https://vtop.vit.ac.in/student/stud_login.asp'
reg_no = input('Enter your registration number: ')
password = getpass.getpass('Enter your password:')

#web_data = ur.urlopen(main_url).read()
#print(web_data)

browser = webdriver.PhantomJS()
browser.get(main_url)
assert "FFCS" in browser.title

reg_tb = browser.find_element_by_class_name("textbox2")
pass_tb = browser.find_element_by_name("passwd")

reg_tb.send_keys(reg_no)
pass_tb.send_keys(password)

#soup_data = BeautifulSoup(web_data,"html.parser")

cap_img = browser.find_element_by_id("imgCaptcha")
captcha_location = cap_img.location
captcha_size = cap_img.size
browser.save_screenshot('captcha.png')

im = Image.open('captcha.png')
left = captcha_location['x']
top = captcha_location['y']
right = captcha_location['x'] + captcha_size['width']
bottom = captcha_location['y'] + captcha_size['height']

im = im.crop((left, top, right, bottom))
im.save('captcha.png')
im.close()

im = Image.open('captcha.png')
root = tkinter.Tk()
tkimage = ImageTk.PhotoImage(im)
tkinter.Label(root, image=tkimage).pack()
#root.mainloop()

captcha_data = input('Enter the Captcha: ')
captcha_tb = browser.find_element_by_name("vrfcd")
captcha_tb.send_keys(captcha_data)

submit_btn = browser.find_element_by_class_name("submit3")
submit_btn.click()

time.sleep(5)
login_url = browser.current_url
assert "FFCS" in browser.title

browser.get('https://vtop.vit.ac.in/student/course_regular.asp?sem=WS')
print(browser.page_source)
