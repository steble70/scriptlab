# ccprep.py 0.2.2
# © Stefan Blecko 2025

import json
import random
import os


def dp900_glossary(fpath='DP-900_glossary.json'):
    """
    Laddar in en JSON formaterad, DP-900 ordlista som
    jag skapade i Copilot.

    Args: fpath 
    Returns: Tuple
    """
    os.chdir(os.environ['USERPROFILE'])
    jsonfile = open(fpath)
    unformatted_json = json.load(jsonfile) # Laddas in som en dict.
    sk = random.choice(list(unformatted_json['Glossary'].keys()))
    sv = random.choice(list(unformatted_json['Glossary'].values()))
    return sk, sv

def main():
    print(f'\nDP-900 - TEST YOUR KNOWLEDGE\n') 
    print(f'What is "{dp900_glossary()[0]}"?\n\n')

    unique_results = set()
    while True:
        if len(unique_results) != 5: 
            result = dp900_glossary()[1]
            unique_results.add(result)
        else:
            break
    print(*unique_results, sep='\n')

if __name__ == "__main__":
    main()
