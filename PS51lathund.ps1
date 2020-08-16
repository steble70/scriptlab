<#
Lathund för PowerShell 7.0 noviser version 0.1j
© 2018, 2020 av Stefan Blecko

Kopiera gärna innehållet i filen till C:\Users\[ditt användarnamn]\Documents\
WindowsPowerShell\Microsoft.PowerShell_profile.ps1.
#>

$host.PrivateData.ErrorBackgroundColor = 'Black'
$host.PrivateData.WarningBackgroundColor = 'Black'
$host.PrivateData.DebugBackgroundColor = 'Black'
$host.PrivateData.VerboseBackgroundColor = 'Black'
$host.PrivateData.ProgressBackgroundColor = 'DarkBlue'
$host.UI.RawUI.BackgroundColor = 'Black'


$PSprojfoldername = "PSproj"
Set-Variable $HOME C:\Users\$env:USERNAME
Write-Host "Användare: $env:USERNAME | Projektmapp: $PSprojfoldername`n" `
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
    Set-Location ($PSprojfoldername + ":")
    Get-ChildItem *.ps1, *.py | Select @{Name = "Skript"; Expression = { $_.Name } },
    @{Name = "Senast ändrad"; Expression = { $_.LastWriteTime } } | sort "Senast ändrad" `
        -Descending | Out-Host
}

Function Get-PSHelpMenu {
    Get-ChildItem Function:Get*, Function:New*, Function:Clear* -Exclude Clear-Host |
    Select-Object @{Name = "Meny"; Expression = { $_.Name } }
}

function Get-PSHelpTopics {
    $ProgressPreference = 'SilentlyContinue'
    Get-Help about_* | select Name | Format-Wide -Column 3 | more
}

Function New-PSWin {
    Start-Process -FilePath "pwsh.exe" -ArgumentList "-NoLogo -WindowStyle Normal"
}

function Clear-TmpFolder {
    $ErrorActionPreference = 'SilentlyContinue'
    Remove-Item $env:TEMP\* -Force -Recurse
}
function Clear-PSReadlineHist {
    Clear-Content $env:USERPROFILE\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
}

Function Get-PSEnv {
    Get-ChildItem env: | select Name | Format-Wide -Column 3 | more
}
function Get-PSAutoVar {
    Get-Variable | select Name | sort Name | Format-Wide -Column 3 | more

}

function Get-VScodeShortcuts {
    [PSCustomObject]@{
        "Indent"              = "Ctrl + Å"
        "Outdent"             = "Ctrl + ´"
        "Debug"               = "F5"
        "Run script"          = "Ctrl + F5"
        "Run selection"       = "F8"
        "Toggle line comment" = "Ctrl + '"
        "Open-EditorFile"     = "Opens file in VS Code from consol"
    }

}
function Get-NewPS7Cmdlets {
    [PSCustomObject]@{
        "Out-GridView"     = 'Ex: $P | Out-GridView'
        "Get-Clipboard"    = 'Get-Clipboard'
        "Set-Clipboard"    = 'Ex: Set-Clipboard -Value "This is a test string"'
        "Out-Printer"      = 'Ex: Get-Content -Path ./readme.txt | Out-Printer'
        "Clear-RecycleBin" = 'Clear-RecycleBin'
        "Get-Hotfix"       = 'Get-Hotfix'
    }
}
function Get-AllCmdlets {
    $OutputEncoding = [console]::OutputEncoding
    $OutputEncoding.ASCIIENCODING
    Get-Command -CommandType Cmdlet, Function | Format-Wide -Property Name -Column 3 | more
}

