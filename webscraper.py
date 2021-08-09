from selenium import webdriver
import time
import helpers as hp
from datetime import datetime
import json
import sys
from os.path import exists as ispath, dirname, basename, join as joinpath, abspath, sep as dirsep, isfile, splitext

sys.path.insert(0, joinpath(dirname(dirname(abspath(__file__)))))

# Selenium setup
exec_path = "C:\Selenium\chromedriver_win32\chromedriver.exe"
scrap_url = "https://indiacovidresources.in"

driver = webdriver.Chrome(executable_path=exec_path)
driver.get(scrap_url)

# maximize window
driver.maximize_window()
time.sleep(5)

# city search div
search_div = driver.find_element_by_xpath('//*[@id="app-root"]/div[2]/div[1]/div[2]/div/div[2]/div/input')
state_div = ""


# main
def main(city, service):
    # check if city param is valid
    if city != "":
        search_div.send_keys(city)
        time.sleep(5)
        # function call to find_city
        find_city("tile-title")

        # check if service param is valid
        if service != "":
            # function call to find_service
            find_service("tile-title", service)
            # store return value of find_service_data to data variable
            data = find_service_data("card-header", "card-title", "card-footer", city, service, state_div)
            print(json.dumps(data, indent=4))
            hp.send(data[0])


def find_city(city_div):
    city_divs = driver.find_elements_by_class_name(city_div)
    # defined global as used under find_service_data
    global state_div
    state_div = driver.find_element_by_class_name("sc-lgqmxq").text

    # check if city exists
    if city_divs.__len__() > 0:
        city_divs[0].click()
        time.sleep(5)
    else:
        print("Please input valid city name")
        driver.close()


def find_service(service_div, service):
    service_divs = driver.find_elements_by_class_name(service_div)

    # loop through all the services and match with service param
    for i in range(service_divs.__len__()):
        if service == service_divs.__getitem__(i).text:
            service_divs[i].click()

    time.sleep(5)


def find_service_data(name_div, phone_div, date_div, city, service, state):
    name_divs = driver.find_elements_by_class_name(name_div)
    phone_div = driver.find_elements_by_class_name(phone_div)
    date_div = driver.find_elements_by_class_name(date_div)
    data_dict = {}
    # creating dictionary
    for i in range(name_divs.__len__()):
        data_dict[i] = {
            "description": name_divs.__getitem__(i).text + "is available",
            "category": service,
            "state": state,
            "district": city,
            "phoneNumber": [phone_div.__getitem__(i).text],
            "addedOn": convert_to_timestamp(date_div.__getitem__(i).text),
            "modifiedOn": convert_to_timestamp(date_div.__getitem__(i).text)
        }

    return data_dict


def scroll_page(scroll_div_id):
    scroll_div_id_act = driver.find_element_by_css_selector("[id^=" + scroll_div_id + "]")
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                          scroll_div_id_act)
    time.sleep(2)


def convert_to_timestamp(last_verified):
    # Split date from text and date
    last_verified_split = last_verified.split(":", 1)

    # Split date to add missing year to current year
    last_verified_date = last_verified_split[1].strip().split(" ", 2)

    # Get current date to get current year
    today = datetime.today()

    # Convert into full date with current year
    convert_full_date = f"{last_verified_date[0].replace('th', '')} " + f"{last_verified_date[1].capitalize()} " + f"{today.year} " + f"{last_verified_date[2].replace('.', ':')}"

    # Convert into unix timestamp
    datetime_object = datetime.strptime(convert_full_date, '%d %b %Y %I:%M %p').timetuple()
    unix_timestamp = time.mktime(datetime_object)
    return unix_timestamp


if __name__ == "__main__":
    main("Delhi", "Hospital")

driver.close()
