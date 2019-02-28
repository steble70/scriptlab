#!/usr/bin/env python
#Floskelmaskinen version 0.1b (c) 2019 av Stefan Blacko

import random

def Floskelmaskinen(How_many_empty_phrases = 1):
    '''
    Man kör programet genom att ange hur många floskler som ska genereras, tex
    Floskelmaskinen(10) = 10 floskler eller Floskelmaskinen(1322) = 1322 floskler.
    '''
    
    subjekt = ['Sverigedemokrater', 'Moderater', 'Centernpartister', 'Liberaler',
               'Kristdemokrater']

    predikat = ['vill se tillväxten av', 'vill ha fler', 'skapar tillfällen för',
                'bekämpar utanförskapet genom','sätter focus på']
                     

    objekt = ['låga ingångslöner', 'arbetslinjen','värdegrunder', 'att göra rätt för sig',
              'flera jobb', 'svenska värderingar', 'ansvar', 'sänkta bidrag', 'trygghet',
              'fler poliser', 'integration', 'segregationen', 'småföretagen',
              'sänkta ingångslöner', 'bidragsberoende', 'en valfrihet för alla',
              'att ha mera RUT', 'entreprenörer', 'flera enkla jobb',
              'friheten främst','en valfrihetsrevolutionen', 'ansvar först','arbeten',
              'människor', 'i framtiden', 'landet']                 

    counter = 0

    while counter < How_many_empty_phrases:
        counter = counter + 1
        print('Vi', random.choice(subjekt), random.choice(predikat), random.choice(objekt),
              'och', random.choice(objekt) + '.')


    
    
