![PowerShell-Python Logo](/Banner.jpg)


## Välkommen till Scriptlab
#### [Stefan Bleckos](https://twitter.com/minnesbilder) Python/PowerShell sajt 
##### Klicka gärna på länkarna ovan för titta närmare på källkoden.

```powershell
<#
Lathund för PowerShell 7.0 noviser version 0.3
© 2022 av Stefan Blecko

Kopiera gärna innehållet i filen till C:\Users\[ditt användarnamn]\Documents\
WindowsPowerShell\Microsoft.PowerShell_profile.ps1.
#>

$host.PrivateData.ErrorBackgroundColor = 'Black'
$host.PrivateData.WarningBackgroundColor = 'Black'
$host.PrivateData.DebugBackgroundColor = 'Black'
$host.PrivateData.VerboseBackgroundColor = 'Black'
$host.PrivateData.ProgressBackgroundColor = 'DarkBlue'
$host.UI.RawUI.BackgroundColor = 'Black'


$PSprojfoldername = "POPYS"
Set-Variable $HOME C:\Users\$env:USERNAME
if (Test-Path -Path "C:\Users\$env:USERNAME\Desktop\$PSprojfoldername") {
}
else {
    New-Item -Path "C:\Users\$env:USERNAME\Desktop\" -Name $PSprojfoldername `
        -ItemType "directory" | Out-Null
    New-Item -ItemType File "C:\Users\$env:USERNAME\Desktop\$PSprojfoldername\untitled1.ps1" | Out-Null
}
New-PSDrive -Name $PSprojfoldername -PSProvider FileSystem -Root `
    "C:\Users\$env:USERNAME\Desktop\$PSprojfoldername" -Description `
    "Välkommen till skript lådan." | Out-Null

Function Get-ProjectFolder {
    Set-Location ($PSprojfoldername + ":")
    Get-ChildItem *.py, *.ps1, *.ipynb -Recurse | Select-Object @{Name = "Skript"; Expression = { $_.Name } },
    @{Name = "Senast ändrad"; Expression = { $_.LastWriteTime } } | Sort-Object "Senast ändrad" `
        -Descending | Out-Host
}

function Get-FileCount {
    [CmdletBinding()]
    param (
        [array]$Path = '*',
        [switch]$Recurse,
        [switch]$GroupFileExtension
    )
    process {
        if ($Recurse.IsPresent) {
            if ($GroupFileExtension.IsPresent) {
                Get-ChildItem $Path -Recurse -File | Group-Object -Property Extension |
                Select-Object @{Name = "Antal"; Expression = { $_.Count } },
                @{Name = "Filändelse"; Expression = { $_.Name } }
                $c1 = Get-ChildItem $Path -Recurse -File | Measure-Object |
                Select-Object Count -ExpandProperty Count
                Write-Output "`nAntal filer (Exklusive folders): $c1"
            }
            else {
                $c1 = Get-ChildItem $Path -Recurse -File | Measure-Object |
                Select-Object Count -ExpandProperty Count
                Write-Output "`nAntal filer (Exklusive folders): $c1"
            }
        }
        else {
            if ($GroupFileExtension.IsPresent) {
                Get-ChildItem $Path -File | Group-Object -Property Extension |
                Select-Object @{Name = "Antal"; Expression = { $_.Count } },
                @{Name = "Filändelse"; Expression = { $_.Name } }
                $c2 = Get-ChildItem $Path -File | Measure-Object |
                Select-Object Count -ExpandProperty Count
                Write-Output "`nAntal filer (Exklusive folders): $c2"
            }
            else {
                $c2 = Get-ChildItem $Path -File | Measure-Object |
                Select-Object Count -ExpandProperty Count
                Write-Output "`nAntal filer (Exklusive folders): $c2"
            }
        }
    }
}

