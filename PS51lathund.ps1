<#
PowerShell profile
Version 0.3.2.4
PowerShell version 7.4.1
    - .NET v8.0.0
    - PSReadLine v2.3.4

© 2024 Stefan Blecko
---

Powershell Shortcuts
F1      ShowCommandHelp
F2      SwitchPredictionView
#>

$host.PrivateData.ErrorBackgroundColor = 'Black'
$host.PrivateData.WarningBackgroundColor = 'Black'
$host.PrivateData.DebugBackgroundColor = 'Black'
$host.PrivateData.VerboseBackgroundColor = 'Black'
$host.PrivateData.ProgressBackgroundColor = 'DarkBlue'
$host.UI.RawUI.BackgroundColor = 'Black'

Set-Variable $HOME $env:USERPROFILE  
$projfolder = "POPYS"
$path2projfolder = "$env:USERPROFILE\Desktop\$projfolder"

if (Test-Path -Path $path2projfolder) {
}
else {
    New-Item -Path "$env:USERPROFILE\Desktop\" -Name $projfolder `
        -ItemType "directory" | Out-Null
    New-Item -Path "$env:USERPROFILE\Desktop\$projfolder\" -Name datafiles `
        -ItemType "directory" | Out-Null
    New-Item -ItemType File "$path2projfolder\untitled1.ps1" | Out-Null
}

New-PSDrive -Name $projfolder -PSProvider FileSystem -Root $path2projfolder `
-Description "Välkommen till skriptlådan." | Out-Null

function Get-ProjectFolder {
    Set-Location ($projfolder + ":\")
    Get-ChildItem *.py, *.ps1, *.ipynb, *.csv, *.md -Exclude *checkpoint.ipynb, `
    todo.csv -Recurse | Select-Object @{ Name = "Skript"; Expression = { $_.Name } },
    @{Name = "Senast ändrad"; Expression = { $_.LastWriteTime } } | 
    Sort-Object "Senast ändrad" -Descending | Out-Host 
    if (Test-Path -Path D:\INSTALL\Git\PortableGit\bin\git.exe -PathType Leaf) {
        $Env:PATH += ";D:\INSTALL\Git\PortableGit\bin"
        function Global:prompt {
            (Write-Host "[GIT]" -NoNewline -ForegroundColor DarkYellow `
            -BackgroundColor DarkBlue) + 
            "$($executionContext.SessionState.Path.CurrentLocation)$( `
                '>' * ($nestedPromptLevel + 1)) "
            return " "
        }
    }
    else {
        Write-Warning "Hittade inte Git portable." -WarningAction Continue
    }
}

function Get-AllProjectFolder {
    Set-Location ($projfolder + ":\")
    Get-ChildItem -Directory | Where-Object { $_.Name -notlike '.*' -and `
    $_.Name -notlike '__*__' } | Sort-Object -Property CreationTime -Descending | 
    Select-Object @{Name = "Projekt skapade"; Expression = { $_.Name } }       
}

function Set-DefaultPrompt {
    # function Global:prompt {"PS [$env:USERNAME]$PWD> "}
    function Global:prompt {
        "PS $($executionContext.SessionState.Path.CurrentLocation)$( `
            '>' * ($nestedPromptLevel + 1)) "
    }
    Set-Location "$env:USERPROFILE\Desktop\$projfolder"
}

function New-ProjektFolder {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory)]
        [string]$Newproject
    )
    process {
        New-Item -Path $path2projfolder -Name $Newproject `
            -ItemType "directory" | Select-Object FullName -ExpandProperty FullName
        New-Item -Path "$path2projfolder\$Newproject\" -Name "temp" `
            -ItemType "directory" | Select-Object FullName -ExpandProperty FullName
        New-Item -Path "$path2projfolder\$Newproject\" -Name "docs" `
            -ItemType "directory" | Select-Object FullName -ExpandProperty FullName
        New-Item -Path "$path2projfolder\$Newproject\" -Name "$Newproject" `
            -ItemType "directory" | Select-Object FullName -ExpandProperty FullName
        New-Item -Path "$path2projfolder\$Newproject\" -Name "README.md" `
            -ItemType File | Select-Object FullName -ExpandProperty FullName 
        Set-Location -Path "POPYS:\$Newproject\temp"
    }
}

