# Regenera la ficha 03 v6: DXF -> DWG + PDF con accoreconsole -> PNG de control
$s = 'C:\Users\usuario\AppData\Local\Temp\claude\db3e6b77c6882b90\bc43d6f6-dd79-406e-a22c-6ef32f44ca96\scratchpad'
$f = "$s\f6"
Set-Location $s
python ficha03_v6.py f4/v4.dxf f6/v6.dxf
if ($LASTEXITCODE -ne 0) { exit 1 }
Remove-Item "$f\v6.dwg", "$f\v6.pdf" -ErrorAction SilentlyContinue
& 'C:\Program Files\Autodesk\AutoCAD LT 2023\accoreconsole.exe' /i "$f\v6.dxf" /s "$f\p6.scr" | Out-Null
python -c @"
import fitz
d = fitz.open(r'f6/v6.pdf'); p = d[0]
p.get_pixmap(dpi=110).save(r'f6/v6.png')
mm = lambda v: v / 25.4 * 72
p.get_pixmap(dpi=300, clip=fitz.Rect(mm(128), mm(297 - 101), mm(199), mm(297 - 40))).save(r'f6/v6_sec.png')
p.get_pixmap(dpi=220, clip=fitz.Rect(mm(66), mm(297 - 245), mm(200), mm(297 - 136))).save(r'f6/v6_axo.png')
p.get_pixmap(dpi=200, clip=fitz.Rect(mm(0), mm(0), mm(62), mm(297))).save(r'f6/v6_cartela.png')
p.get_pixmap(dpi=200, clip=fitz.Rect(mm(64), mm(297 - 132), mm(130), mm(297 - 5))).save(r'f6/v6_textos.png')
"@
Get-ChildItem "$f\v6.*" | Select-Object Name, Length, LastWriteTime | Format-Table -AutoSize

