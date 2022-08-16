import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

os.environ['PATH'] += r"C:/Selenium drivers"


def initDriver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # options.headless = True
    global driver
    driver = webdriver.Chrome(options=options)


def neighbour_construction(state, street, city, buildingNum, direction, dir_status):
    initDriver()
    cityURL = '-'.join(map(str, city))
    streetURL = '-'.join(map(str, street))
    url = f"https://www.neighborwho.com/{streetURL}-{cityURL}-{state}-addresses"
    driver.get(url)
    if dir_status == 1:
        compare_text = f"{buildingNum} {' '.join(map(str,street))} {direction[0]}"
    else:
        compare_text = f"{buildingNum} {' '.join(map(str,street))}"
    while True:
        elements = driver.find_elements(By.CLASS_NAME, 'card-title')
        for item in elements:
            if item.text.upper() == compare_text.upper():
                parent = item.find_element(By.XPATH, "..")
                upper_parent = parent.find_element(By.XPATH, "..")
                year_built = upper_parent.find_elements(By.XPATH, ".//*")
                for item in year_built:
                    new_list = item.text.split("\n")
                    for new_item in new_list:
                        if "Built in" in new_item:
                            value = new_item[9:]
                            print(f"NEIGHBOURWHO: {value}")

                            return

        next = driver.find_elements(By.CLASS_NAME, "next-arrow-on")
        if next:
            next[0].click()
            continue
        else:
            break

    print("NEIGHBOURWHO: Not found")
    return


def spokeo_construction(state, street, city, buildingNum, direction, dir_status):

    city_url = '-'.join(map(str, city))
    street_url = '-'.join(map(str, street))
    if dir_status == 1:
        url = f"https://www.spokeo.com/{state}/{city_url}/{buildingNum}-{street_url}-{direction[0]}"
    else:
        url = f"https://www.spokeo.com/{state}/{city_url}/{buildingNum}-{street_url}"

    driver.get(url)
    property_card = driver.find_elements(By.CLASS_NAME, 'summary-details')
    if len(property_card) > 0:
        property_list = property_card[0].text.split("\n")
        for item in property_list:
            if item == "YEAR BUILT":
                index = property_list.index(item)
                year_constructed_spokeo = property_list[index+1]
                print(f"SPOKEO: {year_constructed_spokeo}")
                driver.quit()
                return

    print("SPOKEO: Not found")
    driver.quit()
