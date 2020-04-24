Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser

<#
GN - Grävande Nätverkstekniker
Version 0.1c
© 2020 av Stefan Blecko
#>

function inventory {
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

    # $hdd = Get-CimInstance -ClassName Win32_DiskDrive | Where-Object -Property `
    # DeviceID -EQ \\.\PHYSICALDRIVE0 | Select-Object Model -ExpandProperty Model

    $hdd_size = Get-CimInstance -ClassName Win32_DiskDrive | Where-Object -Property `
    DeviceID -EQ \\.\PHYSICALDRIVE0 | Select-Object size -ExpandProperty Size

    $ram = Get-CimInstance -ClassName Win32_ComputerSystem | Select-Object `
    TotalPhysicalMemory -ExpandProperty TotalPhysicalMemory

    $nic = Get-CimInstance -ClassName Win32_NetworkAdapterConfiguration |
    Where-Object -Property IPEnabled -EQ $true
    <#
    Konvertering medllan Bytes och andra enheter
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
        "Hostname" = $nic.DNSHostName
        "DHCP server" = $nic.DHCPServer
        "DNS Domain" = $nic.DNSDomain
        "IP-adress" = $nic.IPAddress
        "Default Gateway" = $nic.DefaultIPGateway
        "Subnätmask" = $nic.IPSubnet
    }
}
function main {
    inventory
}
main
