<#
PowerShell profile
© 2025 Stefan Blecko
Version 0.4.3
PowerShell 7.5.2, .NET v9.0, PSReadLine v2.3.6

Powershell Shortcuts
F1      ShowCommandHelp
F2      SwitchPredictionView
#>



$host.UI.RawUI.BackgroundColor = 'Black'
$host.PrivateData.ErrorBackgroundColor = 'Black'
$host.PrivateData.WarningBackgroundColor = 'Black'
$host.PrivateData.DebugBackgroundColor = 'Black'
$host.PrivateData.VerboseBackgroundColor = 'Black'
$host.PrivateData.ProgressBackgroundColor = 'DarkBlue'

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
        param (
        [System.IO.FileInfo]$PF = ($projfolder + ":\")
    )
    process {
        Set-Location -Path $PF
        Get-ChildItem *.py, *.ps1, *.ipynb, *.csv, *.md -Exclude *checkpoint*, `
        todo.csv -Recurse | Select-Object @{ Name = "Skript"; Expression = { $_.Name } },
        @{Name = "Senast ändrad"; Expression = { $_.LastWriteTime } } | 
        Sort-Object "Senast ändrad" -Descending | Out-Host 
        if (Test-Path -Path D:\INSTALL\Git\PortableGit\bin\git.exe -PathType Leaf) {
            $Env:PATH += ";D:\INSTALL\Git\PortableGit\bin;D:\INSTALL\gh\bin"
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
}

function Get-AllProjectFolder {
    param (
        [System.IO.FileInfo]$APF = ($projfolder + ":\")
    )
    process {
        Set-Location $APF
        Get-ChildItem -Directory | Where-Object { $_.Name -notlike '.*' -and `
        $_.Name -notlike '__*__' } | Sort-Object -Property CreationTime -Descending | 
        Select-Object @{Name = "Projekt skapade"; Expression = { $_.Name } }
    }       
}

function Set-DefaultPrompt {
    # function Global:prompt {"PS [$env:USERNAME]$PWD> "}
    function Global:prompt {
        "PS $($executionContext.SessionState.Path.CurrentLocation)$( `
            '>' * ($nestedPromptLevel + 1)) "
    }
    Set-Location "$env:USERPROFILE\Desktop\$projfolder"
}

function New-ProjectFolder {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory)]
        [string]$Newproject,
        [System.IO.FileInfo]$ProjectPath = $path2projfolder
    )
    process {
        New-Item -Path $ProjectPath -Name $Newproject `
            -ItemType "directory" | Select-Object FullName -ExpandProperty FullName
        New-Item -Path "$ProjectPath\$Newproject\" -Name "temp" `
            -ItemType "directory" | Select-Object FullName -ExpandProperty FullName
        New-Item -Path "$ProjectPath\$Newproject\" -Name "docs" `
            -ItemType "directory" | Select-Object FullName -ExpandProperty FullName
        New-Item -Path "$ProjectPath\$Newproject\" -Name "$Newproject" `
            -ItemType "directory" | Select-Object FullName -ExpandProperty FullName
        New-Item -Path "$ProjectPath\$Newproject\" -Name "README.md" `
            -ItemType File | Select-Object FullName -ExpandProperty FullName 
        Set-Location -Path "$ProjectPath\$Newproject\temp"
    }
}

function Get-ChangeLog {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory)]
        [string]$Project,
        [System.IO.FileInfo]$ChangeLogPath = "$path2projfolder",
        [string]$Topic
    )
    begin {
        $changelogname = $Project + '-changelog.csv'
        $new_pscustobj = [PSCustomObject]@{
            'Datum'     = "$(Get-Date -Format FileDate)"
            'Changelog' = "$Topic"
        }
    }
    process {
        while ($true) {
            if (Test-Path -Path "$ChangeLogPath\$Project\docs\$changelogname" -PathType Leaf) {
                if ($Topic) {
                    Export-Csv -InputObject $new_pscustobj -Path `
                    "$ChangeLogPath\$Project\docs\$changelogname" -Force -Append
                }
                else {
                    Import-Csv -Path "$ChangeLogPath\$Project\docs\$changelogname"
                }        
            break
            }
            else {
                New-Item -Path "$ChangeLogPath\$Project\" -Name "docs" `
                -ItemType Directory -ErrorAction SilentlyContinue | Out-Null
                New-Item -Path "$ChangeLogPath\$Project\docs\" -Name "$changelogname" `
                    -ItemType File -ErrorAction SilentlyContinue | Out-Null 
                }   
            }
       }
}