function New-ProjektFolder {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory)]
        [string]$Newproject
    )
    process {
        New-Item -Path "C:\Users\$env:USERNAME\Desktop\$PSprojfoldername\" -Name $Newproject `
            -ItemType "directory" | Select-Object FullName -ExpandProperty FullName
        New-Item -Path "C:\Users\$env:USERNAME\Desktop\$PSprojfoldername\$Newproject\" -Name "temp" `
            -ItemType "directory" | Select-Object FullName -ExpandProperty FullName
        New-Item -Path "C:\Users\$env:USERNAME\Desktop\$PSprojfoldername\$Newproject\" -Name "docs" `
            -ItemType "directory" | Select-Object FullName -ExpandProperty FullName
        New-Item -Path "C:\Users\$env:USERNAME\Desktop\$PSprojfoldername\$Newproject\" -Name "$Newproject" `
            -ItemType "directory" | Select-Object FullName -ExpandProperty FullName
        New-Item -Path "C:\Users\$env:USERNAME\Desktop\$PSprojfoldername\$Newproject\" -Name "README.md" `
            -ItemType File | Select-Object FullName -ExpandProperty FullName
    }

}

Function Show-FuncMenu {
    Get-ChildItem Function:Get*, Function:New*, Function:Clear* -Exclude Clear-Host |
    Select-Object @{Name = "Meny"; Expression = { $_.Name } }
}

Function Get-PSConHelp {
    Get-PSReadlineKeyHandler -Bound | Select-Object Function, Key |
    Where-Object { $_.Function -notmatch "DigitArgument" } | more
}

function Get-PSHelpTopics {
    $ProgressPreference = 'SilentlyContinue'
    $OutputEncoding = [console]::OutputEncoding
    $OutputEncoding.ASCIIENCODING
    Get-Help about_* | Format-Wide -Property Name -Column 3 | more
}
function Get-StackOverflowHelp {
    param (
        [array]$topic = "powershell"
    )
    process {
        Start-Process "https://stackoverflow.com/questions/tagged/$topic"
    }
}

function New-PowerShellWindow {
    Start-Process -FilePath "pwsh.exe" -ArgumentList "-NoLogo -WindowStyle Normal"
}

function New-AdminWindow {
    [CmdletBinding()]
    param (
        [System.IO.FileInfo]$File = '-')
    Start-Process -FilePath "pwsh.exe" -ArgumentList "-NoLogo -NoExit -File $File" -Verb RunAs
}

function Clear-TmpFolder {
    $ErrorActionPreference = 'SilentlyContinue'
    Remove-Item $env:TEMP\* -Force -Recurse
}

function Clear-PSReadlineHist {
    Clear-Content $env:USERPROFILE\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
}

Function Get-PSEnv {
    Get-ChildItem env: | Format-Wide -Property Name -Column 3
}

function Get-PSAutoVar {
    Get-Variable | Format-Wide -Property Name -Column 3
}

function Get-VScodeShortcuts {
    [PSCustomObject]@{
        "Indent/Outdent"             = "Ctrl + Å/´"
        "Maximize panel size"        = "Ctrl + Alt + Ö"
        "Debug"                      = "Ctrl+ Shift + D"
        "Run script"                 = "Ctrl + F5"
        "Run selection"              = "F8"
        "Insert snippets"            = "Ctrl + Alt + J"
        "Open New External Terminal" = "Ctrl + Shift + C"
        "IntelliSense"               = "Ctrl + I"
        "Search"                     = "Ctrl + Shift + F"
        "Line comment"               = "Ctrl + '"
        "Block comment"              = "Shift + Alt + A"
        "Go to line"                 = "Ctrl + G"
        "Insert snippet"             = "Ctrl + Alt + J"
        "Run VS Code in current dir" = "code ."
        "Refactor"                   = "Ctrl + Shift + R"
        "Explorer"                   = "Ctrl + Shift + E"
        "Outline view"               = "Alt + O"
    }
}

function Get-SoftwareDesignPrinciple {
    [PSCustomObject]@{
        'KISS principle'                  = 'https://en.wikipedia.org/wiki/KISS_principle'
        "Don't repeat yourself"           = "https://en.wikipedia.org/wiki/Don't_repeat_yourself"
        'Open-closed principle'           = 'https://en.wikipedia.org/wiki/Open–closed_principle'
        'Composition over inheritance'    = 'https://en.wikipedia.org/wiki/Composition_over_inheritance'
        'Single-responsibility principle' = 'https://en.wikipedia.org/wiki/Single-responsibility_principle'
        'Separation of Concerns'          = 'https://en.wikipedia.org/wiki/Separation_of_concerns'
        "You aren't gonna need it"        = "https://en.wikipedia.org/wiki/You_aren't_gonna_need_it"
        'Premature Optimization'          = 'https://en.wikipedia.org/wiki/Program_optimization'
        'Code refactoring'                = 'https://en.wikipedia.org/wiki/Code_refactoring'
        'Clean Code'                      = ''
    }
}

