$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$analysisDir = Join-Path $repoRoot 'analysis'

Set-Location $repoRoot

Write-Host 'Building project with CMake...'
cmake --build build

$tcureDll = Get-ChildItem -Path $repoRoot -Recurse -File -Filter 'TCurve.dll' | Select-Object -First 1
if ($tcureDll) {
    $destDll = Join-Path $analysisDir 'TCurve.dll'
    if ($tcureDll.FullName -ne $destDll) {
        Copy-Item -Path $tcureDll.FullName -Destination $destDll -Force
    }
    Write-Host "Ensured TCurve DLL is available in $analysisDir"
} else {
    Write-Warning 'TCurve.dll was not found. Check the build output location.'
}

$pydFile = Get-ChildItem -Path $repoRoot -Recurse -File -Filter '*.pyd' | Select-Object -First 1
if ($pydFile) {
    $destPyd = Join-Path $analysisDir $pydFile.Name
    if ($pydFile.FullName -ne $destPyd) {
        Copy-Item -Path $pydFile.FullName -Destination $destPyd -Force
    }
    Write-Host "Ensured Python module is available in $analysisDir"
} else {
    Write-Warning '*.pyd file was not found. Check the build output location.'
}

$env:PYTHONPATH = '.'
Set-Location $analysisDir


pybind11-stubgen tcurve

$stubFile = Get-ChildItem -Path $analysisDir -Recurse -File -Filter '*.pyi' | Select-Object -First 1
if ($stubFile) {
    Move-Item -Path $stubFile.FullName -Destination (Join-Path $analysisDir $stubFile.Name) -Force
    Write-Host "Moved stub file to $analysisDir"
} else {
    Write-Warning '*.pyi stub file was not found.'
}

$stubsDir = Join-Path $analysisDir 'stubs'
if (Test-Path $stubsDir) {
    Remove-Item -Path $stubsDir -Recurse -Force
    Write-Host "Removed existing stub folder $stubsDir"
}
