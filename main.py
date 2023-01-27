import json
from logger import Logger
from selenium_func import selenium_login, open_all_templates, selenium_working
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import os
from traceback import format_exc
from chrome_driver_version import check_driver


def main(loger):
    try:
        # dictionary with all config
        with open('configs.json') as file:
            config = json.load(file)

        # create a folder where templates will be downloaded.
        if not os.path.exists("Files"):
            os.mkdir("Files")
            loger.info("Create the folder \"Files\"")

        # to remember the path to folder "Files".
        path = os.path.abspath("Files")

        # Set up Chrome server
        check_driver(os.path.abspath("chrome_driver"))  # download chromedriver last version
        options = webdriver.ChromeOptions()
        s = Service(r'chrome_driver\chromedriver.exe')  # Path to the installed ChromeDriver
        prefs = {"download.default_directory": path}  # Path to the folder "Files"
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--start-maximized")  # open Chrome with full window
        driver = webdriver.Chrome(service=s, options=options)
        driver.implicitly_wait(10)

        selenium_login(loger, config, driver)

        open_all_templates(loger, driver)

        for template in config["templates"]:
            selenium_working(loger, driver, config, template, path)

    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    try:
        logger = Logger(uniqueFileNamePrefics="Selenium")
        main(logger)
    except Exception as e:
        logger.error(f"Unexpected error: \n{format_exc()}")
