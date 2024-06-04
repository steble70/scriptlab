<#
basiceq.ps1 - Basic Equation
version 0.2
(C) 2019 av Stefan Blecko

Outputen ska bli någonting liknande det här (endast Powershell Core):
90 = 27Y - 24
X * 48 = 8
20 = 28Z * 99
55 = 18Y + 59
Y + 6 = 69
79 = 94X + 33
7Y * 28 = 88
83 = Z / 11
77X * 75 = 87
15 = 99Z / 33
#>

function equation_generator {
    $num1 = [string](Get-Random -Minimum 1 -Maximum 60)
    $num2 = [string](Get-Random -Minimum 1 -Maximum 30)
    $num3 = [string](Get-Random -Minimum 1 -Maximum 100)
    
    $num4 = [string](Get-Random -Minimum 1 -Maximum 80)
    $num5 = [string](Get-Random -Minimum 1 -Maximum 70)

    $letter1 = Get-Random -InputObject "X", "Y", "Z"
    $letter2 = Get-Random -InputObject "X", "Y", "Z"

    $operator1 = Get-Random -InputObject " + ", " - ", " * ", " / "
    $operator2 = Get-Random -InputObject " + ", " - ", " * ", " / "

    $numlet_plus_op_plus_num = ("$num1" + "$letter1" + "$operator1" + "$num2") # Tex 19X + 3
    $let_plus_op_plus_num = ("$letter2" + "$operator2" + "$num3") # Tex Y - 4
    
    $left = Get-Random -InputObject $numlet_plus_op_plus_num, $let_plus_op_plus_num 
    $right = Get-Random -InputObject $num4, $num5
    $building_the_equation = Get-Random -InputObject "$left = $right", "$right = $left"
    return $building_the_equation
}
function main {
    Write-Host "GRUNDLÄGGANDE EKVATIONER" -ForegroundColor Blue -BackgroundColor White
    for ($n = 1; $n -lt 11; $n++) {
        Write-Host (equation_generator)
    }
      
}
main
