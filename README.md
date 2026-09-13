# ⚡ Fantasy11 - Dual Android Sports Gaming & Admin Platform

Fantasy11 is a production-ready fantasy sports platform built with a **Dual Android Architecture**:
1. **Fantasy11 Player App (`com.fantasy11.app`)**: Built for end users to draft fantasy teams across **Cricket** 🏏, **Football** ⚽, and **Kabaddi** 🤼, join private friend leagues, enjoy Web Audio stadium crowd sound effects, follow real-time live ball-by-ball simulation, and manage deposits & 6-box OTP IMPS bank withdrawals.
2. **Fantasy11 Admin Console (`com.fantasy11.admin`)**: A dedicated executive operations console for managers to publish/delete guaranteed lobby contests, schedule multi-sport fixtures, calibrate user balances & view transaction audit ledgers, and inject live match events using **God Mode**.

---

## 📁 Repository Structure

```
├── android/
│   ├── fantasy11-user-app/          # Native Android Studio Project (Player App)
│   │   ├── app/build.gradle         # Package: com.fantasy11.app, SDK 34
│   │   └── src/main/
│   │       ├── AndroidManifest.xml
│   │       ├── java/com/fantasy11/app/MainActivity.java
│   │       └── res/layout/activity_main.xml
│   │
│   └── fantasy11-admin-app/         # Native Android Studio Project (Admin Console)
│       ├── app/build.gradle         # Package: com.fantasy11.admin, SDK 34
│       └── src/main/
│           ├── AndroidManifest.xml
│           ├── java/com/fantasy11/admin/AdminActivity.java
│           └── res/layout/activity_admin.xml
│
├── public/
│   ├── index.html                   # Pure Player App Web Interface
│   ├── app.js                       # Player UI, multi-sport pitch, wallet & 6-box OTP
│   ├── styles.css                   # Crimson & Gold player design system
│   ├── manifest.json                # Player PWA Web App Manifest
│   ├── admin.html                   # Dedicated Executive Admin Console Web Interface
│   ├── admin.js                     # Admin logic, telemetries, and live audio
│   ├── admin.css                    # Dark & Gold executive management theme
│   └── manifest-admin.json          # Admin PWA Web App Manifest
│
├── .github/workflows/
│   ├── build-apk.yml                # Automated GitHub Actions Cloud APK Builder
│   └── deploy-pages.yml             # Automated GitHub Pages Deployment
└── build_apks.bat                   # Local Windows APK build helper script
```

---

## 🚀 Getting Started

### Instant Web Access (PWA)
Play immediately via the live zero-error Web App:
- **Player App**: Open [https://rajnishmeenaa.github.io/dream11-fantasy-app/](https://rajnishmeenaa.github.io/dream11-fantasy-app/) in your browser ➔ Tap **Install App**
- **Admin Console**: Open [https://rajnishmeenaa.github.io/dream11-fantasy-app/admin.html](https://rajnishmeenaa.github.io/dream11-fantasy-app/admin.html) in your browser ➔ Tap **Install App**

---

## ☁️ Cloud Build: Automatic APK Compilation via GitHub Actions

This repository includes a pre-configured CI/CD workflow at `.github/workflows/build-apk.yml`.

### How to Build APKs in the Cloud:
1. Create a new repository on [GitHub](https://github.com/new).
2. Push your code:
   ```bash
   git remote add origin https://github.com/<YOUR-USERNAME>/<YOUR-REPO-NAME>.git
   git branch -M main
   git push -u origin main
   ```
3. GitHub Actions will automatically:
   - Spin up an Ubuntu runner with **Java 17** & **Android SDK 34**.
   - Build both APKs: `fantasy11-player-app-debug.apk` and `fantasy11-admin-console-debug.apk`.
   - Upload both binaries as downloadable artifacts under the **Actions** tab!

---

## 🛠️ Local Android Studio Compilation

1. Open **Android Studio**.
2. Select **Open Project** and navigate to:
   - `android/fantasy11-user-app` (Player App)
   - `android/fantasy11-admin-app` (Admin Console)
3. Click **Build** ➔ **Build Bundle(s) / APK(s)** ➔ **Build APK(s)**.
4. Output binaries are located at `app/build/outputs/apk/debug/`.
