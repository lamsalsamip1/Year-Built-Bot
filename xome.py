from pydoc import classname
from types import NoneType
from typing import final
from bs4 import BeautifulSoup
import requests


def search_table(url, compare_text1, compare_text2):
    if (url != 0):

        html_text = requests.get(url, verify=False).text
        soup = BeautifulSoup(html_text, 'html.parser')

        new_table = soup.find('table', id="Master_Properties")
        if new_table == None:
            print("XOME\t\t: Not found")
            return [0, 0]
        new_table.find_all('tr')

        search_table = new_table.find_all('td')
        for item in search_table:

            if (item.text[1:-1].upper() == compare_text1 or item.text[1:-1].upper() == compare_text2):

                final_url = f"https://www.xome.com/{item.find('a')['href']}"
                return [1, final_url]

    return [0, soup]


def find_year(url):
    if (url == 0):
        return 0
    html_text = requests.get(url, verify=False).text
    soup = BeautifulSoup(html_text, 'html.parser')
    cards = soup.find_all('div', class_="detail-item")
    if (len(cards) == 0):
        return 0
    for card in cards:
        if card.find('div', class_="col detail-label").text == "Year Built":
            year_const = card.find(
                'div', class_='col detail-value').text
            if year_const == "" or year_const == 0:
                year_const = "Not found"

            return year_const
    return 0


def xomeConstruction(state, city, street, buildingNum, zip, original_address, dir_status, direction):

    requests.packages.urllib3.disable_warnings()

    final_url = 0
    new_url = 0
    status = 0
    cityURL = '-'.join(map(str, city))

    url = f"https://www.xome.com/realestate/{state}/{cityURL}/{zip}/StreetList/"

    html_text = requests.get(url, verify=False).text
    soup = BeautifulSoup(html_text, 'html.parser')

    check_single = find_year(url)
    if (check_single != 0):
        print(f"XOME\t\t: {check_single}")
        return
    table = soup.find('table', id="Master_dlStreet")
    if (table == None):
        print("XOME\t\t: Not found")
        return

    streetList = table.find_all('a')

    for item in streetList:
        item_list = item.text.split(' ')[-4::-1][::-1]
        length = len(item_list)
        new_item_list = ' '.join(map(str, item_list)).upper()

        if new_item_list == ' '.join(map(str, street[0:length])):
            new_url = f"https://www.xome.com/{item['href']}"
            break

    check_single = find_year(new_url)
    if (check_single != 0):
        print(f"XOME\t\t:{check_single}")
        return

    if dir_status == 1:
        compare_text1 = f"{buildingNum} {direction[0]} {' '.join(map(str,street))} {' '.join(map(str,city))} {state} {zip}"
        compare_text2 = f"{buildingNum} {' '.join(map(str,street))} {direction[0]} {' '.join(map(str,city))} {state} {zip}"
    else:
        compare_text1 = compare_text2 = original_address.upper()
    page = 0
    final = search_table(new_url, compare_text1, compare_text2)
    if final[0] == 1:
        final_url = final[1]
    else:
        final_url = 0
    if (final_url == 0):
        html_text = requests.get(new_url, verify=False).text
        soup = BeautifulSoup(html_text, 'html.parser')
        next_page = soup.find('a', class_="next-page-icon")
        if type(next_page) == NoneType:
            print("XOME\t\t: Not found")
            return
        else:
            while len(next_page) != 0:
                page = page+1
                next_page = soup.find_all('a', class_="next-page-icon")
                new = f"https://www.xome.com/realestate/{state}/{cityURL}/{zip}/{street[0]}?page={page}"
                final_res = search_table(new, compare_text1, compare_text2)
                if final_res[0] == 1:
                    final_url = final_res[1]
                else:
                    soup = final_res[1]
                    if (soup == 0):
                        return
                    final_url = 0
                if final_url != 0:
                    break

    if final_url == 0:
        print("XOME\t\t: Not found")
        return
    else:

        result = find_year(final_url)
        if (result != 0):
            print(
                f"XOME\t\t: {result}")
        else:
            print("XOME\t\t: Not found")
            return
