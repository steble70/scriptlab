#!/usr/bin/python
# argumentationsfel.py
# (C) 2022 av Stefan Blecko. Version 0.3

# Nästa steg är att skriva om raderna 40-53 så att man kan spara flera textsjok
# efter varann (nu går det bara spara ett) i pickle formatet.
# defaultdata_argumentationsfel.data filen är förpreparerad och har flera textsjok
# sparade i pickle formatet. defaultdata_argumentationsfel.data fungerar som det är
# tänkt. För att köra skriptet:
# python.exe .\argumentationsfel.py
# python .\argumentationsfel.py --newdatafile
# python .\argumentationsfel.py --loaddatafile FILE

import datetime
from pathlib import Path
import argparse
import pickle
import random
import base64

homedir = Path().home()

def filenamedate():
    return str(datetime.date.today())

def decodeb64file(d):
    return base64.b64decode(d).decode('utf-8', 'ignore')

def encodeb64file(e):
    list2string_encode_utf8 = e.encode('utf-8')
    return base64.b64encode(list2string_encode_utf8)

def main():
    parser = argparse.ArgumentParser(description='Argumentationsfel version 0.3')
    parser.add_argument("--newdatafile", help="to save, press Enter twice", action="store_true")
    parser.add_argument("--loaddatafile", type=str)
    args = parser.parse_args()

    if args.newdatafile:
        makenewpath = homedir.joinpath("datafile_" + filenamedate() + ".data")
        lines = []
        while True:
            l = input("> ")
            if l:
                lines.append(l)
            else:
                break
        list2string = "\n".join(lines)
        with open(homedir.joinpath(makenewpath), 'wb') as save_pickle:
            pickle.dump(encodeb64file(list2string), save_pickle)
            pickle.dump('\n', save_pickle)

        print(makenewpath.name, '[SPARAD]')

    elif args.loaddatafile:
        path2datafile = homedir.joinpath(args.loaddatafile)
        try:
            with open(homedir.joinpath(path2datafile), 'rb') as ldf:
                all_sentences = pickle.load(ldf)
                print(decodeb64file(all_sentences))
        except FileNotFoundError:
            print('Filen finns ej')

    else:
        try:
            with open(homedir.joinpath('defaultdata_argumentationsfel.data'), 'rb') as default_data:
                sentences = pickle.load(default_data)
                sentence = random.choice(sentences)
                print(decodeb64file(sentence))
        except FileNotFoundError:
            print('Hittade inte filen defaultdata_argumentationsfel.data')



if __name__ == "__main__":
    main()
