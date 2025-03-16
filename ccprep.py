# ccprep.py 0.2
# © Stefan Blecko 2025

import json
import random
import os


def az900_glossary(fpath='AZ-900_glossary.json'):
    """
    Laddar in en JSON-formaterad fil in i minnet.
    Returns: Tuple
    """
    os.chdir(os.environ['USERPROFILE'])
    # First i created a JSON formatted AZ-900 glossary
    # (AZ-900_glossary.json) using CoPilot.
    jsonfile = open(fpath)
    unformatted_json = json.load(jsonfile) # Loaded as a dict.
    show_key = random.choice(list(unformatted_json['Glossary'].keys()))
    show_value = random.choice(list(unformatted_json['Glossary'].values()))
    return show_key, show_value

def main():
    print(f'\nAZ-900 - TEST YOUR KNOWLEDGE\n\nWhat is "{az900_glossary()[0]}"?\n\n')

    unique_results = set()
    for item in range(1,6):
        result = az900_glossary()[1]
        unique_results.add(result) 
    
    print(*unique_results, sep='\n')
            
if __name__ == "__main__":
    main()



