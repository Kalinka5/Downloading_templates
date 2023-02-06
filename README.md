# Downloading_templates
![Pypi](https://img.shields.io/pypi/v/selenium?color=orange&style=plastic)
![Python](https://img.shields.io/pypi/pyversions/selenium?color=gree&style=plastic)
![Forks](https://img.shields.io/github/forks/Kalinka5/Downloading_templates?style=social)
![Stars](https://img.shields.io/github/stars/Kalinka5/Downloading_templates?style=social)

:diamond_shape_with_a_dot_inside: To begin with, program is [**Selenium**](https://www.selenium.dev/selenium/docs/api/py/api.html) practicing with website [HiSlide](https://hislide.io/) where you can download model of different PowerPoint tempalates. 

:diamond_shape_with_a_dot_inside: In this code you can see simple examples of using selenium webdriver: 
+ *login in website*;
+ *click different buttons*;
+ *search template on page and if doesn't found it, goes to the next page*;
+ *wait until files are downloaded*;
+ *rename files in our folder*.
___

## *Usage*
:small_orange_diamond: First of all, **Selenium** uses decently different web drivers like *Chrome, Opera, Firefox* etc. The program uses **Chrome driver**, which always updates to new version when you run the program.

:small_orange_diamond: Also, you can use my config with HiSlide account or you can [*register a new own account*](https://hislide.io/my-account/) and work with it. 

:small_orange_diamond: In addition, I'm downloading certain tempalates **Halloween** and **Modern** themes, but you can download any other templates. To make this, you should change *config file*:gear:.

___

## *Example*
:small_red_triangle: As soon as you run this code, you can see *login page* where program will sign in to your account HiSlide:arrow_forward::

![login](https://user-images.githubusercontent.com/106172806/215406919-1a10630a-0941-47e5-8838-969060191cde.gif)


:small_red_triangle: Further, program automatically choose page **All Templates**, after that click **free** section.

:small_red_triangle: To choose the template I use function *choose_template()*:

```python
def choose_template(xpath: str, driver: webdriver, logger: Logger):
    """
    Choose current template on page. And if program don't found it, click on next page.

    :param xpath: element's xpath on webpage
    :param driver: webdriver (ChromeOptions(), FirefoxProfile()...)
    :param logger: logger to write logs
    """

    # Count of pages in free section
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
```
:small_red_triangle: The program wait 20 sec and if It doesn't find the certain template, it will click to the next page. As you can see below, It will click on the second page:arrow_forward::

![choose_the_template](https://user-images.githubusercontent.com/106172806/215406964-dab374b0-79e8-4281-baf6-f9cd74affa10.gif)

:small_red_triangle: Last but not least, downloading. It click big, green **Download** button. Then goes to another page *downloads*. The program will wait until the files appear in the folder.

:small_red_triangle: Returns to the initial page. Furthermore, click **free** section and download one more template:arrow_forward::

![downloading](https://user-images.githubusercontent.com/106172806/215406989-40ec227d-7370-4760-bd6e-40e5924acc2e.gif)

:small_red_triangle: Additional feature of this program is renaming files when they are downloaded.\
:small_red_triangle: This piece of code renames files:
```python
# Renaming all downloaded files 
file_name = dictionary["templates"][template]["name"]
for elem in os.listdir(path):
    if elem.startswith("0"):  # key word, which all files start with
        os.rename(rf"{path}\{elem}", rf"{path}\{file_name}{elem}")
```
:white_check_mark: As a result, you will get these files:

![files](https://user-images.githubusercontent.com/106172806/215419583-50ea9ee1-1db8-40e6-bb5d-26aae9cfc9e1.jpg)

___

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://user-images.githubusercontent.com/25423296/163456776-7f95b81a-f1ed-45f7-b7ab-8fa810d529fa.png">
  <source media="(prefers-color-scheme: light)" srcset="https://user-images.githubusercontent.com/25423296/163456779-a8556205-d0a5-45e2-ac17-42d089e3c3f8.png">
  <img alt="Shows an illustrated sun in light mode and a moon with stars in dark mode." src="https://user-images.githubusercontent.com/25423296/163456779-a8556205-d0a5-45e2-ac17-42d089e3c3f8.png">
</picture>
