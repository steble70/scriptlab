# ccprep.py 0.2.1
# © Stefan Blecko 2025

import json
import random
import os


def az900_glossary(fpath='AZ-900_glossary.json'):
    """
    Laddar in en JSON formaterad, AZ-900 ordlista som
    jag skapade i CoPilot.

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
    print(f'\nAZ-900 - TEST YOUR KNOWLEDGE\n') 
    print(f'What is "{az900_glossary()[0]}"?\n\n')

    unique_results = set()
    while True:
        if len(unique_results) != 5: 
            result = az900_glossary()[1]
            unique_results.add(result)
        else:
            break
    print(*unique_results, sep='\n')

if __name__ == "__main__":
    main()
