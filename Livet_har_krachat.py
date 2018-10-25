#!/usr/bin/env python
# "Arv och Miljö" version 0.1 av Stefan Blecko

# Här importerar man pythons olika funktioner
import sys
import random
import time
import collections 

# Default värde på en skala 1-20 är 10 man kan säga att 10 motsvarar 50%, alltså normalbegåvad.
def livet(socioekonomiska_faktorer=10, IQ=10):
    '''
    Programmet (livet) kraschar emellanåt. Ju högre värde man har på
    socioekonomiska_faktorer och IQ (man kan bara ha max 20 i värde) dessto
    större chans att programmet (livet) I N T E kraschar så ofta.
    '''
    hur_bra_du_klarar_livet = (socioekonomiska_faktorer + IQ)//2 # Ett medelvärde.
    krasch = collections.Counter() # Krasch är en räknare.


    print('Programmet "Arv och Miljö" körs nu...')
    print('')
    

    year = 0
    
    while year < 10: # Hur mycket lidande man får uppleva under 10 år kan man säga.
        time_to_next_impact = random.randint(1,10) # Hur många år tar tar mellan varje livskris.
        slumpens_utfall = random.randint(1,20) # Slump funktionen i python (random).
        year = year + 1
         
        
        # Om slumpens_utfall är mindre än hur_bra_du_klarar_livet har du klarat dig ett tag.
        if slumpens_utfall > hur_bra_du_klarar_livet:

            # Här har Om slumpens_utfall blivit större.
            starta_om_livet = input('Livet har kraschat. Vad gör du nu? Orkar du Börja om på nytt (j/n)?: ')
            if starta_om_livet == 'j':
                for antalet_j in starta_om_livet:
                    krasch[antalet_j] += 1 # +1 för varje gång loopen körs.
                
                print('')
                print('Livet forsätter som vanligt...')
                print('')
                time.sleep(time_to_next_impact)
            elif starta_om_livet == 'n': # Livet är bara skit.
                print('Livet är slut. Livet blev inte som det var tänkt att bli. Det blev någonting annat.')
                break
            else:
                print('Fel input (j/n)! Starta om programmet.')
                sys.exit()
                

                
        else:
            print('')
            print('Livet har ännu inte kraschat...')
            print('')
            time.sleep(time_to_next_impact)

                          
    
    print('')
    print('Livet kraschade', sum(krasch.values()), 'gånger under en 10-års period.')
    print('Det är bara att hacka i sig.')

    return
