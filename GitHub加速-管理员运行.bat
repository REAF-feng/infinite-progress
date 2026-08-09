@echo off
:: GitHub CDN 加速脚本 — 右键 -> 以管理员身份运行
echo ================================================
echo   GitHub 加速 — 修改 HOSTS 文件
echo ================================================
echo.

set HOSTS=%SystemRoot%\System32\drivers\etc\hosts

echo 正在备份原 hosts 文件...
copy /Y "%HOSTS%" "%HOSTS%.backup_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%" >nul 2>&1

echo 正在写入加速条目...
>>"%HOSTS%" echo.
>>"%HOSTS%" echo # GitHub CDN 加速 — 2026-08-09
>>"%HOSTS%" echo 140.82.116.3   github.com
>>"%HOSTS%" echo 140.82.113.3   api.github.com
>>"%HOSTS%" echo 140.82.113.36  ssh.github.com
>>"%HOSTS%" echo 185.199.108.133 raw.githubusercontent.com
>>"%HOSTS%" echo 185.199.109.133 raw.githubusercontent.com
>>"%HOSTS%" echo 185.199.110.133 github.githubassets.com
>>"%HOSTS%" echo 140.82.112.3   codeload.github.com

echo.
echo ================================================
echo   完成！现在可以正常访问 GitHub 了。
echo ================================================
echo.
echo 按任意键退出...
pause >nul
