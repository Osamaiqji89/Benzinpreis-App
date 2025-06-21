@echo off
:: Build Benzinpreis-App executable using PyInstaller
python -m pip install pyinstaller

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

pyinstaller --noconfirm --windowed --onefile ^
  --icon resources\icons\station.ico ^
  --add-data "resources;resources" main.py

pause
