@echo off
chcp 65001
echo =========================================
echo Supabase 保活脚本 - %date% %time%
echo =========================================

cd /d D:\ETSY_Order_Automation\backend

poetry run python scripts\keep_supabase_alive.py

echo.
echo 保活执行完成
echo =========================================
timeout /t 3