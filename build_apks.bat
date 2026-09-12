@echo off
echo ===================================================
echo   FANTASY11 DUAL ANDROID APK BUILD SCRIPT
echo ===================================================
echo.
echo Checking for Gradle or Android Studio environment...

where gradlew >nul 2>nul
if %errorlevel% neq 0 (
    echo [INFO] gradlew not found in PATH.
    echo If Android Studio is installed, you can:
    echo 1. Open Android Studio
    echo 2. Select 'Open Project' -> Choose 'android/fantasy11-user-app' or 'android/fantasy11-admin-app'
    echo 3. Click 'Build' -> 'Build Bundle(s) / APK(s)' -> 'Build APK(s)'
    echo.
    echo Or push to GitHub to auto-compile both APKs in cloud using the provided workflow:
    echo .github/workflows/build-apk.yml
    pause
    exit /b 0
)

echo Building Fantasy11 User APK...
cd android\fantasy11-user-app
call gradlew assembleDebug
if %errorlevel% equ 0 (
    echo [SUCCESS] User APK built in android/fantasy11-user-app/app/build/outputs/apk/debug/
) else (
    echo [ERROR] Failed to build User APK.
)
cd ..\..

echo Building Fantasy11 Admin APK...
cd android\fantasy11-admin-app
call gradlew assembleDebug
if %errorlevel% equ 0 (
    echo [SUCCESS] Admin APK built in android/fantasy11-admin-app/app/build/outputs/apk/debug/
) else (
    echo [ERROR] Failed to build Admin APK.
)
cd ..\..
echo.
echo Build complete.
pause
