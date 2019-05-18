<#
.SYNOPSIS
Kalkylerar hur mycket lycka du har i ditt liv. Du får +1 procentenheter för varje sak 
(handling) som har gjort dig lite mer lycklig eller -1 procentenheter som har gjort 
dig lite mindre lycklig. 0 procentenheter om ditt lyckotillstånd är oförändrad. Optimal 
lyckonivå bör ligga något över medel (50%) efter dagens slut. 
.EXAMPLE
Get-DalaiLama -defaulthappiness 51 -happines +2 eller help Get-DalaiLama
.NOTES
© 2019 av Stefan Blecko
Kopiera och spara skriptet i mappen C:\Users\[DITT ANVÄNDARNAMN]\Documents\
PowerShell\Modules\Get-DalaiLama\Get-DalaiLama.psm1. Skripet funkar 
bara med PowerShell Core och Windows. 
#>
function Get-DalaiLama {
    [cmdletBinding()]
    param( 
        [Parameter(Mandatory = $true)]
        $happiness ,
        [Parameter(Mandatory = $false)]
        $defaulthappiness 
    )

    Write-Output "
    Om man önskar lycka bör man söka de orsaker som 
    ger upphov till den och om man inte önskar lidande
    bör man se till att de orsaker och förhållande som
    skulle utlösa det inte längre uppträder.
                                            
                                            Dalai Lama" 

    if ($defaulthappiness -ge 0 -and $defaulthappiness -le 100) {
        Set-Content -Value $defaulthappiness -Path "$env:USERPROFILE\Documents\PowerShell\Modules\Get-DalaiLama\H_value"   
        $read_dh = Get-Content -Path "$env:USERPROFILE\Documents\PowerShell\Modules\Get-DalaiLama\H_value"
    }
    elseif ($defaulthappiness -gt 100) {
        Write-Host -Message "`n`nFel: [-defaulthappiness] är större än 100. Försök igen.`n" -ForegroundColor Red
        break
    }
    elseif (Test-Path -Path "$env:USERPROFILE\Documents\PowerShell\Modules\Get-DalaiLama\H_value") {
        $read_dh = Get-Content -Path "$env:USERPROFILE\Documents\PowerShell\Modules\Get-DalaiLama\H_value"        
    }  
    else {
        Set-Content -Value "50" -Path "$env:USERPROFILE\Documents\PowerShell\Modules\Get-DalaiLama\H_value"
        $read_dh = Get-Content -Path "$env:USERPROFILE\Documents\PowerShell\Modules\Get-DalaiLama\H_value"        
    }
    
    $sum = [int]$read_dh + [int]$happiness
    Write-Host "`n`nDin nuvarande lyckonivå är $sum%.`n"
    Set-Content -Value $sum -Path "$env:USERPROFILE\Documents\PowerShell\Modules\Get-DalaiLama\H_value"
}