function Get-ToDo {
    [CmdletBinding()]
    param (
        [string]$Topic,
        [ValidateSet("WRITER", "YOUTUBE", "GOOGLE", "COPILOT", "GITHUB", "WORK",
            "STACKOVERFLOW", "POWERSHELL", "PYTHON", "MP4", "PDF", "URL", "MAIL")]
        [string]$Category = $null,
        [switch]$EraseData
    )
    process {
        if ($EraseData.IsPresent) {
            Remove-Item "$env:USERPROFILE\todo.csv" -Force -ErrorAction SilentlyContinue
        }
        elseif ($Topic) {
            $create_csv = [PSCustomObject]@{
                'Date'      = "$(Get-Date -Format FileDate)"
                'Category'  = $Category
                'ToDo'      = $Topic
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

function Get-RandomCmdlet {
    [CmdletBinding()]
    param (
        [switch]$CommonAlias,
        $Num = 1
    )
    begin {
        $all = Get-Alias | Select-Object @{
            Name = "Dagens CmdLet"; Expression = { $_.DisplayName }} 
           
        $regexp_test = '^cat |^cd |^clear |^copy |^compare |^cp |^del |^dir |
                        |^echo |^kill |^ls |^man |^md |^mount |^mv |^ps |^pwd |
                        |^touch |^type |^sleep '
    }
    process {
        if ($CommonAlias.IsPresent) {
            $S = $all | Where-Object -Property 'Dagens CmdLet' `
            -Match $regexp_test
            $S[0..($Num-1)]
        }
        else {
            $all | Get-Random -Count $Num  
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
        Expression = { $_.Name } 
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
    $ProgressPreference = 'SilentlyContinue'
    Unblock-File -Path $env:TEMP\* 
    Remove-Item $env:TEMP\* -Force -Recurse 
}

function Clear-PSReadlineHist {
    $psconhist = Get-PSReadLineOption | 
    Select-Object HistorySavePath -ExpandProperty HistorySavePath
    Clear-Content -Path $psconhist -Force
    Clear-History
}

function Get-IpythonProfile {
    $ipyprof = Get-ChildItem "$env:USERPROFILE\.ipython\" -Directory | 
    Select-Object Name -ExpandProperty Name |
    Where-Object { $_.Name -notlike "profile_default" } | ForEach-Object {
        $_.Name -replace "profile_", "" }
    
    $ipyobject = New-Object -TypeName PSObject
    foreach ($o in $ipyprof) {
        Add-Member -InputObject $ipyobject -MemberType NoteProperty -Name `
        'IPython profile (ipython --profile=)' -Value $o -Force
        Write-Output $ipyobject
    }
}

function Get-ShellVariables {
    [CmdletBinding()]
    param (
        [switch]$EnvVar = $false
    )
    process {
        if ($EnvVar.IsPresent) {
            Get-ChildItem env: | Select-Object @{
                Name = "Environment variables"; Expression = { $_.Name } 
            } 
        }
        else {
            Get-Variable | Select-Object @{
                Name = "PowerShell variables"; Expression = { $_.Name } 
            }
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
        "Sidebar"                          = "Ctrl + B"
        "Toggle shell"                     = "Ctrl + J"

    }
}

function Get-ColabShortcuts {
    [PSCustomObject]@{
        "Cell Execution"                   = "Shift + Enter"
        "Insert a new cell above"          = "A"
        "Insert a new cell below"          = "B"
        "Delete the current cell"          = "D,D"
        "Split the current cell"           = "Ctrl + Shift + -"
        "Inline hint (Jupyter-style)"      = "Tab"
        "Manual completion menu"           = "Ctrl + Space"
        "Show shortcuts"                   = "Ctrl + M H"
        "Save the notebook instantly"      = "Ctrl + M S"
        "Convert the current cell"         = "Ctrl + M Y / Ctrl + M M"
        "Interrupt a running cell"         = "Ctrl + M ."
        "Toggle the Table of Contents"     = "Ctrl + M T"
        "Run all cells in the notebook"    = "Ctrl + M R"
        "Open the Command Palette"         = "Ctrl + Shift + P"
        "Full editor-bindings reference"   = "F1"
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
        "Konfig. dokumentmall"         = "ALt + Shift + P"
        "Formellist"                   = "F2"
        "Konfig. språk och korr."      = "Alt + F12"
        "Autokorr. och Autotext"       = "Ctrl + F3"
        "Infoga fältkommando"          = "Ctrl + F2"
        "Synonymordlista"              = "Ctrl + F7"
        "Navigator"                    = "F5"
        "Gå till sida"                 = "Ctrl + G"
        "Hitta och Ersätt"             = "Ctrl + H"
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
    Write-Information "Inte implementerat" -InformationAction Continue
}

function Start-AIHelp {  
    # PowerShell, Obsidian, VSCode, Python
    Write-Information "Inte implementerat" -InformationAction Continue
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
            "TCPIP management", "ZIP files", "Antivirus", "Microsoft 365", 
            "Azure", "RegExp")]
        $Topic
    )
    process {
        if (Test-Path -Path "$HOME\admincmdlets.csv" -PathType Leaf) {
            $pycsvfile = Import-Csv -Path "$HOME\admincmdlets.csv"
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
            "Boilerplate", "Builtins", "Modules", "Jupyterlab shortcuts",
            "Ipython", "Ugly code", "argparse", "pathlib",	"calendar",	
            "Software design principle", "PEP8")]
        $Topic
    )
    process {
        if (Test-Path -Path "$HOME\py3quickref.csv" -PathType Leaf) {
            $pycsvfile = Import-Csv -Path "$HOME\py3quickref.csv"
            $pycsvfile | Select-Object $Topic -Unique -ErrorAction Ignore
        }
        else {
            Write-Error -Message '"py3quickref.csv" finns ej.' -Category ResourceUnavailable
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
        Where-Object { $_.CimClassName -Like $SearchFor -and $_.CimClassName `
                -notlike "Win32_Perf*" }
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
    Write-Information "Inte implementerat" -InformationAction Continue
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
                @{Name = "Användare"; Expression = { $_.CsUserName.Replace(
                "$env:COMPUTERNAME\", "") } },
                @{Name = "Windows-Utgåva"; Expression = { $_.WindowsProductName } },
                @{Name = "Produkt-ID"; Expression = { $_.WindowsProductId } },
                @{Name = "Windows version"; Expression = { $_.OsVersion } },
                @{Name = "Windows build"; Expression = { $_.WindowsVersion } }
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
        'Dynamic Parameters'              = 'DynamicParam {}'
        'ValidateSet Attribute'           = '[ValidateSet("Red", "Green", "Blue")]'
        'Mandatory Parameters'            = '[Parameter(Mandatory=$true)]'
        'ValueFromPipeline'               = 'Parameter(ValueFromPipeline=$true)]'
        'HelpMessage'                     = '[Parameter(HelpMessage="Bla, bla, bla.")]'
        'ValidateScript'                  = '[ValidateScript({Test-Path $_ -PathType Leaf})]'
        'Aliases'                         = '[Alias("Dir")]'
        "else"                            = 'else {Write "Ingen Bonus"}'
        "elseif"                          = 'elseif ($x -eq $ra) {Write "Vinst!"; break}'
        "end"                             = " "
        "filter"                          = " "
        "for"                             = 'for ($x = 1; $x -lt 11; $x++) {cat $x}'
        "foreach"                         = 'foreach ($bonus in $bonus_numbers)'
        "from"                            = " "
        "function"                        = 'function Get-Bonus {[CmdletBinding()] param ()}'
        "if"                              = 'if ($bonus -eq 777) {Write "BONUS!"; break}'
        "In"                              = " "
        "hidden"                          = " "
        "parallel"                        = " "
        "param"                           = " "
        "process"                         = " "
        "return"                          = " "
        "sequence"                        = " "
        "switch"                          = 'switch ($bonus) {777 {$bonus = 500 } } '
        "throw"                           = " "
        "trap"                            = " "
        "Until"                           = " "
        "while"                           = 'while ($x -ne (Get-Random 10))'
        "try"                             = 'try { Get-Item bonus.txt -ErrorAction Stop }'
        "catch"                           = 'catch { "Filen finns inte." }'
        "Escape codes"                    = '`n', '`f'
        "ForEach-Object"                  = '1..20 | % { Write-Host "Försök nr $_" }'
        "Expresion evaluetion"            = '$(exp)'
        "Here string"                     = "'multiline string'"
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
        'Array'                           = '$a = ("a", "b")'
        'Add X to array'                  = '$a += "X"'
        'Result to array'                 = '(Get-Process)'
        'Reverse an array'                = '[array]::Reverse($x)'
        'Associative array'               = '$assoc = @{"one" = 1; "two"=2}'
        'Ordered associative array'       = '$assoc2[ordered]{}'
        'Add member'                      = '$assoc["three"] = 3'
        'Convert to PSCust'               = '$assoc2 = [PSCustomObject]$assoc'
        'Trim'                            = '$trim_char.ToString().Trim(".json")'
        'Sort'                            = '1..10 | Sort-Object -Descending'
        'PSCustomObject'                  = '$myObject = [PSCustomObject]{}'
        'Add member to obj'               = '$myObject | Add-Member'
        'Remove obj'                      = '$myObject.psobject.Properties.Remove()'
        'Convert to JSON'                 = '$myObject | ConvertTo-Json > file.json'
        'Import from JSON'                = '$myO = gc file.json | ConvertFrom-Json'
        'Add member to PSCust'            = '$myO | Add-Member -MemberType NoteProperty'
        'Remove member from PSCust'       = '$myObject.psobject.properties.remove("X")'
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
(Get-ToDo)[-2..-1] | Select-Object ToDo
Clear-TmpFolder
Get-ProjectFolder -PF C:\Users\steble70\Downloads\scriptlab-master