function Get-VimQuickRef {
    [PSCustomObject]@{
        'Command-line mode'          = ':'
        'Cursor momment'             = 'h, j, k, l'
        'Start of line'              = '0'
        'End of line'                = '$'
        'Move down half a page'      = 'Ctrl + d'
        'Move up a half a page'      = 'Ctrl + u'
        'Go to line'                 = ': [num]'
        'Copy'                       = 'y', 'yy'
        'Paste'                      = 'p'
        'Save'                       = 'w', 'wq'
        'Delete character'           = 'x', 'X'
        'Delete word'                = 'dw', 'de'
        'Undo'                       = 'u'
        'Redo'                       = 'Ctrl + r'
        'Visual mode'                = 'v'
        'New window'                 = ':vnew'
        'Split Window'               = 'Ctrl + ws', 'Ctrl wv'
        'Switch window'              = 'Ctrl + ww'
        'New tab'                    = ':tabe'
        'Go to the next tab'         = 'gt'
        'Search'                     = '/', '?'
        'Run Python code inside vim' = ':! clear; python %'
    }
}

function Get-WriterShortcuts {
    [PSCustomObject]@{
    }
}

function Get-StudyTips {
    Start-Process "https://en.wikipedia.org/wiki/Study_skills"
}

function Get-WhatsNew {
    param (
        [switch]$Python = $false
    )
    process {
        if ($Python.IsPresent) {
            Start-Process "https://github.com/python/cpython/tree/main/Doc/whatsnew"
        }
        else {
             Start-Process "https://github.com/MicrosoftDocs/PowerShell-Docs/tree/staging/reference/docs-conceptual/whats-new"

        }
    }
}

function Set-PredictiveIntelliSense {
    param (
        [switch]$Off = $false
    )
    process {
        if ($Off.IsPresent) {
            Set-PSReadLineOption -PredictionSource None
        }
        else {
            Set-PSReadLineOption -PredictionSource History
        }
    }
}

function Get-ToDo {
    [CmdletBinding()]
    param (
        [string]$idea,
        [string]$powershell,
        [string]$python,
        [string]$ccna,
        [string]$finished,
        [string]$writer,
        [string]$calc,
        [string]$youtube,
        [string]$books
    )
    process {
        if ($idea -or $powershell -or $python -or $ccna -or $finished -or $writer -or
            $calc -or $youtube -or $books) {
            $new_pscustobj = [PSCustomObject]@{
                'Datum'                  = "$(Get-Date -Format FileDate)"
                'Idéer till nya projekt' = "$idea"
                'PowerShell projekt'     = "$powershell"
                'Python projekt'         = "$python"
                'CCNA projektet'         = "$ccna"
                'Slutförda projekt'      = "$finished"
                'LibreOffice Writer'     = "$writer"
                'LibreOffice Calc'       = "$calc"
                'Youtube'                = "$youtube"
                'Böcker'                 = "$books"
            }
            $new_pscustobj | Export-Csv $HOME\todo.csv -Force -Append
        }
        else {
            if (Test-Path -Path $HOME\todo.csv) {
                Import-Csv -Path $HOME\todo.csv
            }
            else {
                Write-Error "$HOME\todo.csv måste skapas först."
            }
        }
    }
}


function Get-AllCmdlets {
    $OutputEncoding = [console]::OutputEncoding
    $OutputEncoding.ASCIIENCODING
    Get-Command -CommandType Cmdlet, Function | Format-Wide -Property Name -Column 3 |
    more
}

