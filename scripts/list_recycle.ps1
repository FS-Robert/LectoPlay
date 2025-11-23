$s = New-Object -ComObject Shell.Application
$rb = $s.Namespace(0xA)
$count = $rb.Items().Count
for ($i = 0; $i -lt $count; $i++) {
    $it = $rb.Items().Item($i)
    $orig = $rb.GetDetailsOf($it, 1)
    if ($orig -match 'LectoPlay|Trabajos-pyton-c2|Visca') {
        Write-Output "[$i] $($it.Name) | $orig"
    }
}
