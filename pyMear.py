#!/usr/bin/env python

"""
pyMear.py - Träna huvudräkning med Python
Version 0.1 (C) 2019 av Stefan Blecko

Första försöket att göra någonting med matematik med Python.
Skripet funkar visserligen, men är kanske inte den bästa
implementeringen.
"""

import random
import time


def num_selection():
    eighty_procent = random.randint(3, 10)
    twenty_procent = random.randint(0, 2)
    selection = [eighty_procent, eighty_procent, eighty_procent, eighty_procent,
                 eighty_procent, eighty_procent, eighty_procent, eighty_procent,
                 twenty_procent, twenty_procent]
    return random.choice(selection)

def num1():
    return str(num_selection())

def num2():
    return str(num_selection())

def operator():
    group1 = random.choice(['+', '-', '/'])
    group2 = '*'
    group1_and_group2 = [group1, group2]
    return random.choice(group1_and_group2)

def simple_math():
    while True:
        try:
            o = num1() + str(operator()) + num2()
            r = eval(o)
            break
        except ZeroDivisionError:
            pass
    return dict({o: round(r, 2)})

def main():
    d = {}
    for item in range(1, random.randint(1, 10)):
        d.update(simple_math())

    for k, v in d.items():
        while True:
            try:
                user_input = float(input('\n{}='.format(k)))
                break
            except ValueError:
                pass
        if user_input == v:
            print('Rätt!')
        else:
            print('Fel!')

    print('\nVill man träna hjärnan ytterligare kan man göra det här: https://www.mensa.se/provtestet/test/')
    time.sleep(5)


if __name__ == "__main__":
    main()
