from selenium_scraping import neighbour_construction, spokeo_construction
from ownerly import ownerlyConstruction
from xome import xomeConstruction


def init():
    print("\n\tYEAR BUILT BOT")
    print("-----------------------------------------------------------------------\n")
    addressList = input('Enter the address :').upper().split(" ")
    direction = [""]
    cityInput = input('Enter city name:').upper().split(" ")
    cityCount = len(cityInput)
    ignore_list = ["N", "S", "W", "E", "NE", "NW", "SE", "SW", "CO"]
    dir_status = 0
    for component in addressList:
        if component in ignore_list:
            if component != "CO":
                direction[0] = component
                dir_status = 1
            addressList.remove(component)
    zip = addressList[-1]
    buildingNum = addressList[0]
    state = addressList[-2]

    city = addressList[-3-(cityCount-1):-2]
    street = addressList[1:-3-(cityCount-1)]

    print("-----------------------------------------------------------------------\n")
    ownerlyConstruction(state, city, street, buildingNum,
                        direction, dir_status)
    neighbour_construction(state, street, city,
                           buildingNum, direction, dir_status)
    spokeo_construction(state, street, city, buildingNum,
                        direction, dir_status)
    xomeConstruction(state, city, street, buildingNum, zip)
    print("\n-----------------------------------------------------------------------\n")


while True:
    init()
    print("-----------------------------------------------------------------------\n")
