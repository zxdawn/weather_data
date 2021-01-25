import re
import time
import logging
import getpass
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

homepage = 'http://satellite.nsmc.org.cn/portalsite/default.aspx'
driver_path = '/usr/bin/chromedriver'  # path of chrome driver
savename = 'download_fy.sh'

# Choose the following line for info or debugging:
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)


def login(url):
    """Log into the FY website"""
    logging.info('Get the website content')
    driver = webdriver.Chrome(driver_path)
    driver.get(url)
    # driver.set_window_size(1200, 800)

    # input the username and password
    username = input('Input your username: ')
    driver.find_element_by_id('txtUserID').send_keys(username)
    password = getpass.getpass('Input your password: ')
    driver.find_element_by_id('txtPsw').send_keys(password)

    # switch to the frame of captcha
    driver.switch_to.frame('changeCodeImg')
    # input the captcha
    captcha = driver.find_element_by_id('imgCode')
    captcha = input('Input the captcha on the screen: ')

    # switch to the default content
    driver.switch_to.default_content()
    # send the captcha
    driver.find_element_by_id('txtCode').send_keys(captcha)

    # Click login button
    driver.find_element_by_id('btnLogin').click()
    time.sleep(5)

    return driver


def get_orders(driver):
    """Get all download links

    Note: "links" are just the basic ftp links,
    if the requested data is large, one basic link can be split into "sub_links".

    e.g.    AO20200701000065328
        --> AO202007010000653280001
        --> AO202007010000653280002
        --> AO202007010000653280003

    As the largest size of one job is ~ 9.8 G,
    which means that the largest number of sub_links is 3,
    we will create three sub_links based on the basic link,
    no matter whether they are all existed ...

    """
    logging.info('Switch to the "Order" page')
    driver.find_element_by_link_text('My Orders').click()

    # wait the page is loaded successfully
    time.sleep(3)

    # show 100 orders per page
    #   this is enough as the downloaded file size is limited by the FY website ...
    logging.info('Set the number of jobs per page to "100"')
    num_page = Select(driver.find_element_by_css_selector('#selectSize1'))
    num_page.select_by_value('100')
    time.sleep(5)

    # we can use the string of img icon to get the sub_links first
    #   e.g.    "showHidden('1','0','AO20200701000065328',this)"
    #       --> AO202007010000653280001
    #       --> AO202007010000653280002
    #       --> AO202007010000653280003
    logging.info('Get sub links')
    imgs = driver.find_elements_by_css_selector('#displayOrdersList tbody tr td:nth-child(1) img')
    sub_links = [img.get_attribute('onclick').split(',')[2].replace("'", '') for img in imgs]
    logging.debug(f'Sub links: {sub_links}')

    # cherry pick all of the <a>'s that are inside of each 7nd column "Download"
    # https://stackoverflow.com/questions/36270040/selenium-pull-href-out-of-td-in-table
    links = []
    prefix_sublink = {}

    logging.info('Get basic links')
    base_links = driver.find_elements_by_css_selector('#displayOrdersList tbody tr td:nth-child(7) a')
    for link in base_links:
        base_link = link.get_attribute('href')
        job_id = base_link.split(':')[1].replace('//', '')
        if job_id in sub_links:
            # save the prefix of sublink
            #   the prefix has the username and password for ftp links
            prefix_sublink[job_id] = base_link
        else:
            links.append(base_link+'*')

    logging.info('Get sub links')
    # # if one order has large file numbers, we need to click the img to show all the links
    for img in imgs:
        img.click()
    time.sleep(10)

    # if one order has large file numbers, we need to click the img to show all the links
    sub_tds = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//tr[@class='trInfo']")))
    for sub_td in sub_tds:
        for sub_link in sub_td.find_elements_by_css_selector('td:nth-child(1) a'):
            '''
            Example of the link in a href:
                    http://satellite.nsmc.org.cn/PortalSite/Ord/OrderStatus.aspx?
                    orderTimeType=0&orderType=1&
                    orderCode=A202101230507088073&
                    fillOrderCode=A2021012305070880730006
            '''
            split_sublink = re.split('orderCode=|&fillOrderCode=', sub_link.get_attribute('href'))
            order_code = split_sublink[1]
            links.append(prefix_sublink[order_code]+split_sublink[2]+'/*')

    # delete duplicated links
    links = list(sorted(set(links)))

    logging.debug(f'All Links: {links}')

    return links


def generate_script(links):
    """Generate the bash script of downloading all files"""
    logging.info(f'Save links to one bash script named {savename}')
    with open(savename, 'w') as f:
        f.write('#!/bin/bash\n')
        for link in links:
            f.write(f'lftp -e "mget -c {link}" &\n')


def main():
    # keep the browser open in case users need to do something later
    global driver

    # log into the FY website
    driver = login(homepage)

    # get the link of orders
    links = get_orders(driver)

    # generate the download script
    generate_script(links)

    logging.info('!!!!! Finish !!!!!')


if __name__ == '__main__':
    main()

# ----------------------------------------------------------------------------------------------------------------
# ---- Back up ----


def get_captcha_text(loc_frame, loc_captcha, size):
    """Automatically read the text

    Ref: https://stackoverflow.com/questions/59032322/bad-character-recognition-with-pytesseract-ocr-for-images-with-table-structure
         https://nanonets.com/blog/ocr-with-tesseract/
    """
    import cv2
    import imutils
    from PIL import Image
    from pytesseract import image_to_string

    im = Image.open('screenshot.png')  # uses PIL library to open image in memory

    # get the crop region
    left = loc_frame['x'] + loc_captcha['x']
    top = loc_frame['y'] + loc_captcha['y']
    right = loc_frame['x'] + loc_captcha['x'] + size['width']
    bottom = loc_frame['y'] + loc_captcha['y'] + size['height']

    # crop and save
    im = im.crop((left, top, right, bottom))

    # # enlarge the image
    im.save('screenshot.png')

    # get the text
    im = cv2.imread('screenshot.png')
    im = imutils.resize(im, width=700)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    thresh = cv2.GaussianBlur(thresh, (3, 3), 0)
    captcha_text = image_to_string(thresh, lang='eng', config='--psm 6')

    return captcha_text

# # read the captcha from input
# # ---- Not working accurately ---
# # get the location of the frame of captcha
# frame = driver.find_element_by_id('changeCodeImg')
# loc_frame = frame.location

# # locate and save the captcha to image file
# loc_captcha = captcha.location
# size = captcha.size
# driver.save_screenshot('screenshot.png')

# # get the text from screenshot
# captcha_text = get_captcha_text(loc_frame, loc_captcha, size)
