foreach ($f in @('2610.41257v1','2610.41629v1','2610.41618v1')) {
  $html = Get-Content "$PSScriptRoot\$f.html" -Raw
  $html = $html -replace '(?s)<script.*?</script>', '' -replace '(?s)<style.*?</style>', ''
  $text = $html -replace '</(p|div|section|h1|h2|h3|h4|h5|h6|figcaption|li|tr|blockquote)>', "`n"
  $text = $text -replace '<[^>]+>', ' '
  $text = $text -replace '&nbsp;', ' ' -replace '&amp;', '&' -replace '&lt;', '<' -replace '&gt;', '>'
  $text = $text -replace '[ \t]+', ' '
  $lines = $text -split "`n" | ForEach-Object { $_.Trim() } | Where-Object { $_.Length -gt 2 }
  $lines | Out-File -Encoding utf8 "$PSScriptRoot\$f`_lines.txt"
  Write-Output ($f + ': ' + $lines.Count + ' lines')
}