function Get-AdminCmdlets {
    $ProgressPreference = 'SilentlyContinue'
    $core_cmdlets = @(Get-Command -Noun *PSSession* | Select-Object Name -ExpandProperty Name)
    $loca_cmdlets = @(
        Get-Command -Module Microsoft.PowerShell.LocalAccounts |
        Select-Object Name -ExpandProperty Name)
    $cim_cmdlets = @(
        'Get-CimInstance -ClassName Win32_Service | Format-Table Name, State, Started, Status, StartMode',
        'Get-CimInstance -ClassName Win32_OperatingSystem | select LastBootUpTime')
    $computer_par = @(Get-Command -CommandType Cmdlet -ParameterName 'ComputerName' |
        Select-Object Name -ExpandProperty Name)
    $proc_cmdlets = @(
        '(Get-Process -Name vlc).Kill()', 'Stop-Process -Name "vlc"',
        'Get-Process | Where-Object Path -Match "Avira", | select name, id, path',
        'Get-Process -Name vlc | select Id, StartTime',
        'Get-Process | Out-GridView -PassThru | Stop-Process',
        'Get-Process | Out-String | Set-Clipboard')
    $srv_cmdlest = @(
        'Get-Service | Where-Object DisplayName -Match "Avira"',
        'Get-Service workstation | select  Username, Starttype, BinaryPathName',
        'Get-Service | where {$_.Status -eq "Running" -and $_.Name -like "w*"}',
        'Set-Service -Name AdobeARMservice -StartupType Disabled')
    $tcpip_cmdlets = @(
        'Test-Connection www.google.com', 'Test-Connection www.google.com -Traceroute',
        'Get-NetIPAddress', 'Resolve-DnsName', 'Get-NetTCPConnection', 'Get-DnsClient',
        'Clear-DnsClientCache', 'Disable-NetAdapter -Name "Adapter Name"')
    $getitems_cmdlets = @(
        'dir HKLM:\SOFTWARE\',
        'dir .\Users\Admin\Install\*.exe | select VersionInfo -ExpandProperty VersionInfo',
        'Get-ChildItem -Name Avira* | Get-ItemProperty -Exclude SilentlyContinue | select -ExpandProperty VersionInfo',
        'dir Cert:\LocalMachine\Root | ? NotAfter -LT (Get-Date).AddDays(300) | select Subject, NotAfter',
        'Get-Item bonux.txt'
        'dir -Path *.mp4 -Recurse -Filter *powershell* | select FullName > all_ps_mp4.txt')


    [PSCustomObject]@{
        'Core'                         = $core_cmdlets
        'Management'                   = @('Rename-Computer', 'Restart-Computer')
        'LocalAccounts'                = $loca_cmdlets
        'CIM instances'                = $cim_cmdlets
        'ParameterName "ComputerName"' = $computer_par
        'Get items'                    = $getitems_cmdlets
        'Windows Log'                  = 'Get-WinEvent -ListLog * | ? isEnabled | Out-GridView'
        'Processer'                    = $proc_cmdlets
        'Services'                     = $srv_cmdlest
        'Minmum, maximum, sum'         = 'dir | Measure-Object'
        'Looping'                      = '1..20 | ForEach-Object {Write-Host "Försök nr $_. $(vinst) "}'
        'Rename property'              = '@{Name = ""; Expression = {} }'
        'Run variable'                 = 'Invoke-Expression $string'
        'Run cmdlets/*.ps1 file'       = 'Invoke-Command -ComputerName x -ScriptBlock {ipconfig /release}'
        'Open a file'                  = 'Invoke-Item bonus.pdf'
        'Run file'                     = '& notepad.exe'
        'TCPIP'                        = $tcpip_cmdlets
        'Windows Defender update'      = 'Update-MpSignature'
        'Windows Defender scan'        = 'Start-MpWDOScan'
        'Trim'                         = '$trim_char.ToString().Trim(".json")'
        'Sort'                         = '1..10 | Sort-Object -Descending'
        'Azure'                        = @('New-AzVM', 'Get-AzVM', 'Stop-AzVM', 'Start-AzVM', 'Restart-AzVM')
        'Office 365'                   = ''
        'Remote cmdlets'               = @('$credentials = Get-Credential',
                                         '$PSSessionOption = New-PSSessionOption -SkipCACheck',
                                         'Enter-PSSession -ComputerName xxx -Credential $credentials -SessionOption $PSSessionOption -UseSSL')
        'Zip files'                    = @('Compress-Archive -Path C:\Demo\* -DestinationPath archive.zip',
                                           'Compress-Archive -Path *.log -DestinationPath',
                                           'Expand-Archive -Path archive.zip -DestinationPath')
        'Shutdown'                     = 'shutdown /s'
        'Hibernate'                    = 'shutdown /h'
        'Reboot'                       = 'shutdown /r'
        'Reboot (with comment)'        = 'shutdown /r /c "comment"'
        'IP Configuration'             = 'ipconfig /all'
        'Connect to network share'     = 'net use B: \\FPS01\users'
        'Add computer to domain'       = 'Add-Computer -DomainName Domain01 -Server Domain01\DC01 -PassThru -Verbose'
        'Aktivitetshanteraren'         = 'Taskmgr.exe'
    }
}

