#!/usr/bin/env python
'''
pyVirus.py av Stefan Blecko. Version 0.1 2019

Skriptet genererar, slumpmässigt och automatiskt x antal textfiler
med slumpmässigt innehåll på hårddisken. Man kan själv definiera
hur många skräpfiler som ska skapas genom att skriva (från PowerShell):
python .\pyVirus.py (skapar en fil)
python .\pyVirus.py --files 340 (skapar 340 filer)
python .\pyVirus.py --files 1000000 (skapar EN MILJON filer)
python .\pyVirus.py -h (visar hjälp)

Vill man dölja källkoden kan man skapa en sk "compiled Python file".
Starta python.exe/ipython.exe och skriv:

import py_compile
py_compile.compile('pyVirus.py', optimize=-1)

Vill man hellre skapa en .exe fil av skriptet så kan man göra så här
(från PowerShell):

pip install pyinstaller
pyinstaller --onefile .\pyVirus.py
'''

import random
import argparse


def file_gen():
    return str(random.random())[2:] + '.txt'

def special_char_func():
    special_char = ['+', '-', '×', '÷', '%', '‰', '(', ')', '±', '≡', '=', '≈',
                    '<', '>', '≥', '≤', '√', 'ⁿ', '¹', '²', '³', 'π', '°', '#',
                    '∞', 'µ', 'Σ', '∩', '⌠', '⌡']
    return random.choice(special_char)

def myst_message_func():
    message = "i can feel something wonderful is happening i'm alive"
    return message

def junk_in_file_gen():
    a_list_with_special_char = []
    for spch in range(1, 2500):
        a_list_with_special_char.append(special_char_func())
    a_list_with_special_char.append(myst_message_func())
    random.shuffle(a_list_with_special_char)
    return a_list_with_special_char

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', default=1, help='number of files')
    args = parser.parse_args()

    for n in range(0, int(args.files)):
        with open(file_gen(), 'x', encoding='UTF-8') as f:
            for item in junk_in_file_gen():
                f.write("".join(item))
            f.close()

if __name__ == "__main__":
    main()
