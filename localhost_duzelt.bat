@echo off
chcp 65001 >nul
echo ========================================
echo   localhost -^> 127.0.0.1 duzeltmesi
echo ========================================
echo.
echo Sorun: Windows bazen localhost'u IPv6 (::1) yapar.
echo Django sunucusu 127.0.0.1'de dinledigi icin localhost:8000 acilmaz.
echo.
echo Bu script hosts dosyasina su satiri ekler:
echo   127.0.0.1    localhost
echo.
echo YONETICI olarak calistirmaniz gerekir.
echo Sag tik -^> Yonetici olarak calistir
echo.
pause

net session >nul 2>&1
if errorlevel 1 (
    echo.
    echo HATA: Yonetici yetkisi yok. Sag tik ile "Yonetici olarak calistir" secin.
    pause
    exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$h = Join-Path $env:SystemRoot 'System32\drivers\etc\hosts';" ^
  "$lines = Get-Content $h -ErrorAction Stop;" ^
  "if ($lines -match '^\s*127\.0\.0\.1\s+localhost') { Write-Host 'Zaten var: 127.0.0.1 localhost'; exit 0 };" ^
  "$new = @('', '# CV Portfoy - localhost IPv4', '127.0.0.1    localhost') + $lines;" ^
  "Set-Content -Path $h -Value $new -Encoding ASCII;" ^
  "Write-Host 'Tamam: hosts guncellendi.'"

echo.
echo Simdi tarayicida http://localhost:8000/ deneyin.
echo Hala olmazsa bilgisayari yeniden baslatin veya 127.0.0.1 kullanin.
pause
