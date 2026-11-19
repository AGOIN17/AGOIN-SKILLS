# Regenera la ficha 01: DXF -> DWG + PDF con accoreconsole -> PNG de control
$s = 'C:\Users\usuario\AppData\Local\Temp\claude\db3e6b77c6882b90\bc43d6f6-dd79-406e-a22c-6ef32f44ca96\scratchpad'
$f = "$s\f1"
Set-Location $s
python ficha01.py f4/v4.dxf f1/ficha01.dxf
if ($LASTEXITCODE -ne 0) { exit 1 }
Remove-Item "$f\ficha01.dwg", "$f\ficha01.pdf" -ErrorAction SilentlyContinue
& 'C:\Program Files\Autodesk\AutoCAD LT 2023\accoreconsole.exe' /i "$f\ficha01.dxf" /s "$f\p01.scr" | Out-Null
python -c @"
import fitz
d = fitz.open(r'f1/ficha01.pdf'); p = d[0]
p.get_pixmap(dpi=110).save(r'f1/ficha01.png')
mm = lambda v: v / 25.4 * 72
p.get_pixmap(dpi=300, clip=fitz.Rect(mm(121), mm(297 - 100), mm(199), mm(297 - 19))).save(r'f1/ficha01_sec.png')
p.get_pixmap(dpi=250, clip=fitz.Rect(mm(66), mm(297 - 240), mm(200), mm(297 - 136))).save(r'f1/ficha01_axo.png')
p.get_pixmap(dpi=250, clip=fitz.Rect(mm(0), mm(297 - 297), mm(62), mm(297 - 0))).save(r'f1/ficha01_cartela.png')
p.get_pixmap(dpi=250, clip=fitz.Rect(mm(64), mm(297 - 132), mm(130), mm(297 - 5))).save(r'f1/ficha01_textos.png')
"@
Get-ChildItem "$f\ficha01.*" | Select-Object Name, Length, LastWriteTime | Format-Table -AutoSize