function Get-ChangeLog {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory)]
        [string]$Project,
        [string]$Topic
    )
    begin {
        $changelogname = $Project + '-changelog.csv'
    }
    process {
        if ($Topic) {
            $new_pscustobj = [PSCustomObject]@{
                'Datum'     = "$(Get-Date -Format FileDate)"
                'Changelog' = "$Topic"
            }
            $new_pscustobj | 
            Export-Csv "$path2projfolder\$Project\docs\$changelogname" -Force -Append
        }
        else {
            if (Test-Path -Path "$path2projfolder\$Project\docs\$changelogname") {
                Import-Csv -Path "$path2projfolder\$Project\docs\$changelogname"
            }
            else {
                New-Item -Path "$path2projfolder\$Project\docs\" -Name "$changelogname" `
                -ItemType File | Out-Null 
                Write-Warning "$changelogname finns ej. Skapar $changelogname." `
                -WarningAction Continue
            }
        }
    }
}

function Get-ToDo {
    [CmdletBinding()]
    param (
        [string]$Topic,
        [ValidateSet("WRITER", "YOUTUBE", "GOOGLE", "COPILOT", "GITHUB",
        "STACKOVERFLOW", "POWERSHELL", "PYTHON", "MP4", "PDF", "URL")]
        [string]$Tag = $null,
        [switch]$EraseData
    )
    process {
        if ($EraseData.IsPresent) {
            Remove-Item "$env:USERPROFILE\todo.csv" -Force -ErrorAction SilentlyContinue
        }
        elseif ($Topic) {
            $create_csv = [PSCustomObject]@{
                'Date' = "$(Get-Date -Format FileDate)"
                'Tag'  = $Tag
                'ToDo' = $Topic
            }
            $create_csv | 
            Export-Csv "$env:USERPROFILE\todo.csv" -Force -Append
        }
        else {
            if (Test-Path -Path "$env:USERPROFILE\todo.csv") {
                Import-Csv -Path "$env:USERPROFILE\todo.csv"
            }
            else {
                
            }
        }
    }
}

function Get-PSConHelp {
    Get-PSReadlineKeyHandler -Bound | Select-Object Function, Key |
    Where-Object { $_.Function -notmatch "DigitArgument" }
}

function Get-AllHelpTopics {
    # $OutputEncoding = [console]::OutputEncoding
    # $OutputEncoding.ASCIIENCODING
    $ProgressPreference = 'SilentlyContinue'
    Get-Help about_* | Select-Object @{Name = "Help article"; 
    Expression = { $_.Name } } 
}

function Get-RandomCmdlet {
    [CmdletBinding()]
    param (
        $Num = 1 
    )
    process {
        @(Get-Alias | Select-Object @{Name = "Dagens CmdLet"; Expression = { `
            $_.DisplayName } }) | Get-Random -Count $Num 
    }
}

function New-PowerShellWindow {
    param (
        [switch]$AdminWindow = $false,
        [System.IO.FileInfo]$ScriptFile = '-'
    )
    process {
        if ($AdminWindow.IsPresent) {
            Start-Process -FilePath "pwsh.exe" -ArgumentList `
                "-NoLogo -NoExit -File $ScriptFile" -Verb RunAs
        } 
        else {
            Start-Process -FilePath "pwsh.exe" -ArgumentList `
                "-NoLogo -NoExit -File $ScriptFile"
        }
    }
}

function Clear-TmpFolder {
    $ErrorActionPreference = 'SilentlyContinue'
    Unblock-File -Path $env:TEMP\*
    Remove-Item $env:TEMP\* -Force -Recurse
}

