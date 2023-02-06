<#
VScode PowerShell extension profile
Version 0.1
© 2023 av Stefan Blecko

Kopiera gärna innehållet i filen till C:\Users\[ditt användarnamn]\Documents\
PowerShell\Microsoft.VSCode_profile.ps1.
#>

Set-Variable $HOME C:\Users\$env:USERNAME
$PSprojfoldername = "POPYS"

New-PSDrive -Name $PSprojfoldername -PSProvider FileSystem -Root `
    "$env:USERPROFILE\Desktop\$PSprojfoldername" -Description `
    "Välkommen till skriptlådan." | Out-Null

function Get-ProjectFolder {
    Set-Location ($PSprojfoldername + ":\")
    Get-ChildItem *.py, *.ps1, *.ipynb, *.csv, *.md -Exclude *checkpoint.ipynb -Recurse | 
        Select-Object @{
        Name = "Skript"; Expression = { $_.Name } },
        @{Name = "Senast ändrad"; Expression = { $_.LastWriteTime } } | 
        Sort-Object "Senast ändrad" -Descending | Out-Host 
}

function Get-AllProjectFolder {
    Set-Location ($PSprojfoldername + ":\")
    Get-ChildItem -Directory | Where-Object {$_.Name -notlike '.*' -and $_.Name -notlike '__*__' } | 
    Sort-Object -Property CreationTime -Descending | 
    Select-Object @{Name = "Projekt skapade"; Expression = { $_.Name } } 
}

function Get-VScodeShortcuts {
    [PSCustomObject]@{
        "Indent/Outdent"                   = "Ctrl + Å/´"
        "Maximize panel size"              = "Ctrl + Alt + Ö"
        "Debug"                            = "Ctrl+ Shift + D"
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

function Get-AdminTask {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory)]
        [ValidateSet("Server management", "Print management", "Remote management",
            "Remote management (parameterName ComputerName)", "Runing files",
            'Service management', "Windows Log", "TCPIP management", "ZIP files",
            "List files", "Accunts management", "Cim", "Process management",
            "Service management", "Windows Log", "TCPIP management", "ZIP files",
            "Antivirus", "Office 365", "Azure")]
        $Topic
    )
    process {
        if (Test-Path -Path "$env:USERPROFILE\Documents\PowerShell\admincmdlets.csv" -PathType Leaf) {
            $pycsvfile = Import-Csv -Path "$env:USERPROFILE\Documents\PowerShell\admincmdlets.csv"
            $pycsvfile | Select-Object $Topic -Unique -ErrorAction Ignore
        }
        else {
            Write-Error -Message '"admincmdlets.csv" finns ej.' -Category ObjectNotFound
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
        'Import from JSON'                = '$myObjectImport = Get-Content file.json | ConvertFrom-Json'
        'Add member to PSCust'            = '$myObject | Add-Member -MemberType NoteProperty -Name X -Value X'
        'Remove member from PSCust'       = '$myObject.psobject.properties.remove("X")'
    }
}

Get-ProjectFolder