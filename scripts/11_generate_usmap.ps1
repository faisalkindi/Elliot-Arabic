<#
  11_generate_usmap.ps1 — produce Mappings.usmap from the RUNNING game using jmap.

  jmap reads the game's process memory (no DLL is injected into the game) and writes a
  .usmap (and can confirm the engine version). This is the least-invasive way to unblock
  UE5 extraction.

  USAGE:
    1. Launch the game and get to the MAIN MENU or in-game (so UE objects are loaded).
    2. Run:  pwsh ./11_generate_usmap.ps1
       If jmap can't auto-detect the engine version, pass it:
              pwsh ./11_generate_usmap.ps1 -EngineVersion 5.4

  Alternative (fully offline): create a full memory dump via Task Manager
  (Details -> Elliot-Win64-Shipping.exe -> Create dump file) then:
              pwsh ./11_generate_usmap.ps1 -Minidump "C:\path\Elliot-Win64-Shipping.DMP"
#>
param(
  [string]$EngineVersion = "",
  [string]$Minidump = ""
)
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$cfg  = Get-Content (Join-Path $here "config.json") -Raw | ConvertFrom-Json
$jmap = Join-Path $here $cfg.jmap_exe
$out  = Join-Path $here $cfg.usmap
New-Item -ItemType Directory -Force -Path (Split-Path $out) | Out-Null

if (-not (Test-Path $jmap)) { Write-Host "[MISSING] jmap_dumper.exe at $jmap" -ForegroundColor Red; exit 1 }

if ($EngineVersion) {
  $env:PATTERNSLEUTH_RES_EngineVersion = $EngineVersion
  Write-Host "[INFO] Forcing engine version $EngineVersion" -ForegroundColor Cyan
}

if ($Minidump) {
  if (-not (Test-Path $Minidump)) { Write-Host "[MISSING] minidump $Minidump" -ForegroundColor Red; exit 1 }
  Write-Host "jmap --minidump `"$Minidump`" `"$out`"" -ForegroundColor DarkGray
  & $jmap --minidump $Minidump $out
}
else {
  $proc = Get-Process -Name "Elliot-Win64-Shipping" -ErrorAction SilentlyContinue
  if (-not $proc) {
    Write-Host "[WAIT] Game process 'Elliot-Win64-Shipping' not found." -ForegroundColor Yellow
    Write-Host "       Launch the game (reach the main menu / in-game), then re-run this script." -ForegroundColor Yellow
    exit 2
  }
  $gamePid = $proc.Id
  Write-Host "[INFO] Found game PID $gamePid. Reading reflection data (this can take a minute)..." -ForegroundColor Cyan
  Write-Host "jmap --pid $gamePid `"$out`"" -ForegroundColor DarkGray
  & $jmap --pid $gamePid $out
}

if (Test-Path $out) {
  $kb = [math]::Round((Get-Item $out).Length/1KB,1)
  Write-Host "[OK] Mappings.usmap written ($kb KB) -> $out" -ForegroundColor Green
  Write-Host "Next: set engine_version in config.json (jmap log shows it), then run 10_extract_iostore.ps1" -ForegroundColor Green
} else {
  Write-Host "[FAIL] no usmap produced. If jmap printed an EngineVersion error, re-run with -EngineVersion <ver>." -ForegroundColor Red
  exit 1
}
