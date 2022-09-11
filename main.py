from audioop import add
from selenium_scraping import neighbour_construction, spokeo_construction, been_verified
from ownerly import ownerlyConstruction
from xome import xomeConstruction


def init():
    print("\n\tYEAR BUILT BOT")
    print("-----------------------------------------------------------------------\n")
    input_address = input('Enter the address :').upper().replace(",", "")
    addressList = input_address.split()

    if (addressList[-1] == "STATES" and addressList[-2] == "UNITED"):
        addressList.remove("STATES")
        addressList.remove("UNITED")

    if addressList[-1] == "USA":
        addressList.remove("USA")
    original_list = input_address[:]
    direction = ["", ""]
    cityInput = input('Enter city name:').upper().split(" ")

    if "CO" in cityInput:
        cityInput.remove("CO")
        addressList.remove("CO")
    cityCount = len(cityInput)
    ignore_list = ["N", "S", "W", "E", "NE", "NW", "SE", "SW"]
    dir_status = 0
    count = 0
    for component in addressList:
        if component in ignore_list:
            direction[0] = component
            direction[1] = count
            dir_status = 1
            addressList.remove(component)
        count = count+1

    street = addressList[1:-3-(cityCount-1)]

    zip = addressList[-1]
    buildingNum = addressList[0]
    state = addressList[-2]

    city = addressList[-3-(cityCount-1):-2]

    print("-----------------------------------------------------------------------\n")
    
    ownerlyConstruction(state, city, street, buildingNum,
                        direction, dir_status)
    neighbour_construction(state, street, city,
                           buildingNum, direction, dir_status)
    spokeo_construction(state, street, city, buildingNum,
                        direction, dir_status)
    been_verified(state, street, city, buildingNum,
                  direction, dir_status)
    xomeConstruction(state, city, street, buildingNum,
                     zip, original_list, dir_status, direction)
    print("\n-----------------------------------------------------------------------\n")


while True:

    init()
    print("-----------------------------------------------------------------------\n")