function Clear-PSReadlineHist {
    $psconhist = Get-PSReadLineOption | 
    Select-Object HistorySavePath -ExpandProperty HistorySavePath
    Clear-Content -Path $psconhist -Force
    Clear-History
}

function Show-IpythonProfile {
    param (
        [switch]$ListProfile,
        [switch]$DelHistData,
        [System.IO.FileInfo]$SQLiteFile = 
        "$env:USERPROFILE\.ipython\profile_clipro\history.sqlite"
    )
    if ($ListProfile.IsPresent) {
        Get-ChildItem "$env:USERPROFILE\.ipython\" -Directory | 
        Select-Object Name -ExpandProperty Name |
        Where-Object {$_.Name -notlike "profile_default"} | ForEach-Object {
        $_.Name -replace "profile_", ""}
        Write-Output "`nipython --profile="
    }
    elseif ($DelHistData.IsPresent) {
        Remove-Item -Path $SQLiteFile -Force -ErrorAction SilentlyContinue
    }
    else {
        Write-Warning "Parameter saknas." -InformationAction Continue
    }
}

function Show-ShellVar {
    [CmdletBinding()]
    param (
        [switch]$EnvVar = $false
    )
    process {
        if ($EnvVar.IsPresent) {
            Get-ChildItem env: | Select-Object @{
                Name = "Environment variables"; Expression = { $_.Name } } 
        }
        else {
            Get-Variable | Select-Object @{
                Name = "PowerShell variables"; Expression = { $_.Name } }
        }
    }
}

function Get-VScodeShortcuts {
    [PSCustomObject]@{
        "Indent/Outdent"                   = "Ctrl + Å/´"
        "Maximize panel size"              = "Ctrl + Alt + Ö"
        "Debug"                            = "Ctrl+ Shift + D"
        "Debugging module"                 = "Import-Module MyModule.psm1"
        "Run script"                       = "Ctrl + F5"
        "Run selection"                    = "F8"
        "Insert snippets"                  = "Ctrl + Alt + J"
        "Open New External Terminal"       = "Ctrl + Shift + C"
        "IntelliSense"                     = "Ctrl + I"
        "Search"                           = "Ctrl + Shift + F"
        "Line comment"                     = "Ctrl + '"
        "Block comment"                    = "Shift + Alt + A"
        "Go to line"                       = "Ctrl + G"
        "Insert snippet"                   = "Ctrl + Alt + J"
        "Run VS Code in current dir"       = "code ."
        "Refactor"                         = "Ctrl + Shift + R"
        "Explorer"                         = "Ctrl + Shift + E"
        "Outline view"                     = "Alt + O"
        "Git"                              = "Ctrl + Shift + G"
        "Toggle between Light/Dark Themes" = "Ctrl + Alt + T"
    }
}

function Get-GitQuickRef {
    [PSCustomObject]@{
        'Create repositories' = 'git init', 'git clone [url]'
        'Branches'            = 'git branch [branch-name]', 'git checkout',
                                'git merge [branch]', 'git branch -d [branch-name]'
        'Synchronize changes' = 'git fetch', 'git merge', 'git push', 'git pull'
        'Make changes'        = 'git status', 'git log', 'git log --follow [file]',
                                'git show [commit]', 'git add [file]',
                                'git commit -m "[descriptive message]"'
        'GitHub skills'       = 'skills.github.com'
    }
}

