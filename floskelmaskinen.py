#!/usr/bin/env python

"""
floskelmaskinen.py, version 0.21, (c) 2019, 2020 av Stefan Blecko

Ex:
python floskelmaskinen.py (skapar 1 floskel)
python floskelmaskinen.py --antal_floskler 43 (skapar 43 floskler)
"""

import random
import argparse
import time


def floskel():
    data1 = [
        "Sverigedemokrater",
        "Moderater",
        "Centerpartister",
        "Liberaler",
        "Kristdemokrater"]

    data2 = [
        "vill se tillväxten av",
        "vill ha",
        "skapar tillfällen för",
        "bekämpar utanförskapet genom",
        "sätter fokus på"]

    data3 = [
        "låga ingångslöner",
        "med våran svenska värdegrund",
        "möjligheten göra rätt för sig",
        "flera jobb",
        "att svenska värderingar ska råda i samhället",
        "sunda statsfinanser",
        "sänkta bidrag",
        "trygghetsskapande åtgärder",
        "fler poliser",
        "fler integrationsåtgärder",
        "segregationen",
        "fler småföretagare",
        "sänkta ingångslöner",
        "bidragsberoende",
        "en valfrihet för alla",
        "fler RUT tjänster",
        "fler entreprenörer i samhället",
        "flera enkla jobb",
        "frihetsreformer",
        "en valfrihetsrevolutionen",
        "ansvarstagande",
        "sätter arbetslinjen främst",
        "människor ska komma i arbete",
        "genom våran framtidsvision",
        "fokuserar på jobben, jobben, jobben"]

    return data1, data2, data3

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--antal_floskler", default=1)
    args = parser.parse_args()

    counter = 0
    while counter < int(args.antal_floskler):
        counter = counter + 1
        print("\nVi", random.choice(floskel()[0]), random.choice(floskel()[1]),
            random.choice(floskel()[2]), "samt", random.choice(floskel()[2]) + ".")
    time.sleep(10)

if __name__ == "__main__":
    main()
