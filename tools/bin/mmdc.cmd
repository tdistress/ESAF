@echo off
setlocal
pnpm exec mmdc %*
exit /b %ERRORLEVEL%
