#!/usr/bin/env python
# coding: utf-8

# klass_test.py
# version 0.1
# (C) 2020 av Stefan

import random

class SLP(object):
    '''Genererar (S)pel(L)edar(P)ersoner till Drakar & Demoner
       Copyright Stefan 2020
    '''

    def __init__(self, ras='Orch', namn='', antal=1):
        self.ras = ras
        self.namn = namn
        self.antal = antal+1
        
    def grundegenskaper(self):
        if self.ras == 'Orch':
            O_monster_data = {'STY': random.randint(4, 24), 'STO': random.randint(3, 18),
                              'FYS': random.randint(3, 18), 'SMI': random.randint(3, 18),
                              'INT': random.randint(2, 12)+3, 'PSY': random.randint(3, 18),
                              'KAR': random.randint(2, 12)}
            O_monster_data['SB'] = round((O_monster_data['STY'] + O_monster_data['STO'])/2)
            O_monster_data['KP'] = round((O_monster_data['FYS'] + O_monster_data['STO'])/2)
            return O_monster_data

        elif self.ras == 'Svartalf':
            S_monster_data = {'STY': random.randint(2, 12)+2, 'STO': random.randint(2, 8)+2,
                              'FYS': random.randint(3, 18), 'SMI': random.randint(3, 18),
                              'INT': random.randint(2, 12)+2, 'PSY': random.randint(3, 18),
                              'KAR': random.randint(2, 12)}
            S_monster_data['SB'] = round((S_monster_data['STY'] + S_monster_data['STO'])/2)
            S_monster_data['KP'] = round((S_monster_data['FYS'] + S_monster_data['STO'])/2)
            return S_monster_data
        
        elif self.ras == 'Troll':
            T_monster_data = {'STY': random.randint(3, 18)+6, 'STO': random.randint(3, 18)+6,
                              'FYS': random.randint(2, 12)+6, 'SMI': random.randint(3, 18),
                              'INT': random.randint(2, 12)+3, 'PSY': random.randint(3, 18),
                              'KAR': random.randint(1, 4)}
            T_monster_data['SB'] = round((T_monster_data['STY'] + T_monster_data['STO'])/2)
            T_monster_data['KP'] = round((T_monster_data['FYS'] + T_monster_data['STO'])/2)
            return T_monster_data
        

        elif self.ras == 'Skelett':
            Sk_monster_data = {'STY': round(random.randint(3, 18)/2), 'STO': random.randint(3, 18),
                               'FYS': 0, 'SMI': random.randint(3, 18), 'INT': 0, 'PSY': 1, 'KAR': 0}
            Sk_monster_data['SB'] = round((Sk_monster_data['STY'] + Sk_monster_data['STO'])/2)
            Sk_monster_data['KP'] = round((Sk_monster_data['FYS'] + Sk_monster_data['STO'])/2)
            return Sk_monster_data
            
        
        elif self.ras == 'Zombie':
            Z_monster_data = {'STY': random.randint(3, 18)*2, 'STO': random.randint(3, 18),
                              'FYS': 0, 'SMI': random.randint(3, 18), 'INT': 0, 'PSY': 1,
                              'KAR': 0}
            Z_monster_data['SB'] = round((Z_monster_data['STY'] + Z_monster_data['STO'])/2)
            Z_monster_data['KP'] = round((Z_monster_data['FYS'] + Z_monster_data['STO'])/2)
            return Z_monster_data

        else: 
            return None

