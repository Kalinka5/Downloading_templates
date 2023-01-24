import time
from traceback import format_exc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException


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
        # time.sleep(3)

        logger.info('Filled in username')
        login_input = driver.find_element(By.ID, 'username')
        login_input.clear()
        login_input.send_keys(login)
        # time.sleep(2)

        logger.info('Filled in password')
        password_input = driver.find_element(By.ID, 'password')
        password_input.clear()
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        # time.sleep(5)

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
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='https://hislide.io/powerpoint-template/']"))).click()

        logger.info("Click on 'Free PowerPoint Templates'.")
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "a[href='https://hislide.io/free-powerpoint-templates/']"))).click()

        return None

    except Exception as e:
        logger.error(f"Unexpected error: \n{format_exc()}")


def choose_template(css, driver, logger):
    """Choose current template"""
    retries = 4
    for i in range(retries):
        page = i+2
        try:
            logger.info("Click on current Powerpoint template.")
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css))).click()
            break

        except TimeoutException:
            logger.info(f"Click on {page} page")
            css_page = "a[href='https://hislide.io/free-powerpoint-templates/page/" + str(page) + "/']"
            print(css_page)
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, css_page))).click()

        except Exception as e:
            logger.error(f"Unexpected error: \n{format_exc()}")


def downloading(driver, logger):
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
                EC.element_to_be_clickable((By.XPATH, "//button[@class='purchase-method-download']")))
            button.click()
            time.sleep(10)

            logger.info("Click close button after downloading.")
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button[class='remember-popup-close-button fancybox-button fancybox-button--close']"))).click()

            logger.info("Click on 'Free PowerPoint Templates'.")
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "a[href='https://hislide.io/free-powerpoint-templates/']"))).click()

            result = True
            break

        except ElementClickInterceptedException:
            logger.warning("Download button click was intercepted.\nTrying to click on the button again.")
            driver.execute_script("arguments[0].click()", button)
            result = False

    return result
