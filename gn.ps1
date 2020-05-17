#Requires -RunAsAdministrator

<#
gn.ps1 - Grävande Nätverkstekniker
Version 0.3
© 2020 av Stefan Blecko

Att köra skriptet
1. Starta Powershell 7 som administratör ("Run as Administrator")
2. Det finns nu två sätt att köra skriptet

   Alternativ 1
   Spara skriptet som en .psm1 fil.
   Kopiera filen till $env:USERPROFILE\Documents\PowerShell\Modules\gn\gn.psm1.

   När du sen startar pwsh.exe (PowerShell konsolen) kommer dina funktioner
   automatiskt laddas in.

   Alternativ 2
   Spara skriptet som en .ps1 fil (vanligt skript)
   Kör filen genom att skriva (i PowerShell konsolen):
   . .\gn.ps1

#>

function Get-ComputerInventory {
    $comp_brand = Get-CimInstance -ClassName Win32_ComputerSystem | Select-Object `
    Manufacturer -ExpandProperty Manufacturer

    $bios = Get-CimInstance -ClassName Win32_BIOS | Select-Object Manufacturer `
    -ExpandProperty Manufacturer

    $bios_version = Get-CimInstance -ClassName Win32_BIOS | Select-Object Version `
    -ExpandProperty Version

    $comp_serial = Get-CimInstance -ClassName Win32_ComputerSystem | Select-Object `
    Model -ExpandProperty Model

    $cpu = Get-CimInstance -ClassName Win32_Processor | Select-Object Name `
    -ExpandProperty Name

    $os = Get-CimInstance -ClassName Win32_OperatingSystem | Select-Object Caption `
    -ExpandProperty Caption

    $win_serial = Get-CimInstance -ClassName Win32_OperatingSystem | Select-Object `
    SerialNumber -ExpandProperty SerialNumber

    $snd = Get-CimInstance -ClassName Win32_SoundDevice | Select-Object Name `
    -ExpandProperty Name

    $gpx = Get-CimInstance -ClassName Win32_VideoController | Select-Object Name `
    -ExpandProperty Name

    $hdd_size = Get-CimInstance -ClassName Win32_DiskDrive | Where-Object -Property `
    DeviceID -EQ \\.\PHYSICALDRIVE0 | Select-Object size -ExpandProperty Size

    $ram = Get-CimInstance -ClassName Win32_ComputerSystem | Select-Object `
    TotalPhysicalMemory -ExpandProperty TotalPhysicalMemory

    $nic = Get-CimInstance -ClassName Win32_NetworkAdapterConfiguration |
    Where-Object -Property IPEnabled -EQ $true
    <#
    Konvertering medlan Bytes och andra enheter
    Kbytes: [Bytes] / 1KB
    Mbytes: [Bytes] / 1MB
    Gbytes: [Bytes] / 1GB
    Tbytes: [Bytes] / 1TB
    #>

    [PSCustomObject]@{
        "Tillverkare" = $comp_brand
        "Modell " = $comp_serial
        "BIOS" = $bios
        "BIOS version" = $bios_version
        "Windows version" = $os
        "Windows Produkt-ID" = $win_serial
        "Processor" = $cpu
        "RAM" = [math]::Round($ram / (1GB))
        "Ljudkort" = $snd
        "Grafikkort" = $gpx
        "Hårddisk" = [math]::Round($hdd_size / (1GB))
        "Nätverkskort" = $nic.Description
        "MAC adress" = $nic.MACAddress
        "Hostname" = $nic.DNSHostName
        "DHCP server" = $nic.DHCPServer
        "DNS Domain" = $nic.DNSDomain
        "IP-adress" = $nic.IPAddress
        "Default Gateway" = $nic.DefaultIPGateway
        "Subnätmask" = $nic.IPSubnet
    }
}

function Get-WinLogErr {
    # Ex: Get-WinLogErr -messages 20
    [CmdletBinding()]
    param (
        [Parameter()]
        [ValidateNotNullOrEmpty()]
        [int]$messages = 10
    )
    $sysappseclog = Get-WinEvent -LogName System, Application, Security | Where-Object {
    $_.LevelDisplayName -contains "Varning" -or $_.LevelDisplayName -contains "Fel" `
    -or $_.LevelDisplayName -contains "Kritisk" }
    $sysappseclog | Sort-Object -Top $messages
}
function Get-FilesGreaterThan {
    # Ex: Get-FilesGreaterThan -mbyte 7 -path C:\Users\steble70\Desktop\
    [CmdletBinding()]
    param (
        [Parameter(Mandatory)]
        [string]$mbyte,
        [Parameter(Mandatory)]
        [System.IO.FileInfo]$path
    )
    $mbyte = $mbyte + "MB"
    $ErrorActionPreference = 'SilentlyContinue'
    Get-ChildItem -Path $path -Recurse -Force | Select-Object FullName, Length,
    @{Name = "MB"; Expression = {[math]::Round($_.Length / 1MB, 2)}} |
    Where-Object {$_.Length -gt $mbyte}
}

function Get-InstallProg {
    Get-CimInstance -ClassName Win32_Product | Format-Wide -Property Name -Column 3
}
