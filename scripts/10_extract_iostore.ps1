<#
  10_extract_iostore.ps1 — extract text-bearing assets from Elliot's IoStore archive.

  Converts Zen (.ucas/.utoc) -> legacy .uasset/.uexp using retoc, into config.work_extract,
  so the Python parsers (20_/21_) can read them. READ-ONLY on the game: it only reads the
  Paks folder and writes into the workspace.

  PREREQUISITES (see README.md): retoc.exe in _tools/, a valid Mappings.usmap, and the
  correct engine_version + (if needed) aes_key set in config.json.

  Run:  pwsh ./10_extract_iostore.ps1
        pwsh ./10_extract_iostore.ps1 -Filter "/Game/Elliot/Text"   # narrower extract
#>
param(
  [string]$Filter = ""
)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$cfg  = Get-Content (Join-Path $here "config.json") -Raw | ConvertFrom-Json

$retoc = Join-Path $here $cfg.retoc_exe
$usmap = Join-Path $here $cfg.usmap
$paks  = $cfg.game_paks
$out   = Join-Path $here $cfg.work_extract
$utoc  = Join-Path $paks "Elliot-Windows.utoc"

# --- preflight ---
$fail = $false
if (-not (Test-Path $retoc)) { Write-Host "[MISSING] retoc.exe at $retoc  -> download from github.com/trumank/retoc" -ForegroundColor Yellow; $fail = $true }
if (-not (Test-Path $usmap)) { Write-Host "[MISSING] Mappings.usmap at $usmap -> generate via UE4SS Dumpers (see README, this is the blocker)" -ForegroundColor Yellow; $fail = $true }
if (-not (Test-Path $utoc))  { Write-Host "[MISSING] game archive $utoc" -ForegroundColor Red; $fail = $true }
if ($fail) { Write-Host "Preflight failed. Resolve the items above, then re-run." -ForegroundColor Red; exit 1 }

New-Item -ItemType Directory -Force -Path $out | Out-Null

# --- build retoc args ---
# retoc to-legacy <input.utoc> <output_dir> --version <UE5_x> [--mappings ...] [--aes-key ...] [--filter ...]
$args = @("to-legacy", $utoc, $out, "--version", $cfg.engine_version, "--mappings", $usmap)
if ($cfg.aes_key) { $args += @("--aes-key", $cfg.aes_key) }
if ($Filter)      { $args += @("--filter", $Filter) }
else {
  # default: pull only likely text/data folders to avoid unpacking all ~13.5 GB.
  # NOTE: exact top-level content path for Elliot is unconfirmed; adjust after first
  # `retoc list` of the archive. Common roots: /Game/<Project>/... and /Game/L10N/...
  Write-Host "[INFO] No -Filter given. Listing archive roots first so you can target a folder:" -ForegroundColor Cyan
  & $retoc list $utoc --version $cfg.engine_version --mappings $usmap | Select-Object -First 60
  Write-Host "[INFO] Re-run with -Filter '/Game/...Text...' to extract just the text dirs." -ForegroundColor Cyan
}

Write-Host "retoc $($args -join ' ')" -ForegroundColor DarkGray
& $retoc @args
Write-Host "Done. Extracted assets in: $out" -ForegroundColor Green
Write-Host "Next: python 20_parse_locres.py ; python 21_parse_datatable_json.py" -ForegroundColor Green