function Get-ObsidianQuickRef {
    [PSCustomObject]@{
        'Internal linking'     = '[[Internal link]]'
        'Embeds'               = '![[Obsidian#What is Obsidian]]'
        'Header'               = '#'
        'Emphasis'             = '*Italic text*'
        'Bold, Italic'         = '_**This is bold Italic text**_'
        'Lists 1'              = '-'
        'Lists 2'              = '1.'
        'Images'               = '![Tolkien](https://something/pic.jpg)'
        'Resizing images'      = '![Tolkien|100](https://something/pic.jpg)'
        'YouTube embed'        = '![](https://www.youtube.com/...)'
        'External links'       = '[Obsidian help](http:obsidian.md)'
        'Obsidian URI links'   = '[Link to node](obsidian://)'
        'Blockquotes'          = '>'
        'Inline code'          = '`text`'
        'Code blocks'          = '```python```'
        'Task list 1'          = '- [ ]'
        'Task list 2'          = '- [x]'
        'Strikethrough'        = '~~text~~'
        'Highlighting'         = '==text=='
        'Subscript'            = 'H~2~O'
        'Superscript'          = 'X^2^'
        'Comments'             = '%%This is a comment%%'
        'Footnotes'            = '[^1]'
        'Horizontal bar'       = '---'
        'term'                 = ': definition'
        'Tables'               = '| First Header | Second Header |'
        'Open command palette' = 'Ctrl + P'
        'Delete paragraph'     = 'Ctrl + D'
        'Follow link'          = 'Alt + Enter'
        'Insert MD link'       = 'Ctrl + K'
        'Quick switcher'       = 'Ctrl + O'
        'Open settings'        = 'Ctrl + ,'
        'Create new note'      = 'Ctrl + N'
        'Search'               = 'Ctrl + F'
        'Search & replace'     = 'Ctrl + H'
        'Bold'                 = 'Ctrl + B'
    }
}

function Get-WriterShortcuts {
    [PSCustomObject]@{
        "Skapa formatmall"             = "Shift + F11"
        "Formatmallar"                 = "F11"
        "Synonymordlista"              = "Ctrl + F7"
        "Navigator"                    = "F5"
        "Gå till sida"                 = "Ctrl + G"
        "Sök och Ersätt"               = "Ctrl + H"
        "Skapa tabell"                 = "Ctrl + F12"
        "Centrerad text"               = "Ctrl + E"
        "Vänsterjusterad"              = "Ctrl + L"
        "Brödtext"                     = "Ctrl + 0"
        "Rubrik 2"                     = "Ctrl + 2"
        "Radbrytning utan nytt stycke" = "Shift + Enter"
        "Sidbrytning"                  = "Ctrl + Enter"
        "Helskärm"                     = "Shift + Ctrl + J"
        "Infoga kommentar"             = "Ctrl + Alt + C"
        "Block selektion"              = "Ctrl + Shift + F8"
        "Punktlista"                   = "Shift + F12"
        "Upphäv bladskydd"             = "Ctrl + Shift + T"
        "Slutet av dokumentet"         = "Ctrl + End"
        "Höger-klick"                  = "(kontext) meny"
    }
}

function Get-CalcShortcuts {
    Write-Warning "Inte implementerat" -InformationAction Continue
    
}

function Get-ITHelp {   
    param (
        [ValidateSet("PowerShell", "Obsidian", "VSCode", "Python")]
        [string]$Topic
    )
    process {
        switch ($Topic) {
            "PowerShell" {
                Start-Process "https://learn.microsoft.com/en-us/powershell/scripting/overview"}
            "Obsidian" {
                Start-Process "https://help.obsidian.md/Home"}
            "VSCode" {
                Start-Process "https://code.visualstudio.com/updates"}
            "Python" {
                Start-Process "https://docs.python.org/3/library/index.html"   
            }
            default {
                Start-Process "https://stackoverflow.com/questions"}
        }
    }        
}

function Set-WindowTitle {
    param (
        [Parameter(Mandatory)] 
        [string]$Title
    )
    process {
        $host.UI.RawUI.WindowTitle = "$Title"
    }    
}

function Get-PredictiveIntelliSense {
    # F.o.m PowerShell 7.3 är "predictiveIntelliSense" aktiverat som default
    Get-PSReadLineOption | Select-Object PredictionSource, PredictionViewStyle
}

