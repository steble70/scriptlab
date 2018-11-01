<#
Lathund för PowerShell 5.1 noviser version 0.1g
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

    
Function Get-PSproj {
    Write-Host "`nPÅGÅENDE POWERSHELL PROJEKT (GET-PSPROJ)" -ForegroundColor White `
    -BackgroundColor Black -NoNewline
    Set-Location ($PSprojfoldername + ":")
    Get-ChildItem *.ps1 | Select @{Name = "Skript"; Expression = {$_.Name}}, 
    @{Name = "Senast ändrad"; Expression = {$_.LastWriteTime}} | sort "Senast ändrad" `
    -Descending | Out-Host
}
Function Get-PSConHelp {
    Write-Host "`nPOWERSHELL KONSOL HJÄLP (GET-PSCONHELP)" -ForegroundColor White `
    -BackgroundColor Black -NoNewline
    Get-PSReadlineKeyHandler -Bound | Select Function, Key | ? {$_.Function `
    -notmatch "DigitArgument"} | Format-Table -HideTableHeaders
    Write-Host "NewPowerShellWindow     New-PSWin`n`n" -ForegroundColor Gray
}

Function New-PSWin { 
    Start-Process -FilePath "powershell.exe" -ArgumentList `
    "-NoLogo -NoProfile -WindowStyle Normal"
}

Function Get-PSEnv {
    Write-Host "`nPOWERSHELL MILJÖ VARIABLER (GET-PSENV)" -ForegroundColor `
    White -BackgroundColor Black -NoNewline
    Get-ChildItem env: | select Name | Format-Table -HideTableHeaders
}
Function Get-PSVar {
    Write-Host "`nINBYGGDA POWERSHELL VARIABLER (GET-PSVAR)" -ForegroundColor `
    White -BackgroundColor Black -NoNewline
    Get-Variable | select Name | sort Name | Format-Table -HideTableHeaders
} 
Function main {
    Get-PSproj
    Get-PSConHelp
    Get-PSEnv
    Get-PSVar

}

main
