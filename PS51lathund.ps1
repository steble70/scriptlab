<#
Lathund för PowerShell 5.1 noviser version 0.1
© 2018 av Stefan Blecko

Kopiera gärna innehållet i filen till C:\Users\[ditt användarnamn]\Documents\
WindowsPowerShell\Microsoft.PowerShell_profile.ps1 och testa och se vad som händer.
#>

$PSprojfoldername = "PSproj"
Set-Variable $HOME C:\Users\$env:USERNAME

Write-Host "Användare: $env:USERNAME | Projektmapp: $PSprojfoldername`n" -BackgroundColor DarkBlue

if (Test-Path -Path "C:\Users\$env:USERNAME\Desktop\$PSprojfoldername") {
}
else {
    New-Item -Path "C:\Users\$env:USERNAME\Desktop\" -Name $PSprojfoldername -ItemType "directory" | Out-Null
}
New-PSDrive -Name $PSprojfoldername -PSProvider FileSystem -Root "C:\Users\$env:USERNAME\Desktop\$PSprojfoldername" -Description "Välkommen till skript lådan." | Out-Null
Set-Location ($PSprojfoldername + ":")
Write-Host "PÅGÅENDE POWERSHELL PROJEKT" -ForegroundColor White -BackgroundColor Black
Get-ChildItem *.ps1 | Select-Object Name, LastWriteTime | Sort-Object LastWriteTime -Descending | Out-Host
Write-Host "KONSOLFÖNSTRETS KORTKOMMANDON" -ForegroundColor White -BackgroundColor Black
Get-PSReadlineKeyHandler -Bound | Select-Object Function, Key | Where-Object {$_.Function -notmatch "DigitArgument"}