function Get-AdminTask {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory)]
        [ValidateSet("Server management", "Security", "Hardware inventory", 
            "Patching", "Print management", "Remote management",
            "Remote management (parameterName ComputerName)", "Running files",
            "List files", "Service management", "Accunts management", "Cim",
            "Process management", "Service management", "Windows Log", 
            "TCPIP management", "ZIP files", "Antivirus", "Microsoft 365", "Azure")]
        $Topic
    )
    process {
        if (Test-Path -Path "$env:USERPROFILE\Desktop\$projfolder\admincmdlets.csv" -PathType Leaf) {
            $pycsvfile = Import-Csv -Path "$env:USERPROFILE\Desktop\$projfolder\admincmdlets.csv"
            $pycsvfile | Select-Object $Topic -Unique -ErrorAction Ignore
        }
        else {
            Write-Error -Message '"admincmdlets.csv" finns ej.' -Category ObjectNotFound
        }
    }
}

function Get-Py3QuickRef {
    param (
        [Parameter(Mandatory)]
        [ValidateSet("Strings",	"Lists", "Tuples", "Dictionaries", "Sets",	
            "Comparisons", "Math", "Loops", "List comprehension", "Generators",
            "Functions", "Printing", "File access", "Input", "Error streams", 
            "Exceptions", "OOP", "Debugging", "JSON", "Databases", "SYS", "OS", 
            "Boilerplate", "Builtins", "Modules", "Jupyterlab shortcuts", "Ipython", 
            "Ugly code", "argparse", "pathlib",	"calendar",	"Software design principle",
            "PEP8")]
        $Topic
    )
    process {
        if (Test-Path -Path "$env:USERPROFILE\Desktop\$projfolder\py3quickref.csv" -PathType Leaf) {
            $pycsvfile = Import-Csv -Path "$env:USERPROFILE\Desktop\$projfolder\py3quickref.csv"
            $pycsvfile | Select-Object $Topic -Unique -ErrorAction Ignore
        }
        else {
            Write-Error -Message '"py3quickref.csv" finns ej.' -Category ObjectNotFound
        }
    }
}

function Get-CimWin32Classes {
    [CmdletBinding()]
    param (
        [string]$SearchFor = "*"
    )
    process {
        Get-CimClass -ClassName win32_* | Select-Object CimClassName |
        Where-Object {$_.CimClassName -Like $SearchFor -and $_.CimClassName `
        -notlike "Win32_Perf*"}
    }
}

function Get-VimQuickRef {
    <#
    Vim 9 script syntax
    vim9script
    # Detta är en kommentar
    var a = 1
    g:jackpot = {
        mini: 10000
        medium: 100000
        maxi: 1000000
        }
    
    def bonus():
    return something    
    #>
    [PSCustomObject]@{
        'Command-line mode'                   = ':'
        'Cursor momment'                      = 'h, j, k, l'
        'Start of line'                       = '0'
        'End of line'                         = '$'
        'Move down half a page'               = 'Ctrl + d'
        'Move up a half a page'               = 'Ctrl + u'
        'Go to line'                          = ': [num]'
        'Select'                              = 'v'
        'Copy'                                = 'y', 'yy', 'Ctrl + Insert'
        'Cut'                                 = 'd', 'Shift + Delete'
        'Paste'                               = 'p', 'Shift + Insert'
        'Save'                                = 'w', 'wq'
        'Delete character'                    = 'x', 'X'
        'Delete word'                         = 'dw', 'de'
        'Undo'                                = 'u'
        'Redo'                                = 'Ctrl + r'
        'Visual mode'                         = 'v'
        'New window'                          = ':vnew'
        'Split Window'                        = 'Ctrl + ws', 'Ctrl + wv'
        'Switch window'                       = 'Ctrl + ww'
        'Resize all windows'                  = 'CTRL + W='
        'Decreases the current window height' = 'CTRL + W-'
        'New tab'                             = ':tabe'
        'Go to the next tab'                  = 'gt'
        'Search'                              = '/', '?'
        'Run Python code inside vim'          = ':! clear; python3 %'
        'Invoke terminal'                     = ':term'
    }
}

function Get-CCNAQuickRef {
    Write-Warning "Inte implementerat" -InformationAction Continue
}

function Get-SysInfo {
    param (
        [switch]$TcpIp = $false
    )
    begin {
        $ProgressPreference = 'SilentlyContinue'
    }
    process {
        if ($TcpIp.IsPresent) {
            Get-ComputerInfo | Select-Object CsNetworkAdapters -ExpandProperty `
            CsNetworkAdapters | Where-Object { $_.ConnectionStatus -eq "Connected" } |
            Format-List Description, ConnectionStatus, IPAddresses, DHCPServer
        }
        else {
            Get-ComputerInfo | Select-Object @{
            Name = "Datornamn"; Expression = { $_.CsName } },
            @{Name = "Datortillverkare"; Expression = { $_.CsManufacturer } },
            @{Name = "Dator serienummer"; Expression = { $_.CsModel } },
            @{Name = "Windows-Utgåva"; Expression = { $_.WindowsProductName } },
            @{Name = "Produkt-ID"; Expression = { $_.WindowsProductId } },
            @{Name = "Windows version"; Expression = { $_.OsVersion } },
            @{Name = "Windows build"; Expression = { $_.WindowsVersion } }
            # @{Name = "BIOS"; Expression = { $_.BiosManufacturer } },
            # @{Name = "BIOS Version"; Expression = { $_.BiosName, $_.BiosVersion } }
        }
    }
}

