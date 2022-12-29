![PowerShell-Python Logo](/Banner.jpg)


## **Välkommen till Scriptlab**
#### [Stefan Bleckos](https://twitter.com/minnesbilder) Python/PowerShell sajt 
##### Klicka gärna på länkarna ovan för titta närmare på källkoden.


### Python kompetenser
```python
secupass.py - Genererar "säkra" lösenord
Version 0.1 av Stefan Blecko
Spara skripet och skriv sen (från PowerShell): 
python .\secupass.py --num 5 (alltså 5 lösenord)
Outputen blir någonting liknade det här:
luwozA%2
xizakA/7
pefuqA$5
sOmute?2
jAhima$1
Skriver man istället (från PowerShell):
python .\secupass.py --num 19 --out mina_lösenord.txt 
så sparas 19 lösenord i en textfilen "mina_lösenord.txt" istället.
'''


import argparse
import random

def passwd():
    # LÖSENORDETS BESTÅNDSDELAR

    character_set = [['b', 'c', 'f', 'g', 'h', 'j', 'k', 'l',
                      'm', 'n', 'p', 'q', 's', 't', 'v', 'w',
                      'x', 'z'],
                     ['a', 'e', 'i', 'o', 'u', 'y'],
                     ['!', '@', '$', '%', '&', '/', '?', '*']]

    def category_1():
        return random.choice(character_set[0])

    def category_2():
        return random.choice(character_set[1])

    def category_4():
        return random.choice(character_set[2])

    def rd1():
        return random.randint(0, 9)
    rd2 = random.randint(0, 5)

    collect_all_character = []

    # BYGGER LÖSENORDET
    for n in range(1, 4):
        collect_all_character.append(category_1())
        collect_all_character.append(category_2())

    collect_all_character[rd2] = str(collect_all_character[rd2]).upper()
    collect_all_character.append(category_4())
    collect_all_character.append(rd1())

    return collect_all_character

def main():
    parser = argparse.ArgumentParser(
        epilog="Ahhh! Why should it be so booky to use argparse?")
    parser.add_argument('--num', type=int)
    parser.add_argument('--out', type=argparse.FileType('w'))
    args = parser.parse_args()

    if args.num and args.out:
        for n in range(0, args.num):
            for item in passwd():
                args.out.write(str(item))
            args.out.write('\n')
        args.out.close()    
    elif args.num:
        for n in range(0, args.num):
            print(*passwd(), sep='')         
    else:
        print('secupass.py: error: the following arguments are required: --num')


if __name__ == '__main__':
    main()
```

### PowerShell kompetenser
```powershell
function Get-ChangeLog {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory)]
        [string]$Project,
        [string]$Topic
    )
    process {
        if ($Topic) {
            $new_pscustobj = [PSCustomObject]@{
                'Datum'     = "$(Get-Date -Format FileDate)"
                'Changelog' = "$Topic"
            }
            $new_pscustobj | 
            Export-Csv "$HOME\Desktop\$PSprojfoldername\$Project\docs\changelog.csv" -Force -Append
        }
        else {
            if (Test-Path -Path "$HOME\Desktop\$PSprojfoldername\$Project\docs\changelog.csv") {
                Import-Csv -Path "$HOME\Desktop\$PSprojfoldername\$Project\docs\changelog.csv"
            }
            else {
                Write-Error "$HOME\Desktop\$PSprojfoldername\$Project\docs\changelog.csv måste skapas först."
            }
        }
    }
}
```
