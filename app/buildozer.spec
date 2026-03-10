[app]

# ── App Identity ───────────────────────────────────────────────────────────────
title = Vocald
package.name = vocald
package.domain = com.vocald

# ── Source ─────────────────────────────────────────────────────────────────────
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,db,onnx,ttf
source.include_patterns = assets/*, models/*, app/ui/kv/*
source.exclude_dirs = tests, bin, .git, .github, __pycache__, docs, scripts

# ── Version ────────────────────────────────────────────────────────────────────
version = 1.0.0

# ── Requirements ───────────────────────────────────────────────────────────────
# Core
requirements = python3,kivy==2.3.0,kivymd,pillow

# Audio processing
requirements += ,pydub,numpy

# ML / Speaker ID (added progressively per module)
# requirements += ,onnxruntime,scipy,scikit-learn

# Database
requirements += ,sqlite3

# ── Android ────────────────────────────────────────────────────────────────────
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,READ_CALL_LOG,FOREGROUND_SERVICE,RECEIVE_BOOT_COMPLETED,WAKE_LOCK,REQUEST_INSTALL_PACKAGES

android.api = 33
android.minapi = 29
android.ndk = 25b
android.sdk = 33
android.ndk_api = 21

android.archs = arm64-v8a, armeabi-v7a

# Enable AndroidX
android.enable_androidx = True
android.gradle_dependencies = androidx.work:work-runtime:2.8.1

# ── App Icon & Splash ──────────────────────────────────────────────────────────
# icon.filename = %(source.dir)s/assets/icons/vocald_icon.png
# presplash.filename = %(source.dir)s/assets/images/splash.png
presplash.color = #0A0E1A

# ── Orientation ────────────────────────────────────────────────────────────────
orientation = portrait

# ── Services (added in Module 8) ───────────────────────────────────────────────
# android.services = VocaldMonitor:app/monitoring/foreground_service.py:foreground

# ── Fullscreen ─────────────────────────────────────────────────────────────────
fullscreen = 0

# ── Log Level (set to 2 for production) ────────────────────────────────────────
log_level = 2

# ── Build ──────────────────────────────────────────────────────────────────────
[buildozer]
log_level = 2
warn_on_root = 1
