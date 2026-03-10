[app]

title = Vocald
package.name = vocald
package.domain = com.vocald

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,ttf
source.exclude_dirs = tests,bin,.git,.github,__pycache__,docs,scripts

version = 1.0.0

requirements = python3,kivy==2.3.0,pillow,pydub,numpy

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,READ_CALL_LOG,FOREGROUND_SERVICE,RECEIVE_BOOT_COMPLETED,WAKE_LOCK

android.api = 33
android.minapi = 29
android.ndk = 25b
android.sdk = 33
android.ndk_api = 21

android.archs = arm64-v8a

android.enable_androidx = True

presplash.color = #0A0E1A

orientation = portrait

fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1