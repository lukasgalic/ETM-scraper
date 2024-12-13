import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


driver = webdriver.Chrome()
url = "https://www.europeantransportmaps.com/map/roro-ferry/ports-and-terminals"
driver.get(url)


lista = []

try:

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, 'map-menu-list-witharrows'))
    )
    print("Loading complete!")

    list_countries = driver.find_elements(
        By.CSS_SELECTOR, '.map-menu-list-witharrows li')

    for i in range(len(list_countries)):
        list_countries = driver.find_elements(
            By.CSS_SELECTOR, '.map-menu-list-witharrows li')

        country = list_countries[i]
        country_text = country.text
        print(country_text)
        print("Country: " + country.text)

        link = country.find_element(By.TAG_NAME, 'a')
        if link:
            href = link.get_attribute('href')

            driver.get(href)
            time.sleep(1)

            list_cities = driver.find_elements(
                By.CSS_SELECTOR, '.map-menu-list-witharrows li')

            for i in range(len(list_cities)):
                list_cities = driver.find_elements(
                    By.CSS_SELECTOR, '.map-menu-list-witharrows li')
                city = list_cities[i]
                city_text = city.text
                print("City: " + city.text)

                link2 = city.find_element(By.TAG_NAME, 'a')
                if link2:
                    href = link2.get_attribute('href')

                    driver.get(href)

                    list_options = driver.find_elements(
                        By.CSS_SELECTOR, '.map-menu-list-witharrows li')

                    if len(list_options) > 1:
                        see_all_terminals = list_options[1]

                        link3 = see_all_terminals.find_element(
                            By.TAG_NAME, 'a')
                        if link3:
                            href = link3.get_attribute(
                                'href')  # Get the URL

                            driver.get(href)
                            time.sleep(1)

                            list_terminals = driver.find_elements(
                                By.CSS_SELECTOR, '.map-menu-list-witharrows li')

                            if list_terminals:
                                for terminal in list_terminals:
                                    terminal_text = terminal.text
                                    entry = [country_text,
                                             city_text, terminal_text]
                                    lista.append(entry)

                    driver.back()
                driver.back()

            driver.back()

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'map-menu-list-witharrows'))
            )
    df = pd.DataFrame(lista, columns=['Country', 'City', 'Terminal'])

    print(df)

    df.to_excel('ports_and_terminals.xlsx', index=False)

finally:
    driver.quit()
