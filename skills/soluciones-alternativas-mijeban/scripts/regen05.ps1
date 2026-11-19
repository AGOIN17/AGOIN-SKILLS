# Regenera la ficha 03 v5: DXF -> DWG + PDF con accoreconsole -> PNG de control
$s = 'C:\Users\usuario\AppData\Local\Temp\claude\db3e6b77c6882b90\bc43d6f6-dd79-406e-a22c-6ef32f44ca96\scratchpad'
$f = "$s\f5"
Set-Location $s
python ficha03_v5.py f4/v4.dxf f5/v5.dxf
if ($LASTEXITCODE -ne 0) { exit 1 }
Remove-Item "$f\v5.dwg", "$f\v5.pdf" -ErrorAction SilentlyContinue
& 'C:\Program Files\Autodesk\AutoCAD LT 2023\accoreconsole.exe' /i "$f\v5.dxf" /s "$f\p5.scr" | Out-Null
python -c @"
import fitz
d = fitz.open(r'f5/v5.pdf'); p = d[0]
p.get_pixmap(dpi=110).save(r'f5/v5.png')
mm = lambda v: v / 25.4 * 72
p.get_pixmap(dpi=300, clip=fitz.Rect(mm(128), mm(297 - 101), mm(199), mm(297 - 40))).save(r'f5/v5_sec.png')
p.get_pixmap(dpi=220, clip=fitz.Rect(mm(66), mm(297 - 245), mm(200), mm(297 - 136))).save(r'f5/v5_axo.png')
p.get_pixmap(dpi=200, clip=fitz.Rect(mm(0), mm(0), mm(62), mm(297))).save(r'f5/v5_cartela.png')
p.get_pixmap(dpi=200, clip=fitz.Rect(mm(64), mm(297 - 132), mm(130), mm(297 - 5))).save(r'f5/v5_textos.png')
"@
Get-ChildItem "$f\v5.*" | Select-Object Name, Length, LastWriteTime | Format-Table -AutoSize
