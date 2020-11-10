from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import sys
import time
import argparse


driver = webdriver.Chrome('./chromedriver')
url = "https://amazon.in"
login_endpoint = "/ap/signin"

def head_to_login():
    driver.get(url)
    button = driver.find_element_by_xpath('//*[@id="nav-link-accountList"]/div/span')
    button.click()
    time.sleep(3)

def login(username, password):
    username_in = driver.find_element_by_xpath("//input[@id='ap_email']")
    submit_button = driver.find_element_by_xpath("//input[@id='continue']")
    username_in.send_keys(username)
    submit_button.click()
    time.sleep(3)

    password_in = driver.find_element_by_xpath("//input[@id='ap_password']")
    submit_button = driver.find_element_by_xpath("//input[@id='signInSubmit']")
    password_in.send_keys(password)
    submit_button.click()
    time.sleep(3)

def search_product(product):
    search_input = driver.find_element_by_xpath("//input[@id='twotabsearchtextbox']")
    search_input.send_keys(product + "\n")
    time.sleep(5)

def head_to_first_product():
    first_product = driver.find_element_by_xpath('//div[@data-component-type="s-search-result"]')
    link = first_product.find_element_by_xpath('//a[@class="a-link-normal a-text-normal"]')
    link.click()
    time.sleep(3)
    driver.switch_to.window(driver.window_handles[-1])

def add_to_wish_list(wish_list = None):
    button = driver.find_element_by_name('submit.add-to-registry.wishlist')
    button.click()
    time.sleep(1)
    if wish_list:
        list_input = driver.find_element_by_xpath("//input[@id='list-name']")
        list_input.clear()
        list_input.send_keys(wish_list)
        create_list = driver.find_element_by_xpath("//span[@id='wl-redesigned-create-list']")
        create_list.click()
        time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Add product from amazon india to wish list')
    parser.add_argument('--product', help='Product to search for and buy', default='iphone')
    parser.add_argument('--username', help='username')
    parser.add_argument('--password', help='password')
    parser.add_argument('--wish-list', help='Wish List Name', default=None)

    args = parser.parse_args()
    
    head_to_login()
    login(args.username, args.password)
    search_product(args.product)
    head_to_first_product()
    add_to_wish_list(args.wish_list)



