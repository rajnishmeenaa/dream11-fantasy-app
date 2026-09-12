workflow_content = """name: Build Fantasy11 Dual APKs (User & Admin)

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build-apks:
    name: Build User & Admin Android APKs
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Source Code
        uses: actions/checkout@v4

      - name: Set up Java Development Kit (JDK 17)
        uses: actions/setup-java@v4
        with:
          distribution: 'zulu'
          java-version: '17'

      - name: Setup Android SDK Tools
        uses: android-actions/setup-android@v3

      # Build User App
      - name: Build Fantasy11 User APK
        run: |
          cd android/fantasy11-user-app
          if [ ! -f "gradlew" ]; then
            gradle wrapper --gradle-version 8.2.2
          fi
          chmod +x gradlew
          ./gradlew assembleDebug --no-daemon

      # Build Admin App
      - name: Build Fantasy11 Admin Console APK
        run: |
          cd android/fantasy11-admin-app
          if [ ! -f "gradlew" ]; then
            gradle wrapper --gradle-version 8.2.2
          fi
          chmod +x gradlew
          ./gradlew assembleDebug --no-daemon

      # Archive and Upload User APK
      - name: Upload Fantasy11 Player APK
        uses: actions/upload-artifact@v4
        with:
          name: fantasy11-player-app-debug
          path: android/fantasy11-user-app/app/build/outputs/apk/debug/*.apk

      # Archive and Upload Admin APK
      - name: Upload Fantasy11 Admin Console APK
        uses: actions/upload-artifact@v4
        with:
          name: fantasy11-admin-console-debug
          path: android/fantasy11-admin-app/app/build/outputs/apk/debug/*.apk
"""

with open(".github/workflows/build-apk.yml", "w", encoding="utf-8") as f:
    f.write(workflow_content.strip() + "\n")

print("Updated .github/workflows/build-apk.yml")
