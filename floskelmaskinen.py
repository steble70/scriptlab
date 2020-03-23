#!/usr/bin/env python
# floskelmaskinen.py, version 0.2, (c) 2019, 2020 av Stefan Blecko

import random
import argparse

def floskel():
    subjekt = ['Sverigedemokrater', 'Moderater', 'Centernpartister', 'Liberaler',
               'Kristdemokrater']

    predikat = ['vill se tillväxten av', 'vill ha fler', 'skapar tillfällen för',
                'bekämpar utanförskapet genom','sätter focus på']
                     
    objekt = ['låga ingångslöner', 'arbetslinjen','värdegrunder', 'att göra rätt för sig',
              'flera jobb', 'svenska värderingar', 'ansvar', 'sänkta bidrag', 'trygghet',
              'fler poliser', 'integration', 'segregationen', 'småföretagande',
              'sänkta ingångslöner', 'bidragsberoende', 'en valfrihet för alla',
              'att ha mera RUT', 'entreprenörer', 'flera enkla jobb',
              'friheten främst','en valfrihetsrevolutionen', 'ansvar först','arbeten',
              'människor', 'i framtiden', 'landet']                 

    return subjekt, predikat, objekt


def main():
    '''
    Ex:
    python floskelmaskinen.py (skapar 1 floskel)
    python floskelmaskinen.py --antal_floskler 43 (skapar 43 floskler)
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--antal_floskler', default=1)
    args = parser.parse_args()

    counter = 0
    while counter < int(args.antal_floskler):
        counter = counter + 1
        print('Vi', random.choice(floskel()[0]), random.choice(floskel()[1]), 
              random.choice(floskel()[2]), 'och', random.choice(floskel()[2]) + '.')

if __name__ == "__main__":
    main()
