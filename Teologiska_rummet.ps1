# Teologiska rummet i P1 (http://sverigesradio.se/sida/avsnitt/893626?programid=3109) 
# diskuterar Storinkvisitorn (en liten berättelse insprängd i Dostojevskij
# mastodont verk Bröderna Karamazov). Romanen är den troende Dostojevskijs uppgörelse 
# med kristendomen. 

# Man kan väl säga att Dostojevskij själv pendlar mellan å ena sidan att Gud finns 
# och å andra sidan att Gud inte finns. Den fundamentala frågan är väl om livet är 
# meningsfullt, rättvist och gott?

# Berättelsens teman
[array]$Teman = ('Religionskritik', 'Människans frihet', 'Människans ondska', 'Guds likgiltighet (tystnad)',
'Kyrkans roll som en auktoritet när det gäller att lära känna Gud')

Write-Host "Berättelsen Storinkvisitorn"
Write-Host "Ett av berättelsens teman är..." 
Get-Random $Teman -OutVariable NewVar

if ($NewVar -contains 'Guds likgiltighet (tystnad)') {
Write-Host 'Kanske det stakaste argumentet mot Guds existens'
}
else {
break
}