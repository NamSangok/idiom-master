@echo off
chcp 65001 > nul
echo ========================================================
echo   🌟 IdiomMaster - GitHub 자동 푸시 스크립트 🌟
echo ========================================================
echo.

git status
echo.
set /p commit_msg="커밋 메시지를 입력하세요 (엔터 시 기본값): "
if "%commit_msg%"=="" set commit_msg=Update idioms data and app

git add .
git commit -m "%commit_msg%"

echo.
echo GitHub으로 푸시 중...
git push origin main

echo.
echo ========================================================
echo   ✅ GitHub 푸시 완료! Netlify가 실시간으로 자동 배포합니다.
echo ========================================================
pause
