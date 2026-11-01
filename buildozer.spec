
[app]

title = SORYA AI
package.name = sorya
package.domain = com.sorya

source.dir = .
source.include_exts = py,kv,png,jpg,atlas

version = 1.0

requirements = python3,kivy,requests

orientation = portrait
fullscreen = 0

android.permissions = INTERNET
android.api = 35
android.minapi = 24
android.archs = arm64-v8a

[buildozer]

log_level = 2
warn_on_root = 1