function Get-Ps7QuickRef {
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
        "Escape codes"                    = '`n', '`f'
        "ForEach-Object"                  = '1..20 | ForEach-Object { Write-Host "Försök nr $_. $(vinst) " }'
        "Expresion evaluetion"            = '$(exp)'
        "Here string"                     = "@'multiline string'@"
        'Increment value'                 = '++'
        'Decrement'                       = '--'
        'String matches'                  = '-like'
        'String matches regex'            = '-match'
        'Reference a value in collection' = '-contaians'
        'Split string'                    = '-split'
        'Join string'                     = '-join'
        'Format output'                   = '-f'
        'Array elements'                  = '$x[4..12]'
        'Last elements'                   = '$y[-1]'
        'Last 4 elements'                 = '$z[-4..-1]'
        'Index pos 1,4, and 6 through 9'  = '$arr[1,4+6..9]'
        'Array'                           = '$a = @("a", "b")'
        'Add X to array'                  = '$a += "X"'
        'Result to array'                 = '@(Get-Process)'
        'Reverse an array'                = '[array]::Reverse($x)'
        'Associative array'               = '$assoc = @{one=1 ; two=2}'
        'Ordered associative array'       = '$assoc2[ordered]@{}'
        'Add member'                      = '$assoc["three"] = 3'
        'Convert to PSCust'               = '$assoc2 = [PSCustomObject]$assoc'
        'Trim'                            = '$trim_char.ToString().Trim(".json")'
        'Sort'                            = '1..10 | Sort-Object -Descending'
        'PSCustomObject'                  = '$myObject = [PSCustomObject]@{}'
        'Add member to obj'               = '$myObject | Add-Member'
        'Remove obj'                      = '$myObject.psobject.Properties.Remove()'
        'Convert to JSON'                 = '$myObject | ConvertTo-Json > file.json'
        'Import from JSON'                = '$myO = gc file.json | ConvertFrom-Json'
        'Add member to PSCust'            = '$myO | Add-Member -MemberType NoteProperty -Name X -Value X'
        'Remove member from PSCust'       = '$myObject.psobject.properties.remove("X")'
        '[Parameter()]'                   = '[ValidateSet("X", "Y", "Z")]', 
                                            '[ValidateRange()]', '[ValidateScript({})]'
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

New-Alias -Name "touch" -Value New-Item -Description "Create new file."
Clear-Host
Clear-TmpFolder
Get-ProjectFolder
Write-Host
try {(Get-ToDo)[-1] | Format-List -Property "ToDo" | Out-String -NoNewline}
catch { }
Get-RandomCmdlet | Format-List | Out-String -NoNewline
Write-Host
