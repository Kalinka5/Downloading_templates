import json
from logger import Logger
from selenium_func import selenium_login, selenium_searching, choose_template, downloading
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

        # create a folder where xls files were downloaded.
        if not os.path.exists("Files"):
            os.mkdir("Files")
            loger.info("Create the folder \"Files\"")

        # to remember the path to folder "Files".
        path = os.path.abspath("Files")

        # Set up Chrome server
        check_driver(os.path.abspath("chrome_driver"))  # загружает chromedriver последней версии
        options = webdriver.ChromeOptions()
        s = Service(r'chrome_driver\chromedriver.exe')  # Path to the installed ChromeDriver
        prefs = {"download.default_directory": path}  # Path to the folder "Files"
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=s, options=options)
        driver.implicitly_wait(10)

        selenium_login(loger, config, driver)
        selenium_searching(loger, driver)
        choose_template("a[href='https://hislide.io/product/halloween-powerpoint-template-free/']", driver, logger)
        downloading(driver, logger)
        choose_template("a[href='https://hislide.io/product/business-ppt-slides-free-download/']", driver, logger)
        downloading(driver, logger)

    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    try:
        logger = Logger(uniqueFileNamePrefics="Selenium")
        main(logger)
    except Exception as e:
        logger.error(f"Unexpected error: \n{format_exc()}")
