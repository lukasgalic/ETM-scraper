import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time


driver = webdriver.Chrome()
url = "https://www.europeantransportmaps.com/map/roro-ferry/operator"
driver.get(url)


lista = []

try:

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, 'map-menu-list-witharrows'))
    )
    print("Loading complete!")

    operators_list = driver.find_elements(
        By.CSS_SELECTOR, '.map-menu-list-witharrows li')

    for i in range(len(operators_list)):
        operators_list = driver.find_elements(
            By.CSS_SELECTOR, '.map-menu-list-witharrows li')

        operator = operators_list[i]
        operator_text = operator.text
        print(operator_text)

        link = operator.find_element(By.TAG_NAME, 'a')
        if link:
            href = link.get_attribute('href')

            driver.get(href)
            time.sleep(1)

            services_list = driver.find_elements(
                By.CSS_SELECTOR, '.map-menu-list-witharrows li')

            for i in range(len(services_list)):
                services_list = driver.find_elements(
                    By.CSS_SELECTOR, '.map-menu-list-witharrows li')
                service = services_list[i]
                service_text = service.text

                link2 = service.find_element(By.TAG_NAME, 'a')
                if link2:
                    href = link2.get_attribute('href')

                    driver.get(href)
                    time.sleep(1)

                    ro_pax = driver.find_elements(
                        By.CSS_SELECTOR, '.map-menu-category-box p')

                    for type in ro_pax:
                        type_text = type.text.split(":")[-1].strip()

                    routings = driver.find_elements(
                        By.CSS_SELECTOR, '.map-menu-list-witharrows li')

                    for routing in routings:
                        routing_text = routing.text

                        entry = [operator_text, service_text,
                                 type_text, routing_text]
                        lista.append(entry)
                driver.back()

            driver.back()

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'map-menu-list-witharrows'))
            )

    df = pd.DataFrame(
        lista, columns=['Operator', 'Services', 'Type', 'Routing'])

    print(df)

    df.to_excel('operators_and_services.xlsx', index=False)

finally:
    driver.quit()
