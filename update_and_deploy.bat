
@echo off
cd /d %~dp0

echo Git dəyişikliklərini əlavə edir...
git add .

echo Commit edilir...
git commit -m "Kod dəyişiklikləri"

echo Renderə göndərilir...
git push

echo Deploy prosesi başa çatdı.
pause
