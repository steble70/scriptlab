"""
slpgen.py, version 0.7 (OOP-version)
Genererar spelledarpersoner till Drakar & Demoner
"""

import random
import argparse
from colorama import Fore, Back, Style, init

# Initiera colorama för färgstöd i terminalen
init(autoreset=True)

class NPC:
    """
    Representerar en enskild spelledarperson (SLP) och dess egenskaper.
    """
    def __init__(self, race, index):
        self.race = race
        self.index = index
        self.attributes = self._roll_attributes()
        self._calculate_secondary_stats()

    def _roll_attributes(self):
        """
        Slår fram grundegenskaper baserat på varelsetyp.
        """
        if self.race == "Orch":
            return {
                "STY": random.randint(4, 24),
                "STO": random.randint(3, 18),
                "FYS": random.randint(3, 18),
                "SMI": random.randint(3, 18),
                "INT": random.randint(2, 12) + 3,
                "PSY": random.randint(3, 18),
                "KAR": random.randint(2, 12),
            }
        elif self.race == "Svartalf":
            return {
                "STY": random.randint(2, 12) + 2,
                "STO": random.randint(2, 8) + 2,
                "FYS": random.randint(3, 18),
                "SMI": random.randint(3, 18),
                "INT": random.randint(2, 12) + 2,
                "PSY": random.randint(3, 18),
                "KAR": random.randint(2, 12),
            }
        elif self.race == "Troll":
            return {
                "STY": random.randint(3, 18) + 6,
                "STO": random.randint(3, 18) + 6,
                "FYS": random.randint(2, 12) + 6,
                "SMI": random.randint(3, 18),
                "INT": random.randint(2, 12) + 3,
                "PSY": random.randint(3, 18),
                "KAR": random.randint(1, 4),
            }
        elif self.race == "Skelett":
            return {
                "STY": round(random.randint(3, 18) / 2),
                "STO": random.randint(3, 18),
                "FYS": 0,
                "SMI": random.randint(3, 18),
                "INT": 0,
                "PSY": 1,
                "KAR": 0,
            }
        elif self.race == "Zombie":
            return {
                "STY": random.randint(3, 18) * 2,
                "STO": random.randint(3, 18),
                "FYS": 0,
                "SMI": random.randint(3, 18),
                "INT": 0,
                "PSY": 1,
                "KAR": 0,
            }
        return {}

    def _calculate_secondary_stats(self):
        """
        Beräknar Skadebonus (SB) och Kroppspoäng (KP).
        """
        self.attributes["SB"] = round((self.attributes["STY"] + self.attributes["STO"]) / 2)
        self.attributes["KP"] = round((self.attributes["FYS"] + self.attributes["STO"]) / 2)

    def __str__(self):
        """
        Returnerar en snyggt formaterad strängrepresentation av varelsen.
        """
        prefix = f"{self.race} {self.index:<2} "
        attr_string = "  ".join([f"{k} {v}" for k, v in self.attributes.items()])
        return prefix + attr_string


class NPCGenerator:
    """
    Hanterar generering och utskrift av grupper av SLP:er.
    """
    def __init__(self, race, count):
        self.race = race
        self.count = count

    def generate_and_print(self):
        """
        Skapar och skriver ut det antal SLP:er som angetts.
        """
        for i in range(1, self.count + 1):
            npc = NPC(self.race, i)
            print(npc)


def main():
    # Konfigurera argumenthanteraren
    description_text = f"{Fore.GREEN + Style.BRIGHT + Back.CYAN}Drakar och Demoner SLP-generator (OOP){Style.RESET_ALL}"
    parser = argparse.ArgumentParser(prog="slpgen.py", description=description_text)
    
    available_races = ["Orch", "Svartalf", "Troll", "Skelett", "Zombie"]
    
    parser.add_argument("ras", choices=available_races, help="Vilken ras som ska genereras")
    parser.add_argument("num", type=int, help="Antal varelser som ska skapas")
    
    args = parser.parse_args()

    # Skapa en generator och kör igång processen
    generator = NPCGenerator(args.ras, args.num)
    generator.generate_and_print()


if __name__ == "__main__":
    main()
