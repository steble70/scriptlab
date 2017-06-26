import random
dice1 = random.randint(3,18) + 10
dice2 = random.randint(3,18) + 8
dice3 = random.randint(3,18) + 5
dice6 = random.randint(3,18)
dice7 = random.randint(3,18) + 10
Stefan_barbaren = {'STO':dice1, 'STY':dice2, 'FYS':dice3, 'SMI':0,
                   'INT':0, 'PSY':0}
print('Stefan, barbarens grundegenskaper: ')
print('STO:',Stefan_barbaren['STO'])
print('STY:',Stefan_barbaren['STY'])
print('FYS:',Stefan_barbaren['FYS'])
print()
print('Färdigheter: ')
Stefan_barbaren['Finna dolda ting'] = dice6
Stefan_barbaren['Slåss med Arbetsförmedlingen'] = dice7
print('Finna dolda ting:',Stefan_barbaren['Finna dolda ting'])
print('Slåss med Arbetsförmedlingen:', Stefan_barbaren['Slåss med Arbetsförmedlingen'])
print('The End')
