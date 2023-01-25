import time
from traceback import format_exc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
import os


def selenium_login(logger, dictionary: dict, driver):
    """

    :param logger: logger() to write logs
    :param dictionary: config file to get login, password
    :param driver: Chrome option where selenium will do all work
    :return: None
    This function open Chrome web page, then login to account in Sellerboard.
    """
    try:
        login = dictionary["HiSlide"]["login"]
        password = dictionary["HiSlide"]["password"]

        logger.info('Login through https://hislide.io/my-account/')
        driver.get("https://hislide.io/my-account/")
        time.sleep(3)

        logger.info("Click on close button")
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='Button__Block-sc-1c0eo6i-0 bhCgZe ModalControl__Control-sc-1dl29es-0 cLmiHt jsx-813992241 eapp-popup-control-close-component transition-exited']"))).click()
        time.sleep(5)

        logger.info('Filled in username')
        login_input = driver.find_element(By.ID, 'username')
        login_input.clear()
        login_input.send_keys(login)
        time.sleep(2)

        logger.info('Filled in password')
        password_input = driver.find_element(By.ID, 'password')
        password_input.clear()
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        time.sleep(5)

    except Exception as e:
        logger.error(f"Unexpected error: \n{format_exc()}")
        driver.close()
        driver.quit()


def selenium_searching(logger, driver):
    """

    :param logger: logger() to write logs
    :param driver: Chrome option where selenium will do all work
    :return: None
    This function will search all stores and click in it then click on yesterday button,
    and then it will click on “Download table (.xls)" button, finally rename file_name to shop name.
    """
    try:
        logger.info("Click on 'PowerPoint Templates'.")
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/']"))).click()
        time.sleep(5)

        logger.info("Click on 'Free PowerPoint Templates'.")
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[@href='https://hislide.io/shop/?filter_license=free']"))).click()
        time.sleep(5)

        return None

    except Exception as e:
        logger.error(f"Unexpected error: \n{format_exc()}")


def choose_template(xpath, driver, logger):
    """Choose current template"""
    retries = 142
    for i in range(retries):
        page = i+2
        try:
            logger.info("Click on current Powerpoint template.")
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            time.sleep(5)
            break

        except TimeoutException:
            logger.info(f"Click on {page} page")
            css_page = "//a[@class='next page-numbers']"
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, css_page))).click()

        except Exception as e:
            logger.error(f"Unexpected error: \n{format_exc()}")


def downloading(driver, logger, template, path, dictionary):
    """
    :param driver: webdriver (ChromeOptions(), FirefoxProfile()...)
    :param logger: logger() to write logs
    :return: True, False or None
    This function have 3 attempts to click the download button. If it is not clickable return False.
    If time out of downloading file (10 sec) it will try click again 3 times.
    """
    retries = 3
    result = False  # default func result
    for i in range(retries):
        try:
            logger.info("Click button 'Download Now'.")
            button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='product__btn']")))
            button.click()
            time.sleep(10)

            file_name = dictionary["templates"][template]["name"]
            for elem in os.listdir(path):
                if elem.startswith("0"):  # key word, which all files start with
                    os.rename(rf"{path}\{elem}", rf"{path}\{file_name}{elem}")

            result = True
            break

        except ElementClickInterceptedException:
            logger.warning("Download button click was intercepted.\nTrying to click on the button again.")
            driver.execute_script("arguments[0].click()", button)

    return result
