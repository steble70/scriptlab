## Välkommen till Scriptlab
#### [Stefan Bleckos](https://twitter.com/minnesbilder) Python/PowerShell sajt 

```powershell
#Requires -RunAsAdministrator
<#GN - Grävande nätverkstekniker version 0.1
(C) 2018 av Stefan
#>

Set-ExecutionPolicy Bypass -scope Process -Force


<#Visar ditt datormärke, serienummer, processor, opertivsystem, Windows serienummer, ljudkort, 
grafikkort och hårddisk. Visar statusen för ljudkortet, grafikkortet samt hårddisken.#>
Get-CimInstance -ClassName Win32_ComputerSystem | Select-Object @{Name="Datormärke";
Expression={$_.Manufacturer}}, Model | Format-List 
Get-CimInstance -ClassName Win32_Processor | Select-Object @{Name="Processor";
Expression={$_.Name}} | Format-List 
Get-CimInstance -ClassName Win32_OperatingSystem | Select-Object @{Name="Operativsystem";
Expression={$_.Caption}}, BuildNumber, SerialNumber | Format-List 
Get-CimInstance -ClassName Win32_SoundDevice | Select-Object @{Name="Ljudkort";
Expression={$_.Name}},Status | Format-List 
Get-CimInstance -ClassName Win32_VideoController | Select-Object @{Name="Grafikkort";
Expression={$_.Name}}, Status | Format-List 
Get-PhysicalDisk | Select-Object @{Name="Hårddisk";
Expression={$_.FriendlyName}}, OperationalStatus, HealthStatus, Size | Format-List

Write-Host "Kontrollerar om hårddisken är OK..."
Repair-Volume -DriveLetter c -OfflineScanAndFix 
Optimize-Volume -DriveLetter c -Analyze 


<# Om din dator upptäder konstigt (tex helt plötsligt startar om av sig själv), kan det 
vara ett teckan det det är något fel med RAM minnet.#>
while ($true) {
    $memcheck = Read-Host "Vill du kontrollera RAM minnet med Windows minnesdiagnostik (j/n)?"
    if ($memcheck -eq "j") {
        mdsched.exe # Programmet mdsched.exe körs (finns med i Windows 10).
        break      
    }
    elseif ($memcheck -eq "n") {
        Write-Host "Don't Worry Be Happy."
        Start-Sleep -Seconds 5  
        break
    }
    else { 
        $memcheck | Out-Null
    }

}
```
