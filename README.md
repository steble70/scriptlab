![PowerShell-Python Logo](/banner.jpg)


## Välkommen till Scriptlab
#### [Stefan Bleckos](https://twitter.com/minnesbilder) Python/PowerShell sajt 
##### Klicka gärna på länkarna ovan för titta närmare på källkoden.

```powershell
<#
Lathund för PowerShell 5.1 noviser version 0.1i
© 2018 av Stefan Blecko

Kopiera gärna innehållet i filen till C:\Users\[ditt användarnamn]\Documents\
WindowsPowerShell\Microsoft.PowerShell_profile.ps1.  
#>

$PSprojfoldername = "PSproj"
Set-Variable $HOME C:\Users\$env:USERNAME
Write-Host "Användare: $env:USERNAME | Projektmapp: $PSprojfoldername`n"`
-BackgroundColor DarkBlue

if (Test-Path -Path "C:\Users\$env:USERNAME\Desktop\$PSprojfoldername") {
}
else {
    New-Item -Path "C:\Users\$env:USERNAME\Desktop\" -Name $PSprojfoldername `
    -ItemType "directory" | Out-Null
    New-Item -Path "C:\Users\$env:USERNAME\Desktop\$PSprojfoldername\" -Name `
    "PSskript1.ps1" -ItemType "File" | Out-Null
}
New-PSDrive -Name $PSprojfoldername -PSProvider FileSystem -Root `
"C:\Users\$env:USERNAME\Desktop\$PSprojfoldername" -Description `
"Välkommen till skript lådan." | Out-Null 

Function Get-PSHelpMenu {
    Write-Host "`nMENY" -BackgroundColor Black -ForegroundColor White -NoNewline
    $showmenu = @{"Din skript mapp:" = "Get-PSproj"; "Konsol hjälp:" = 
    "Get-PSConHelp"; "Nytt Konsol fönster:" = "New-PSWin"; "Miljövariabler:" = "Get-PSEnv"; 
    "Reserverade ord:" = "Get-PSResWord"; "Automatiska variabler:" =
    "Get-PSAutoVar"}
    $showmenu | Format-Table -HideTableHeaders
}
Function Get-PSproj {
    Set-Location ($PSprojfoldername + ":")
    Write-Host "`nPÅGÅENDE POWERSHELL PROJEKT" -ForegroundColor White `
    -BackgroundColor Black -NoNewline
    
    Get-ChildItem *.ps1 | Select @{Name = "Skript"; Expression = {$_.Name}}, 
    @{Name = "Senast ändrad"; Expression = {$_.LastWriteTime}} | sort "Senast ändrad" `
    -Descending | Out-Host
}
Function Get-PSConHelp {
    Write-Host "`nPOWERSHELL KONSOL HJÄLP" -ForegroundColor White `
    -BackgroundColor Black -NoNewline
    Get-PSReadlineKeyHandler -Bound | Select Function, Key | ? {$_.Function `
    -notmatch "DigitArgument"} | Format-Table -HideTableHeaders
}
Function New-PSWin { 
    Start-Process -FilePath "powershell.exe" -ArgumentList `
    "-NoLogo -NoProfile -WindowStyle Normal" 
}
Function Get-PSEnv {
    Write-Host "`nMILJÖ VARIABLER" -ForegroundColor `
    White -BackgroundColor Black -NoNewline
    Get-ChildItem env: | select Name | Format-Table -HideTableHeaders
}
Function Get-PSAutoVar {
    Write-Host "`nAUTOMATISKA VARIABLER" -ForegroundColor `
    White -BackgroundColor Black -NoNewline
    Get-Variable | select Name | sort Name | Format-Table -HideTableHeaders
} 
Function Get-PSResWord {
    $reswords = @{"Begin;" = " "; "Break:" = " "; "Catch:" = " "; 
    "Continue:" = " "; "Data:" = " "; "Do:" = " "; "DynamicParam:" = " "; 
    "Else:" = 'else {Write "Inte Bingo"}'; 
    "Elseif:" = 'if ($x-eq 5) {Write "Bingo!"; break} else {Write "Inte Bingo"}'; 
    "End:" = " "; "Exit:" = " "; "Filter:" = " "; "For:" = 'for ($x = 1; $x -lt 11; $x++) {Write-Host $x}'; 
    "ForEach:" = " "; "From:" = " "; "Function:" = " "; "If:" = 'if ($x-eq 5) {Write "Bingo!"; break} 
    else {Write "Inte Bingo"}'; "In:" = " "; "InlineScript:" = " "; "Hidden:" = " "; "Parallel:" = " "; 
    "Param:" = " "; "Process:" = " "; "Return:" = " "; "Sequence:" = " "; "Switch:" = " "; "Throw:" = `
    " "; "Trap:" = " "; "Until:" = " "; "While:" = 'while ($x -ne (Get-Random 10)) 
    {Write "Inte Bingo."; Sleep -Seconds 1}; Write "BINGO!"'; "Workflow:" = " "}
    
    Write-Host "`nRESERVERADE ORD" -BackgroundColor Black -ForegroundColor White -NoNewline
    $reswords | Format-Table -HideTableHeaders 
}
Function main {
    Get-PSproj
    Get-PSHelpMenu
    
}

main
```
