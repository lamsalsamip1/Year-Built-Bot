import pyautogui
import os
import time
import windowsapps
import psutil
import time
import win32process
import win32gui
import psutil
import win32process
import win32gui
import time


def active_window_process_name():
    # This produces a list of PIDs active window relates to
    pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    # pid[-1] is the most likely to survive last longer
    return psutil.Process(pid[-1]).name()


def move_active():
    keys = ['tab']
    while True:

        if (active_window_process_name() == "googleearth.exe"):
            return
        else:
            with pyautogui.hold('alt'):
                pyautogui.press(keys)
                pyautogui.press('enter')
            keys.append('tab')


def google_earth(address):

    if "googleearth.exe" in (i.name() for i in psutil.process_iter()):
        move_active()
        # print(active_window_process_name())
    else:
        if windowsapps.find_app('Google Earth Pro'):
            windowsapps.open_app('Google Earth Pro')
            time.sleep(7)

        else:
            print("Google Earth not found")
            return

    screenWidth, screenHeight = pyautogui.size()
    # print(f"{screenHeight} X {screenWidth}")

    typeX = (40/1080)*screenHeight
    typeY = (96/1920)*screenWidth

    # currentMouseX, currentMouseY = pyautogui.position()
    # print(f"{currentMouseX} X {currentMouseY} Y")

    response = os.startfile("earth.lnk")

    pyautogui.moveTo(typeX, typeY)
    pyautogui.click()
    with pyautogui.hold('ctrl'):
        pyautogui.press('a')
    pyautogui.press('del')

    pyautogui.write(address, interval=0.01)
    pyautogui.press('enter')
