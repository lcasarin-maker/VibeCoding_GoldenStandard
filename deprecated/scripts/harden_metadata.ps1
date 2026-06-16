param()

$catalogs = @(
    @{ Path = "golden_standard_coding_vices.yaml"; Domain = "vibe-coding"; Kind = "vc" },
    @{ Path = "golden_standard_testing_vices.yaml"; Domain = "testing"; Kind = "vt" },
    @{ Path = "golden_standard_tokenomics.yaml"; Domain = "tokenomics"; Kind = "tk" }
)

foreach ($catalog in $catalogs) {
    $path = Join-Path -Path $PSScriptRoot -ChildPath "..\$($catalog.Path)"
    $path = [System.IO.Path]::GetFullPath($path)
    $text = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
    $lines = $text -split "\r?\n"
    $out = New-Object System.Collections.Generic.List[string]

    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]
        $out.Add($line)

        if ($line -match '^(  status: )([A-Z_]+)$') {
            if ($i + 1 -lt $lines.Count -and $lines[$i + 1] -match '^  severity: ') {
                continue
            }

            $status = $Matches[2]
            $severity = switch ($catalog.Kind) {
                'tk' {
                    if ($status -in @('PREVENTED', 'REMEDIATED')) { 'medium' }
                    elseif ($status -eq 'AUDITED') { 'low' }
                    else { 'low' }
                }
                default {
                    if ($status -in @('PREVENTED', 'REMEDIATED')) { 'high' }
                    elseif ($status -eq 'AUDITED') { 'medium' }
                    else { 'medium' }
                }
            }

            $statusTag = $status.ToLowerInvariant().Replace('_', '-')
            $out.Add("  severity: $severity")
            $out.Add("  tags:")
            $out.Add("    - $($catalog.Domain)")
            $out.Add("    - $statusTag")
        }
    }

    $newText = ($out -join [Environment]::NewLine)
    if ($newText -ne $text) {
        [System.IO.File]::WriteAllText($path, $newText, [System.Text.UTF8Encoding]::new($false))
    }
}
