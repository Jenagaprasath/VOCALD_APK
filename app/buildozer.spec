[app]

title = Vocald
package.name = vocald
package.domain = com.vocald

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,ttf
source.exclude_dirs = tests,bin,.git,.github,__pycache__,docs,scripts

version = 1.0.1

requirements = python3,kivy==2.3.0,pillow,numpy

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,FOREGROUND_SERVICE,RECEIVE_BOOT_COMPLETED,WAKE_LOCK

# API 33 = target (what features we use)
android.api = 33

# minapi MUST match ndk_api to avoid mismatch error
android.minapi = 21
android.ndk_api = 21

android.ndk = 25b
android.build_tools_version = 34.0.0

android.archs = arm64-v8a

android.enable_androidx = True

presplash.color = #0A0E1A

orientation = portrait

fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1