function Get-CimWin32Class {
    $OutputEncoding = [console]::OutputEncoding
    $OutputEncoding.ASCIIENCODING
    Get-CimClass -ClassName win32_* | where CimClassName -NotLike win32_perf* | more
}
function Get-SIC {
    $ProgressPreference = 'SilentlyContinue'
    $OutputEncoding = [console]::OutputEncoding
    $OutputEncoding.ASCIIENCODING
    Set-Location $env:USERPROFILE\Documents\PowerShell\
    Get-Content SIC.txt | more
}
function Get-Py3QuickRef {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory)]
        [ValidateSet("Strings", "Lists", "Tuples", "Dictionaries", "Sets",
            "Comparisons", "Loops", "List comprehension", "Generators", "Functions",
            "Printing", "File access", "Input", "Error stream", "Other file operations",
            "Exceptions", "OOP", "JSON", "Databases", "SYS", "OS", "Boilerplate",
            "Built-in Functions", "Exceptions")]
        $topic
    )
    Set-Location $env:USERPROFILE\Documents\PowerShell\
    if (Test-Path -Path py3quickref.csv) {
        $pycsvfile = Import-Csv -Path .\py3quickref.csv
        $pycsvfile | Select-Object $topic
    }
    else {
        Write-Error -Message "File not found."
    }
}
function Get-SysInfo {
    $ProgressPreference = 'SilentlyContinue'
    $cpu = Get-ComputerInfo | select CsProcessors -ExpandProperty CsProcessors
    Get-ComputerInfo | select @{Name = "Datormärke"; Expression = { $_.CsManufacturer } },
    @{Name = "Dator serienummer"; Expression = { $_.CsModel } },
    @{Name = "CPU"; Expression = { $cpu.Name } },
    @{Name = "Host Name"; Expression = { $_.CsDNSHostName } },
    @{Name = "Windows-Utgåva"; Expression = { $_.WindowsProductName } },
    @{Name = "Produkt-ID"; Expression = { $_.WindowsProductId } },
    @{Name = "Windows version"; Expression = { $_.OsVersion } },
    @{Name = "Windows build"; Expression = { $_.WindowsVersion } },
    @{Name = "BIOS"; Expression = { $_.BiosManufacturer } },
    @{Name = "BIOS Version"; Expression = { $_.BiosName, $_.BiosVersion } },
    @{Name = "Domän"; Expression = { $_.CsDomain } },
    @{Name = "Domän roll"; Expression = { $_.CsDomainRole } }
}
function Get-BigFiles {
    # Ex: Get-BigFiles -mbyte 7 -path C:\Users\steble70\Desktop\
    [CmdletBinding()]
    param (
        [Parameter(Mandatory)]
        [System.IO.FileInfo]$path,

        [Parameter(Mandatory)]
        [string]$mbyte
    )
    $mbyte = $mbyte + "MB"
    $ErrorActionPreference = 'SilentlyContinue'
    Get-ChildItem -Path $path -Recurse -Force | Select-Object FullName, Length,
    @{Name = "MB"; Expression = { [math]::Round($_.Length / 1MB, 2) } } |
    Where-Object { $_.Length -gt $mbyte }
}

Function Get-Ps7QuickRef {
    [PSCustomObject]@{"begin" = " "; "break" = " "; "catch" = " ";
        "continue" = " "; "data" = " "; "do" = " "; "dynamicParam" = " ";
        "else" = 'else {Write "Ingen Bonus"}';
        "elseif" = 'elseif ($x -eq $ra) {Write "Vinst!"; break}';
        "end" = " "; "exit" = " "; "filter" = " ";
        "for" = 'for ($x = 1; $x -lt 11; $x++) {Write-Host $x}';
        "foreach" = 'foreach ($bonus in $bonus_numbers)'; "from" = " ";
        "function" = 'function Get-Bonus {[CmdletBinding()] param ()}';
        "if" = 'if ($x -eq 777) {Write "BONUS!"; break}'; "In" = " ";
        "inlineScript" = " "; "hidden" = " "; "parallel" = " ";
        "param" = " "; "process" = " "; "return" = " "; "sequence" = " ";
        "switch" = 'switch ($bonus) {n {" "} } '; "throw" = " "; "trap" = " ";
        "Until" = " "; "while" = 'while ($x -ne (Get-Random 10))'; "workflow" = " ";
        "Range operator" = '..';
    }
}

Function main {
    Clear-Host
    Get-PSproj
    Clear-TmpFolder
}

main

