# Selenium
![Pypi](https://img.shields.io/pypi/v/selenium?color=orange)
![Python](https://img.shields.io/pypi/pyversions/selenium?color=gree&style=plastic)
![Forks](https://img.shields.io/github/forks/Kalinka5/detective_game?style=social)

To begin with, program is **Selenium** practicing with website [HiSlide](https://hislide.io/) where you can download model of different PowerPoint tempalates. 

In this code you can see simple examles of using selenium webdriver from *login in website* to *how to wait downloading files and then rename this file in our folder*.
___

## *Usage*
First of all, **Selenium** uses decently different web drivers like *Chrome, Opera, Firefox* etc. The program uses **Chrome driver**, which always updates to new version when you run the program.

Also, you can use my config with HiSlide account or you can [*register a new own account*](https://hislide.io/my-account/) and work with it. 

In addition, I'm downloading certain tempalates **Halloween** and **Modern** themes, but you can download any other templates. To make this, you should change config file.

___

## *Example*
As soon as you run this code, you can see *login page* where program will sign in to your account HiSlide.

![login](https://user-images.githubusercontent.com/106172806/215406919-1a10630a-0941-47e5-8838-969060191cde.gif)


Further, program automatically choose page **All Templates**, after that click **free** section.

To choose the template I use function *choose_template()*:

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
The program wait 20 sec and if It doesn't find the certain template, it will click to the next page. As you can see below, It will click on the second page.

![choose_the_template](https://user-images.githubusercontent.com/106172806/215406964-dab374b0-79e8-4281-baf6-f9cd74affa10.gif)

Last but not least, downloading. It click big, green **Download** button. Then goes to another page *downloads*. The program will wait until the files appear in the folder.

Returns to the initial page. Furthermore, click **free** section.

![downloading](https://user-images.githubusercontent.com/106172806/215406989-40ec227d-7370-4760-bd6e-40e5924acc2e.gif)

Additional feature of this program is renaming files when they are downloaded.
This piece of code renames files:
```python
# Renaming all downloaded files 
file_name = dictionary["templates"][template]["name"]
for elem in os.listdir(path):
    if elem.startswith("0"):  # key word, which all files start with
        os.rename(rf"{path}\{elem}", rf"{path}\{file_name}{elem}")
```
As a result, you will get these files:

![files](https://user-images.githubusercontent.com/106172806/215419583-50ea9ee1-1db8-40e6-bb5d-26aae9cfc9e1.jpg)

___

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://user-images.githubusercontent.com/25423296/163456776-7f95b81a-f1ed-45f7-b7ab-8fa810d529fa.png">
  <source media="(prefers-color-scheme: light)" srcset="https://user-images.githubusercontent.com/25423296/163456779-a8556205-d0a5-45e2-ac17-42d089e3c3f8.png">
  <img alt="Shows an illustrated sun in light mode and a moon with stars in dark mode." src="https://user-images.githubusercontent.com/25423296/163456779-a8556205-d0a5-45e2-ac17-42d089e3c3f8.png">
</picture>
