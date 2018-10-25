<#
PS51lathund.ps1 

Lathund f�r PowerShell 5.1 noviser version 0.1
� 2018 av Stefan Blecko

Kopiera g�rna inneh�llet i filen till C:\Users\[ditt anv�ndarnamn]\Documents\
WindowsPowerShell\Microsoft.PowerShell_profile.ps1 och testa och se vad som h�nder.
#>

$PSprojfoldername = "PSproj"
Set-Variable $HOME C:\Users\$env:USERNAME

Write-Host "Anv�ndare: $env:USERNAME | Projektmapp: $PSprojfoldername`n" -BackgroundColor DarkBlue

if (Test-Path -Path "C:\Users\$env:USERNAME\Desktop\$PSprojfoldername") {
}
else {
    New-Item -Path "C:\Users\$env:USERNAME\Desktop\" -Name $PSprojfoldername -ItemType "directory" | Out-Null
}
New-PSDrive -Name $PSprojfoldername -PSProvider FileSystem -Root "C:\Users\$env:USERNAME\Desktop\$PSprojfoldername" -Description "V�lkommen till skript l�dan." | Out-Null
Set-Location ($PSprojfoldername + ":")
Write-Host "P�G�ENDE POWERSHELL PROJEKT`n" -ForegroundColor White -BackgroundColor Black
Get-ChildItem -Name *.ps1
Write-Host " " 
Write-Host "KONSOLF�NSTRETS KORTKOMMANDON" -ForegroundColor White -BackgroundColor Black
Get-PSReadlineKeyHandler -Bound | Select-Object Function, Key | Where-Object {$_.Function -notmatch "DigitArgument"}
