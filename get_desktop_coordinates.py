import pyautogui as pg
import sys

"""
找到鼠标位置
"""
def get_location():
    try:

        while True:
            x, y = pg.position()
            position_str = "x:" + str(x).rjust(4) + "---y:" + str(y).rjust(4)
            print(position_str, end="")
            print("\b" * len(position_str), end="", flush=True)
    except KeyboardInterrupt:
        print("finish by Ctrl + c")

def test(a):
    a.append(3)
    a.append(3)
    a.append(3)
    a.append(3)

a = []
test(a)
print(a)