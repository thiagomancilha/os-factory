<#
.SYNOPSIS
  Renders a .osFactory OS DOCX to PDF (via Word COM) and then to
  per-page PNGs + a contact sheet (via pdftoppm), for visual audit.

.DESCRIPTION
  Generic by design: takes the DOCX and output directory as parameters,
  never a hardcoded demand or client name. Must run on native Windows
  with Microsoft Word installed (Word COM automation is not available
  from a Linux/WSL/bridged shell — run this script directly in Windows
  PowerShell).

  Mirrors the mechanism already proven in the sibling .proposalFactory
  repository: Word COM opens the DOCX, exports it as PDF via
  ExportAsFixedFormat, and pdftoppm rasterizes each PDF page to PNG.

.PARAMETER InputDocx
  Path to the source .docx file.

.PARAMETER OutputDir
  Directory where the PDF, page-NNN.png files and contact-sheet.png
  will be written. Created if it does not exist.

.PARAMETER PdftoppmPath
  Optional explicit path to pdftoppm.exe. If omitted, the script looks
  for pdftoppm on PATH.

.EXAMPLE
  pwsh tools/render_docx_with_word.ps1 -InputDocx 05-output\<demanda>\OS-<demanda>.docx -OutputDir 05-output\<demanda>\preview
#>
param(
  [Parameter(Mandatory=$true)][string]$InputDocx,
  [Parameter(Mandatory=$true)][string]$OutputDir,
  [Parameter(Mandatory=$false)][string]$PdftoppmPath
)

$ErrorActionPreference = 'Stop'

$inputPath = (Resolve-Path -LiteralPath $InputDocx).Path
$outputPath = [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $OutputDir))
New-Item -ItemType Directory -Force -Path $outputPath | Out-Null

$baseName = [System.IO.Path]::GetFileNameWithoutExtension($inputPath)
$pdfPath = Join-Path $outputPath ($baseName + '.pdf')

# --- Resolve pdftoppm before touching Word, so we fail fast ---
if (-not $PdftoppmPath) {
  $cmd = Get-Command pdftoppm -ErrorAction SilentlyContinue
  if ($cmd) { $PdftoppmPath = $cmd.Source }
}
if (-not $PdftoppmPath -or -not (Test-Path -LiteralPath $PdftoppmPath)) {
  Write-Output "VISUAL_VALIDATION_NOT_EXECUTED: pdftoppm nao encontrado (instale poppler ou informe -PdftoppmPath)."
  exit 2
}

# --- Word COM: DOCX -> PDF ---
try {
  $word = New-Object -ComObject Word.Application
} catch {
  Write-Output "VISUAL_VALIDATION_NOT_EXECUTED: Microsoft Word (COM) nao disponivel neste host."
  exit 2
}

$word.Visible = $false
$word.DisplayAlerts = 0
try {
  $doc = $word.Documents.Open($inputPath, $false, $true)
  # wdExportFormatPDF = 17
  $doc.ExportAsFixedFormat($pdfPath, 17)
  $doc.Close($false)
} finally {
  $word.Quit()
  [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($word) | Out-Null
}

if (-not (Test-Path -LiteralPath $pdfPath)) {
  Write-Output "OUTPUT_BLOCKED: exportacao para PDF falhou ($pdfPath nao foi criado)."
  exit 3
}

# --- pdftoppm: PDF -> PNG per page ---
& $PdftoppmPath -png -r 150 $pdfPath (Join-Path $outputPath 'page')

$pages = Get-ChildItem -Path $outputPath -Filter 'page-*.png' | Sort-Object Name
if ($pages.Count -eq 0) {
  Write-Output "OUTPUT_BLOCKED: rasterizacao produziu zero paginas PNG."
  exit 3
}

# --- Contact sheet: simple grid montage via .NET System.Drawing ---
Add-Type -AssemblyName System.Drawing
$thumbW = 300
$images = $pages | ForEach-Object { [System.Drawing.Image]::FromFile($_.FullName) }
$thumbH = [int]($thumbW * $images[0].Height / $images[0].Width)
$cols = [Math]::Min(4, $images.Count)
$rows = [Math]::Ceiling($images.Count / $cols)
$sheet = New-Object System.Drawing.Bitmap ([int]($cols * $thumbW)), ([int]($rows * $thumbH))
$g = [System.Drawing.Graphics]::FromImage($sheet)
$g.Clear([System.Drawing.Color]::White)
for ($i = 0; $i -lt $images.Count; $i++) {
  $x = ($i % $cols) * $thumbW
  $y = [Math]::Floor($i / $cols) * $thumbH
  $g.DrawImage($images[$i], $x, $y, $thumbW, $thumbH)
}
$contactSheetPath = Join-Path $outputPath 'contact-sheet.png'
$sheet.Save($contactSheetPath, [System.Drawing.Imaging.ImageFormat]::Png)
foreach ($img in $images) { $img.Dispose() }
$g.Dispose()
$sheet.Dispose()

Write-Output "OK: $pdfPath"
Write-Output "OK: $($pages.Count) paginas PNG em $outputPath"
Write-Output "OK: $contactSheetPath"