function Get-CimWin32Classes {
    $OutputEncoding = [console]::OutputEncoding
    $OutputEncoding.ASCIIENCODING
    Get-CimClass -ClassName win32_* | Where-Object CimClassName -NotLike win32_perf* |
    Format-Wide CimClassName -Column 3 | more
}

function Invoke-Evim {
    <#
    EVim (Easy Vim): vim -y -n [filnamn]
    Commamd mode: Ctrl + O / Ctrl + L
    Spara: Ctrl + S
    Vim 64bit (med bla Python support):
    https://github.com/vim/vim-win32-installer/releases
    #>
    param (
        [ValidateScript( {
                if ($_ -match "\.py|\.txt|\.ini|\.ps1|\.log|\.htm|\.html|\.bat|
                \.cmd|\.inf|\.json") {
                    return $true
                }
                else {
                    throw "Fel filändelse!"
                }
            })]
        [System.IO.FileInfo]$file
    )

    if (Test-Path -Path "C:\Program Files\VIM") {
        vim -y -n $file
    }
    else {
        Write-Error "Hittade inte Vim Directory. Är Vim installerad?"
    }
}

function Get-Py3QuickRef {
    param (
        [Parameter(Mandatory)]
        [ValidateSet("Strings", "Lists", "Tuples", "Dictionaries", "Sets",
            "Comparisons", "Loops", "List comprehension", "Generators", "Functions",
            "Printing", "File access", "Input", "Error streams", "Other file operations",
            "Exceptions", "OOP", "JSON", "Databases", "SYS", "OS", "Boilerplate",
            "Jupyterlab shortcuts", "IPython shortcuts", "Builtins")]
        $topic
    )
    Set-Location $env:USERPROFILE\Documents\PowerShell\
    if (Test-Path -Path py3quickref.csv) {
        $pycsvfile = Import-Csv -Path .\py3quickref.csv
        $pycsvfile | Select-Object $topic -Unique

    }
    else {
        Write-Error -Message "Filen finns ej."
    }
}

function Get-CCNAQuickRef {
    param (
        [Parameter(Mandatory)]
        [ValidateSet("TCP/IP", "Ethernet", "IP Routing", "Cisco IOS", "IPv4 Subnetting",
         	"OSPF", "IP Version 6", "Wireless Networks")]
        $topic
    )
    Set-Location $env:USERPROFILE\Documents\PowerShell\
    if (Test-Path -Path CCNAquickref.csv) {
        $CCNAcsvfile = Import-Csv -Path .\CCNAquickref.csv
        $CCNAcsvfile | Select-Object $topic -Unique

    }
    else {
        Write-Error -Message "Filen finns ej."
    }
}

function Get-SysInfo {
    $ProgressPreference = 'SilentlyContinue'
    Get-ComputerInfo | Select-Object @{Name = "Datortillverkare";
    Expression = { $_.CsManufacturer } },
    @{Name = "Dator serienummer"; Expression = { $_.CsModel } },
    @{Name = "Windows-Utgåva"; Expression = { $_.WindowsProductName } },
    @{Name = "Produkt-ID"; Expression = { $_.WindowsProductId } },
    @{Name = "Windows version"; Expression = { $_.OsVersion } },
    @{Name = "Windows build"; Expression = { $_.WindowsVersion } },
    @{Name = "BIOS"; Expression = { $_.BiosManufacturer } },
    @{Name = "BIOS Version"; Expression = { $_.BiosName, $_.BiosVersion } }
}

