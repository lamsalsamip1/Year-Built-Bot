from bs4 import BeautifulSoup
import requests


def xomeConstruction(state, city, street, buildingNum, zip):

    final_url = 0
    cityURL = '-'.join(map(str, city))
    url = f"https://www.xome.com/realestate/{state}/{cityURL}/{zip}/StreetList/"
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')

    table = soup.find('table', id="Master_dlStreet")
    streetList = table.find_all('a')
    compare_street = ' '.join(map(str, street))

    for item in streetList:
        item_list = item.text.split(' ')[-4::-1][::-1]
        new_item_list = ' '.join(map(str, item_list)).upper()
        if new_item_list in compare_street:
            new_url = f"https://www.xome.com/{item['href']}"
            break

    if (new_url):
        html_text = requests.get(new_url).text
        soup = BeautifulSoup(html_text, 'html.parser')
        new_table = soup.find('table', id="Master_Properties")
        new_table.find_all('tr')
        search_table = new_table.find_all('td')
        for item in search_table:
            compare_building = item.text.split(' ')[0][1:]
            if (compare_building == buildingNum):
                final_url = f"https://www.xome.com/{item.find('a')['href']}"
                break

    if final_url != 0:
        html_text = requests.get(final_url).text
        soup = BeautifulSoup(html_text, 'html.parser')
        cards = soup.find_all('div', class_="detail-item")
        for card in cards:
            if card.find('div', class_="col detail-label").text == "Year Built":
                print(
                    f"XOME: {card.find('div',class_='col detail-value').text}")
                return

    print("XOME:Not found")
