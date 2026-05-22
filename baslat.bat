@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo   CV Portfoy - Django Sunucusu
echo ========================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo HATA: Sanal ortam bulunamadi: .venv\Scripts\python.exe
    echo PyCharm'da File - Settings - Python Interpreter - .venv secin.
    pause
    exit /b 1
)

echo [1/2] Veritabani guncelleniyor...
".venv\Scripts\python.exe" manage.py migrate --noinput
if errorlevel 1 (
    echo migrate basarisiz.
    pause
    exit /b 1
)

echo [2/2] Sunucu baslatiliyor...
echo.
echo   Ana sayfa : http://127.0.0.1:8000/
echo   Admin     : http://127.0.0.1:8000/admin/
echo   Iletisim  : http://127.0.0.1:8000/contact/
echo.
echo   localhost:8000 acilmiyorsa (normal):
echo   - http://127.0.0.1:8000/ kullanin VEYA
echo   - localhost_duzelt.bat dosyasini YONETICI olarak calistirin
echo.
echo Durdurmak icin bu pencerede Ctrl+C
echo.

REM Sunucu yalnizca IPv4'te dinler; localhost bazen IPv6 (::1) oldugu icin
".venv\Scripts\python.exe" manage.py runserver 127.0.0.1:8000
pause