function Get-IPAddress {
    $ProgressPreference = 'SilentlyContinue'
    Get-ComputerInfo | Select-Object CsNetworkAdapters -ExpandProperty CsNetworkAdapters |
    Where-Object { $_.ConnectionStatus -eq "Connected" } |
    Format-List Description, ConnectionID, IPAddresses
}

Function Get-Ps7QuickRef {
    [PSCustomObject]@{
        # Mindre viktiga reserverade ord: exit, workflow, inlineScript
        "begin"                           = " "
        "break"                           = " "
        "continue"                        = " "
        "data"                            = " "
        "do"                              = " "
        "dynamicParam"                    = " "
        "else"                            = 'else {Write "Ingen Bonus"}'
        "elseif"                          = 'elseif ($x -eq $ra) {Write "Vinst!"; break}'
        "end"                             = " "
        "filter"                          = " "
        "for"                             = 'for ($x = 1; $x -lt 11; $x++) {Write-Host $x}'
        "foreach"                         = 'foreach ($bonus in $bonus_numbers)'
        "from"                            = " "
        "function"                        = 'function Get-Bonus {[CmdletBinding()] param ()}'
        "if"                              = 'if ($x -eq 777) {Write "BONUS!"; break}'
        "In"                              = " "
        "hidden"                          = " "
        "parallel"                        = " "
        "param"                           = " "
        "process"                         = " "
        "return"                          = " "
        "sequence"                        = " "
        "switch"                          = 'switch ($bonus) {777 {"Bonus!"} } '
        "throw"                           = " "
        "trap"                            = " "
        "Until"                           = " "
        "while"                           = 'while ($x -ne (Get-Random 10))'
        "try"                             = 'try { Get-Item bonus.txt -ErrorAction Stop } catch { "Filen finns inte." }'
        "Range operator"                  = '1..10'
        "Expresion evaluetion"            = '$(exp)'
        "Here string"                     = "@'multiline string'@"
        'Increment value'                 = '++'
        'Decrement'                       = '--'
        'String matches'                  = '-like'
        'String not matches'              = '-notlike'
        'String matches regex'            = '-match'
        'Reference a value in collection' = '-contaians'
        'Split string'                    = '-split'
        'Join string'                     = '-join'
        'Format output'                   = '-f'
        'Array elements'                  = '$x[4..12]'
        'Last elements'                   = '$y[-1]'
        'Last 4 elements'                 = '$z[-4..-1]'
        'Array'                           = '$a = @("a", "b")'
        'Add X to array'                  = '$a += "X"'
        'Result to array'                 = '@(Get-Process)'
        'Reverse an array'                = '[array]::Reverse($x)'
        'Associative array'               = '$assoc = @{one=1 ; two=2}'
        'Add member'                      = '$assoc["three"] = 3'
    }
}

function Get-Win10QuickRef {
    [PSCustomObject]@{
        "Lås skärmen"                      = "Win + L"
        "File Explorer"                    = "Win + E"
        "New File Explorer window"         = "Ctrl + N"
        "Run"                              = "Win + R"
        "Windows-inställningar"            = "Win + I"
        "Projicera"                        = "Win + P"
        "Sök"                              = "Win + S"
        "Starta Corona app"                = "Win + C"
        "Diktering"                        = "Win + H"
        "Connect"                          = "Win + K"
        "Växla mellan appar / program"     = "Alt + Tab"
        "Starta Klipp och Skissa"          = "Win + Shift + S"
        "Snap app / fönster"               = "Win + ←↑↓→"
        "Växla mellan virtuella skrivbord" = "Win + Ctrl + ← →"
        "Quick link menu"                  = "Win + X"
        "PowerShell full screen mode"      = "Alt + Enter"
    }
}

Clear-Host
Get-ProjectFolder
Clear-TmpFolder
```
