# Name: Joshua Venable
# Date: 12/26/2022
# Description: After giving the student's classes, and what days of the week they are held, this program will export the dates of the classes to a .csv file.
# Notes:
# v.1.1.0


import sys
import requests
from selenium import webdriver

# set up the webdriver


def setup_driver() -> webdriver:
    """Set up the webdriver.

    Returns:
        webdriver: The webdriver.
    """
    options = webdriver.EdgeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Edge(options=options)
    return driver

# read the config.properties file


def read_config() -> dict:
    """Read the config.properties file.

    Returns:
        dict: A dictionary of the email and password.
    """
    config = {}
    with open('config.properties', 'r') as f:
        config['email'] = f.readline().split(' ')[1].strip()
        config['password'] = f.readline().split(' ')[1].strip()
        config['url'] = f.readline().split(' ')[1].strip()

    return config


def get_to_login():
    session = requests.Session()
    config = read_config()
    session.post(config['url'], data={config['email'], config['password']})
    

get_to_login()