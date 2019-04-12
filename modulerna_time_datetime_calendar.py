#!/usr/bin/python
#(C) 2018 av Stefan Blecko. Version 0.1

import time, datetime, calendar


def dateNow():  
    currentYear = datetime.date.today().strftime("%Y")
    currentMonth = datetime.date.today().strftime("%m")
    temporary_cal = calendar.monthcalendar(int(currentYear), int(currentMonth))
    final_cal = [j for i in temporary_cal for j in i]
    while 0 in final_cal: final_cal.remove(0)
    
    return final_cal
    

def unemployed():
    final_cal_for_loop = dateNow()
    
    print('Den arbetslöses Sisyfos sten. Version 0.1 (C) 2018 av Stefan')
    print()
    
    while True: # <-- En evighetsloop som inte leder någonstans. Allt skit sker inuti "while True" loopen.
        for x in final_cal_for_loop:
            time.sleep(1) # Väntar 1 sek. innan nästa frammatning.
            if x==1:
                print('Dag nr', x, 'aktivitetsrapportera till Arbetsförmedlingen.')
            elif x==26:
                print('Dag nr', x, 'utbetalning av lilla bidraget från Försäkringskassan.')
            elif x==27:
                print('Dag nr', x, 'betala räkningar.')
            elif x==28:
                print('Dag nr', x, 'tomt på kontot igen.')
            else:
                print('Dag nr', x, 'söka jobb, och förtvivla.')
        
        print('...och så här fortsätter det månad efter månad, år efter år.')
        print()


def main():
    unemployed()


main()
