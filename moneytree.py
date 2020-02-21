from selenium import webdriver
from datetime import datetime
import config as config
import time
import sys
import csv

def login(username, password):
    browser \
        .find_element_by_css_selector(elements['username']) \
        .send_keys(username)
    browser \
        .find_element_by_css_selector(elements["password"]) \
        .send_keys(password)
    browser \
        .find_element_by_css_selector(elements["submit"]) \
        .click()

def get_account_amount_xpath(account_name):
    return '//left-column-body//item-content/mt-account/div/span[text()="' + account_name + '"]/../span[2]'

###########################################################

login_link='https://app.getmoneytree.com/app/vault'

###########################################################

elements = {
    'username': 'input[name*=email]',
    'password': 'input[name*=password]',
    'submit': 'button[type=submit]',
    'personal': '//div/ul/li/a[text()="Personal"]',
    'banks': '//left-column-body//a/span[text()="Banks"]',
    'investments': '//left-column-body//a/span[text()="Investments & Insurance"]',
    'other': '//left-column-body//a/span[text()="Other Accounts"]'
}

###########################################################

if len(sys.argv) != 2:
    print 'One and only one argument allowed'
    sys.exit()

command = sys.argv[1]

if command != 'setup' and command != 'refresh' and command != 'parse':
    print 'Must be either setup, refresh or parse'
    sys.exit()

if command == 'setup':
    with open('balance.csv','w') as fd:
        fd.write(
            "Date," + \
            ",".join(
                config.accounts
            ) + \
            "\n"
        )
    sys.exit()

browser = webdriver.Chrome('/usr/local/bin/chromedriver')

try:
    browser.get(login_link)
    time.sleep(10)

    login(config.username, config.password)
    time.sleep(10)

    if command == 'refresh':
        sys.exit()

    browser \
        .find_element_by_xpath(elements['personal']) \
        .click()
    time.sleep(5)

    browser \
        .find_element_by_xpath(elements['banks']) \
        .click()

    browser \
        .find_element_by_xpath(elements['investments']) \
        .click()

    browser \
        .find_element_by_xpath(elements['other']) \
        .click()

    time.sleep(5)

    with open('balance.csv','a') as fd:
        fd.write(
            str(datetime.date(datetime.now())) + "," + \
            ",".join(
                map(
                    lambda account: browser \
                        .find_element_by_xpath(get_account_amount_xpath(account)) \
                        .text \
                        .replace('$', '') \
                        .replace(',', ''),
                    config.accounts
                )
            ) + \
            "\n"
        )
finally:
    browser.close()
