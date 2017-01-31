from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import urllib.request as ur
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
import tkinter 
import getpass

main_url = 'https://vtop.vit.ac.in/student/stud_login.asp'
reg_no = input('Enter your registration number: ')
password = getpass.getpass('Enter your password:')

browser = webdriver.PhantomJS()
browser.get(main_url)
assert "FFCS" in browser.title

reg_tb = browser.find_element_by_class_name("textbox2")
pass_tb = browser.find_element_by_name("passwd")

reg_tb.send_keys(reg_no)
pass_tb.send_keys(password)

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

browser.get('https://vtop.vit.ac.in/student/course_regular.asp?sem=WS')
course_data = browser.page_source
soup_data = BeautifulSoup(course_data,"html.parser")

table_elements = soup_data.select('form table tbody tr td')
all_elements = []

for element in table_elements:
	try:
		soup_data = BeautifulSoup(str(element),"html.parser")
		temp = []
		for line in soup_data:
			temp.append(line.font.string.strip())
	except:
		i = 0

	all_elements.append(temp)

for line in all_elements:
	print(line)

