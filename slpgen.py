"""
slpgen.py, version 0.4
(C) 2023 Stefan Blecko

Genererar spelledarpersoner till Drakar & Demoner

Ex:
python .\slpgen.py Troll 3 # genererar 3 troll
Troll 1  STY 16  STO 16  FYS 13  SMI 6  INT 11  PSY 12  KAR 4  SB 16  KP 14
Troll 2  STY 23  STO 10  FYS 8  SMI 17  INT 8  PSY 4  KAR 3  SB 16  KP 9
Troll 3  STY 17  STO 24  FYS 9  SMI 11  INT 7  PSY 17  KAR 1  SB 20  KP 16

python .\slpgen.py Skelett 349 # genererar 349 skelett
python .\slpgen.py -h # hjälp

Förklaring till förkortningarna: STYrka, STOrlek, FYSisk, SMIdighet,
INTelligens, PSYke, KARisma, SkadeBonus, KroppsPoäng.
"""

import random
import argparse
from colorama import Fore, Back, Style, init

init(autoreset=True)


class SkapaSLP(object):
    def __init__(self, sort, name, number):
        self.sort = sort
        self.name = name
        self.number = number

    def grundegenskaper(self):
        for x in range(1, self.number + 1):
            if self.sort == "Orch":
                O_monster_data = {
                    self.sort: x,
                    "STY": random.randint(4, 24),
                    "STO": random.randint(3, 18),
                    "FYS": random.randint(3, 18),
                    "SMI": random.randint(3, 18),
                    "INT": random.randint(2, 12) + 3,
                    "PSY": random.randint(3, 18),
                    "KAR": random.randint(2, 12),
                }
                O_monster_data["SB"] = round(
                    (O_monster_data["STY"] + O_monster_data["STO"]) / 2
                )
                O_monster_data["KP"] = round(
                    (O_monster_data["FYS"] + O_monster_data["STO"]) / 2
                )
                yield "\n"
                for k, v in O_monster_data.items():
                    yield ("{} {} ".format(k, v))
                yield "\n"

            elif self.sort == "Svartalf":
                S_monster_data = {
                    self.sort: x,
                    "STY": random.randint(2, 12) + 2,
                    "STO": random.randint(2, 8) + 2,
                    "FYS": random.randint(3, 18),
                    "SMI": random.randint(3, 18),
                    "INT": random.randint(2, 12) + 2,
                    "PSY": random.randint(3, 18),
                    "KAR": random.randint(2, 12),
                }
                S_monster_data["SB"] = round(
                    (S_monster_data["STY"] + S_monster_data["STO"]) / 2
                )
                S_monster_data["KP"] = round(
                    (S_monster_data["FYS"] + S_monster_data["STO"]) / 2
                )
                yield "\n"
                for k, v in S_monster_data.items():
                    yield "{} {} ".format(k, v)
                yield "\n"

            elif self.sort == "Troll":
                T_monster_data = {
                    self.sort: x,
                    "STY": random.randint(3, 18) + 6,
                    "STO": random.randint(3, 18) + 6,
                    "FYS": random.randint(2, 12) + 6,
                    "SMI": random.randint(3, 18),
                    "INT": random.randint(2, 12) + 3,
                    "PSY": random.randint(3, 18),
                    "KAR": random.randint(1, 4),
                }
                T_monster_data["SB"] = round(
                    (T_monster_data["STY"] + T_monster_data["STO"]) / 2
                )
                T_monster_data["KP"] = round(
                    (T_monster_data["FYS"] + T_monster_data["STO"]) / 2
                )
                yield "\n"
                for k, v in T_monster_data.items():
                    yield "{} {} ".format(k, v)
                yield "\n"

            elif self.sort == "Skelett":
                Sk_monster_data = {
                    self.sort: x,
                    "STY": round(random.randint(3, 18) / 2),
                    "STO": random.randint(3, 18),
                    "FYS": 0,
                    "SMI": random.randint(3, 18),
                    "INT": 0,
                    "PSY": 1,
                    "KAR": 0,
                }
                Sk_monster_data["SB"] = round(
                    (Sk_monster_data["STY"] + Sk_monster_data["STO"]) / 2
                )
                Sk_monster_data["KP"] = round(
                    (Sk_monster_data["FYS"] + Sk_monster_data["STO"]) / 2
                )
                yield "\n"
                for k, v in Sk_monster_data.items():
                    yield "{} {} ".format(k, v)
                yield "\n"

            elif self.sort == "Zombie":
                Z_monster_data = {
                    self.sort: x,
                    "STY": random.randint(3, 18) * 2,
                    "STO": random.randint(3, 18),
                    "FYS": 0,
                    "SMI": random.randint(3, 18),
                    "INT": 0,
                    "PSY": 1,
                    "KAR": 0,
                }
                Z_monster_data["SB"] = round(
                    (Z_monster_data["STY"] + Z_monster_data["STO"]) / 2
                )
                Z_monster_data["KP"] = round(
                    (Z_monster_data["FYS"] + Z_monster_data["STO"]) / 2
                )
                yield "\n"
                for k, v in Z_monster_data.items():
                    yield ("{} {} ".format(k, v))
                yield "\n"

            else:
                return None


def main():
    parser = argparse.ArgumentParser(
        prog="slpgen.py",
        description=f"{Fore.GREEN + Style.BRIGHT + Back.CYAN}Drakar och Demoner \
        SLP generator{Style.RESET_ALL}",
    )
    parser.add_argument(
        "ras", choices=["Orch", "Svartalf", "Troll", "Skelett", "Zombie"]
    )
    parser.add_argument("num", type=int)
    args = parser.parse_args()

    if args.ras == "Orch":
        o = SkapaSLP(sort="Orch", name="Orch", number=args.num)
        print(*o.grundegenskaper())
    elif args.ras == "Svartalf":
        s = SkapaSLP(sort="Svartalf", name="Svartalf", number=args.num)
        print(*s.grundegenskaper())
    elif args.ras == "Troll":
        t = SkapaSLP(sort="Troll", name="Troll", number=args.num)
        print(*t.grundegenskaper())
    elif args.ras == "Skelett":
        sk = SkapaSLP(sort="Skelett", name="Skelett", number=args.num)
        print(*sk.grundegenskaper())
    elif args.ras == "Zombie":
        z = SkapaSLP(sort="Zombie", name="Zombie", number=args.num)
        print(*z.grundegenskaper())
    else:
        pass


if __name__ == "__main__":
    main()
