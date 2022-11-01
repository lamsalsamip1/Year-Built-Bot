from bs4 import BeautifulSoup
import requests


def ownerlyConstruction(state, city, street, buildingNum, direction, dir_status):

    requests.packages.urllib3.disable_warnings()
    cityURL = '-'.join(map(str, city))

    streetURL = '-'.join(map(str, street))

    url = f"https://www.ownerly.com/{state}/{cityURL}/{streetURL}-home-details".lower()

    i = 1
    page = ""
    while True:
        i = i+1
        new_url = f"{url}{page}"
        html_text = requests.get(new_url, verify=False).text
        soup = BeautifulSoup(html_text, 'html.parser')

        if dir_status == 1:
            compare_1 = f"{buildingNum} {' '.join(map(str,street))} {direction[0]}"
            compare_2 = f"{buildingNum} {direction[0]} {' '.join(map(str,street))}"
        else:
            compare_1 = f"{buildingNum} {' '.join(map(str,street))}"
            compare_2 = compare_1

        all_containers = soup.find_all('div', class_="card-container")
        result_code = check_year_construction(
            all_containers, compare_1, compare_2)
        status = 0
        if result_code == 0:
            arrows = soup.find_all('span', class_="pagination-arrow")
            if (len(arrows) > 0):
                for arrow in arrows:
                    arr_list = arrow.find_all('a')
                    if len(arr_list) > 0:
                        page = f"/page-{i}"
                        if arr_list[0]['href'] == f"{url}{page}":
                            status = 1
                            break
            else:
                print("OWNERLY\t\t: Not found")
                return
            if status == 1:
                continue
            else:
                print("OWNERLY\t\t: Not found")
                return

        elif result_code == 1:
            # No condstruction data
            print("OWNERLY\t\t: Not found")
            break
        elif result_code == 2:
            break


def check_year_construction(all_cards, compare_text_1, compare_text_2):

    for item in all_cards:
        item_card = (item.find('p', class_="card-street-address").text.lower())

        if (len(item['class'])) == 2:
            compare_card = item_card[1:-1]
        else:
            compare_card = item_card

        if compare_text_1.upper() == compare_card.upper() or compare_text_2.upper() == compare_card.upper():
            item_card_features = item.find_all('p')

            for feature in item_card_features:
                if ("Year Constructed: " in feature):
                    year_constructed = feature.find(
                        'span', class_="is-pulled-right").text
                    print("\nOWNERLY\t\t: "+year_constructed)
                    return 2
            return 1
    return 0
