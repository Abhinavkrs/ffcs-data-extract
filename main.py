from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import urllib.request as ur
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
import tkinter 
import getpass
import re

main_url = 'https://vtop.vit.ac.in/student/stud_login.asp'
reg_no = raw_input('Enter your registration number: ')
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

#Change the last two letters according to the semester - WS/FS
browser.get('https://vtop.vit.ac.in/student/course_regular.asp?sem=WS')
course_data = browser.page_source
soup_data = BeautifulSoup(course_data,"html.parser")

table_elements = soup_data.select('form table tbody tr td')
all_elements = []

for element in table_elements:
	try:
		soup_data = BeautifulSoup(str(element),"html.parser")
				
		for line in soup_data:
			all_elements.append(line.font.string.strip())
	except:
		i = 0

all_elements = list(filter(None,all_elements))

sorted_elements = []
temp = []

for line in all_elements:
	if(line[0] != ''):
		if(line[0].isdigit() and len(line) <= 2):
			sorted_elements.append(temp)
			temp = []
		else:
			temp.append(line)

#Remove the top-most element in table which are the headers
del sorted_elements[0]

#all_slots = ['A1','A2','B1','B2','C1','C2','D1','D2','E1','E2','F1','F2','G1','G2','L1','L2','L3','L4','L5','L6','L7','L8','L9','L10','L11','L12','L13','L14','L15','L16','L17','L18','L19','L20','L21','L22','L23','L24','L25','L26','L27','L28','L29','L30','L31','L32','L33','L34','L35','L36','L37','L38','L39','L40','L41','L42','L43','L44','L45','L46','L47','L48','L49','L50','L51','L52','L53','L54','L55','L56','L57','L58','L59','L60']
all_slots = []

for course in sorted_elements:
	for details in course:
		slot_list = details.split("+")
		for x in slot_list:
			regex = re.search(r'^[A-Z][0-9]+',x)
			if(regex):
				all_slots.append(regex.group(0))
		
print(all_slots)
