from selenium import webdriver
from selenium.webdriver.common.by import By
import requests


def generatorTest(driver, link, name, errors_array):
    print('finding generator web part...')
    driver.get(link)

    try:
        generator = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='categoryBox statisticsBox']//div//a")))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")
        errors_array.append((link, name))
        return
    except NoSuchElementException:
        print("Element did not found")
        return
    generator_link = generator.get_attribute('href')

    if(generator_link == 'javascript:void(0)'):
        errors_array.append((link, name))
        print('invalid link')
        return
    try:
        r = requests.head(generator_link)
    except Exception as e:
        errors_array.append((link, name))
        return
    if(not r.status_code == 200):
        errors_array.append((link, name))
        return
    # work well
    print('work well')
    return