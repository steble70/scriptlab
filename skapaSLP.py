#!/usr/bin/env python

'''
skapaSLP.py 
Version 0.1
(C) 2020 av Stefan Blecko
'''

import random


class SkapaSLP(object):
    '''Genererar (S)pel (L)edar (P)ersoner till Drakar & Demoner
    Förklaring till förkortningarna:
    STYrka, STOrlek, FYSisk, SMIdighet, INTelligens, PSYke, KARisma
    '''

    def __init__(self, ras='Orch', namn='?', antal=1):
        self.ras = ras
        self.namn = namn
        self.antal = antal

    def grundegenskaper(self):
        for x in range(1, self.antal+1):
            if self.ras == 'Orch':
                O_monster_data = {'STY': random.randint(4, 24), 'STO': random.randint(3, 18),
                                  'FYS': random.randint(3, 18), 'SMI': random.randint(3, 18),
                                  'INT': random.randint(2, 12)+3, 'PSY': random.randint(3, 18),
                                  'KAR': random.randint(2, 12)}
                O_monster_data['SB'] = round((O_monster_data['STY'] + O_monster_data['STO'])/2)
                O_monster_data['KP'] = round((O_monster_data['FYS'] + O_monster_data['STO'])/2)
                yield '{} {}'.format(O_monster_data, '\n')

            elif self.ras == 'Svartalf':
                S_monster_data = {'STY': random.randint(2, 12)+2, 'STO': random.randint(2, 8)+2,
                                  'FYS': random.randint(3, 18), 'SMI': random.randint(3, 18),
                                  'INT': random.randint(2, 12)+2, 'PSY': random.randint(3, 18),
                                  'KAR': random.randint(2, 12)}
                S_monster_data['SB']=round((S_monster_data['STY'] + S_monster_data['STO'])/2)
                S_monster_data['KP']=round((S_monster_data['FYS'] + S_monster_data['STO'])/2)
                yield '{} {}'.format(S_monster_data, '\n')

            elif self.ras == 'Troll':
                T_monster_data = {'STY': random.randint(3, 18)+6, 'STO': random.randint(3, 18)+6,
                                  'FYS': random.randint(2, 12)+6, 'SMI': random.randint(3, 18),
                                  'INT': random.randint(2, 12)+3, 'PSY': random.randint(3, 18),
                                  'KAR': random.randint(1, 4)}
                T_monster_data['SB']=round((T_monster_data['STY'] + T_monster_data['STO'])/2)
                T_monster_data['KP']=round((T_monster_data['FYS'] + T_monster_data['STO'])/2)
                yield '{} {}'.format(T_monster_data, '\n')

            elif self.ras == 'Skelett':
                Sk_monster_data={'STY': round(random.randint(3, 18)/2), 'STO': random.randint(3, 18),
                                 'FYS': 0, 'SMI': random.randint(3, 18), 'INT': 0, 'PSY': 1, 'KAR': 0}
                Sk_monster_data['SB']=round((Sk_monster_data['STY'] + Sk_monster_data['STO'])/2)
                Sk_monster_data['KP']=round((Sk_monster_data['FYS'] + Sk_monster_data['STO'])/2)
                yield '{} {}'.format(Sk_monster_data, '\n')

            elif self.ras == 'Zombie':
                Z_monster_data={'STY': random.randint(3, 18)*2, 'STO': random.randint(3, 18),
                                'FYS': 0, 'SMI': random.randint(3, 18), 'INT': 0, 'PSY': 1,
                                'KAR': 0}
                Z_monster_data['SB']=round((Z_monster_data['STY'] + Z_monster_data['STO'])/2)
                Z_monster_data['KP']=round((Z_monster_data['FYS'] + Z_monster_data['STO'])/2)
                yield '{} {}'.format(Z_monster_data, '\n')

            else:
                pass

def main():
    Orch = SkapaSLP(antal=10)
    print('Orcher\n', *Orch.grundegenskaper())

    Svartalf = SkapaSLP(ras='Svartalf', antal=4)
    print('Svartalfer\n', *Svartalf.grundegenskaper())

    Troll = SkapaSLP(ras='Troll', antal=2)
    print('Troll\n', *Troll.grundegenskaper())

    Vegas_gam = SkapaSLP(ras='Vegas gam', antal=3)
    print('Vegas gam\n', *Vegas_gam.grundegenskaper())

    Skelett = SkapaSLP(ras='Skelett', antal=2)
    print('Skelett\n', *Skelett.grundegenskaper())


if __name__ == "__main__":
    main()
