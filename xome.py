from bs4 import BeautifulSoup
import requests


def xomeConstruction(state, city, street, buildingNum, zip, original_address, dir_status, direction):

    requests.packages.urllib3.disable_warnings()

    final_url = 0
    new_url = 0
    status = 0
    cityURL = '-'.join(map(str, city))

    url = f"https://www.xome.com/realestate/{state}/{cityURL}/{zip}/StreetList/"

    html_text = requests.get(url, verify=False).text
    soup = BeautifulSoup(html_text, 'html.parser')

    table = soup.find('table', id="Master_dlStreet")
    if (table == None):
        print("XOME:Not found")
        return

    streetList = table.find_all('a')

    compare_street = ' '.join(map(str, street))

    for item in streetList:
        item_list = item.text.split(' ')[-4::-1][::-1]

        new_item_list = ' '.join(map(str, item_list)).upper()

        if new_item_list in compare_street:
            new_url = f"https://www.xome.com/{item['href']}"
            break

    if dir_status == 1:
        compare_text1 = f"{buildingNum} {direction[0]} {' '.join(map(str,street))} {' '.join(map(str,city))} {state} {zip}"
        compare_text2 = f"{buildingNum} {' '.join(map(str,street))} {direction[0]} {' '.join(map(str,city))} {state} {zip}"
    else:
        compare_text1 = compare_text2 = original_address.upper()
    if (new_url != 0):

        html_text = requests.get(new_url, verify=False).text
        soup = BeautifulSoup(html_text, 'html.parser')

        new_table = soup.find('table', id="Master_Properties")
        if new_table == None:
            print("XOME:Not found")
            return
        new_table.find_all('tr')

        search_table = new_table.find_all('td')
        for item in search_table:

            if (item.text[1:-1].upper() == compare_text1 or item.text[1:-1].upper() == compare_text2):
                status = 1
                final_url = f"https://www.xome.com/{item.find('a')['href']}"
                break

        if (status == 0):
            print("XOME:Not found")
            return

        else:
            html_text = requests.get(final_url, verify=False).text
            soup = BeautifulSoup(html_text, 'html.parser')
            cards = soup.find_all('div', class_="detail-item")
            for card in cards:
                if card.find('div', class_="col detail-label").text == "Year Built":
                    year_const = card.find(
                        'div', class_='col detail-value').text
                    if year_const == "" or year_const == 0:
                        year_const = "Not found"
                    print(
                        f"XOME: {year_const}")
                    return
    else:
        print("XOME:Not found")
        return
