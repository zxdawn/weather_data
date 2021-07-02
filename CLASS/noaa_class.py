import re
import click
import time
import logging
import getpass
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

homepage = 'https://www.avl.class.noaa.gov/saa/products/classlogin?resource=%2Fsaa%2Fproducts%2Fwelcome'#http://satellite.nsmc.org.cn/portalsite/default.aspx'
driver_path = '/usr/bin/chromedriver'  # path of chrome driver

# Choose the following line for info or debugging:
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)


def login(url, username, password):
    """Log into the FY website"""
    logging.info('Get the website content')
    driver = webdriver.Chrome(driver_path)
    driver.get(url)
    # driver.set_window_size(1200, 800)

    # input the username and password
    # username = input('Input your username: ')
    # username = 'xinzhang121'
    driver.find_element_by_name('j_username').send_keys(username)
    # password = getpass.getpass('Input your password: ')
    # password = 'zhangxin62313'
    driver.find_element_by_name('j_password').send_keys(password)

    # Click login button
    driver.find_element_by_css_selector(".Button[value='Login']").click()
    time.sleep(5)

    return driver

def input_date(driver, element_name, input_value):
    '''clean the key'''
    logging.info(f'Input {element_name}: {input_value}')
    webElement = driver.find_element_by_name(element_name)
    webElement.send_keys(Keys.CONTROL + "a")
    webElement.send_keys(Keys.DELETE)
    webElement.send_keys(input_value)

def select_element(driver, name, value):
    '''select element by name and value'''
    logging.info(f'select {name}: {value}')
    select = Select(driver.find_element_by_xpath(f"//select[@name='{name}']"))
    select.select_by_value(value)

def product_page(driver, product, start_date, end_date,
                 channel, dataset, satellite, scan_mode):
    '''switch to product page'''
    # the select has bug, we have to change to the page manually
    # select_element(driver, 'datatype_family', product)
    # click the Go to page button
    # driver.find_elements_by_xpath("//input[@type='image' and @name='submit']").click()
    product_page = f'https://www.avl.class.noaa.gov/saa/products/search?sub_id=0&datatype_family={product}'
    driver.get(product_page)


    # input time info
    input_date(driver, 'start_date', start_date.split('_')[0])
    input_date(driver, 'start_time', start_date.split('_')[1]+':00')
    input_date(driver, 'end_date', end_date.split('_')[0])
    input_date(driver, 'end_time', end_date.split('_')[1]+':00')

    # input dataset info
    if channel:
        select_element(driver, 'ABI Channel', channel)
    select_element(driver, 'Product Type', dataset)
    select_element(driver, 'Satellite', satellite)
    select_element(driver, 'ABI Scan Sector', scan_mode)

    # search and submit the order
    driver.find_element_by_css_selector(".Button[value='Quick Search & Order']").click()

    # submit the order
    time.sleep(5)
    logging.info(f'Submit the order')
    driver.find_element_by_css_selector(".Button[value='PlaceOrder']").click()

# -------------------------------------------------------
@click.command()
@click.option(
    '--sdate',
    '-sd',
    help='''
            Beginning date of downloaded files
            YYYY-MM-DD_hh:mm
         '''
)

@click.option(
    '--edate',
    '-ed',
    help='''
            Ending date of downloaded files
            YYYY-MM-DD_hh:mm
         '''
)

@click.option(
    '--product',
    '-p',
    type=click.Choice(['GRABIPRD']),
    default='GRABIPRD',
    help='''
            Product name in Capital.
            GRABIPRD
         ''',
    show_default=True,
)

@click.option(
    '--channel',
    '-c',
    type=click.Choice(['C01', 'C02', 'C03', 'C04',
                       'C05', 'C06', 'C07', 'C08',
                       'C09', 'C10', 'C11', 'C12',
                       'C12', 'C13', 'C14', 'C15', 'C16']),
    help='''
            Channel name in Capital.
            GRABIPRD
         ''',
    show_default=True,
)

@click.option(
    '--dataset',
    type=click.Choice(['Rad', 'CMIP', 'MCMIP', 'ACHA',
                       'ACHT', 'ACM', 'ACTP', 'ADP',
                       'AOD', 'COD', 'CPS', 'CTP', 'DMW',
                       'DMWV', 'DSI', 'DSR', 'FDC',
                       'FSC', 'HIE', 'LST', 'LVMP',
                       'RRQPE', 'RSR', 'SST', 'TPW',
                       'VAA', 'LVTP', 'DMWDIAG', 'DMWPQI',
                       'DMWVDIAG', 'DMWVPQI', 'AICE',
                       'AIM', 'AITA']),
    default='ACHA',
    help='''
            Product type in Capital.
         ''',
    show_default=True,
)

@click.option(
    '--satellite',
    type=click.Choice(['G16', 'G17']),
    default='G16',
    help='''
            Product type in Capital.
         ''',
    show_default=True,
)

@click.option(
    '--scan_mode',
    type=click.Choice(['F', 'C', 'M1', 'M2']),
    default='C',
    help='''
            Scan mode in Capital.
            F, C, M1, or M2
         ''',
    show_default=True,
)

@click.option(
    '--username',
    '-u',
    help='Username',
    show_default=True
)

@click.option(
    '--password',
    '-pwd',
    help='Password',
    show_default=True
)


def main(sdate, edate, product, channel,
         dataset, satellite, scan_mode,
         username, password):
    # global driver

    # log into the NOAA CLASS website
    driver = login(homepage, username, password)

    # create the order
    product_page(driver, product, sdate, edate, channel, dataset, satellite, scan_mode)


if __name__ == '__main__':
    main()
