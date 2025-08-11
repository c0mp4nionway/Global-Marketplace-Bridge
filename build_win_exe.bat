@echo off
REM Build Dropship Automator into a single executable using PyInstaller
pyinstaller --noconfirm --onefile --windowed --add-data "C:\Users\krist\OneDrive\Töölaud\Dropship\Adjusted\Updated Skeleton\secret.key;." --add-data "C:\Users\krist\OneDrive\Töölaud\Dropship\Adjusted\Updated Skeleton\config.enc;." Global_Marketplace_Bridge.py
pause
