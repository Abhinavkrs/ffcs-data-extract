from selenium import webdriver
import cv2 
def get_cap():
    main_url = 'https://vtop.vit.ac.in/student/stud_login.asp'

    browser = webdriver.Chrome()
    browser.get(main_url)
    assert "FFCS" in browser.title
    browser.save_screenshot('captcha.png')

    im = cv2.imread('captcha.png')
    im_cropped = cv2.getRectSubPix(im,(102,25),(725,375))
    return im_cropped
