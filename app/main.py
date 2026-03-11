"""
Vocald - Entry Point
Module 1: App Shell + Screen Manager
"""

import os
import sys

# ── Pre-create .kivy dirs BEFORE Kivy initialises ──────────────────────────
# Kivy 2.3.0 on Android tries shutil.copytree into .kivy/icon/ on first run.
# If the dir already exists the copy is skipped; if it doesn't exist the
# parent must exist so makedirs can create it. Either way we need both dirs.
try:
    _files_dir = os.environ.get('ANDROID_APP_PATH',
                  os.path.join(os.path.expanduser('~'), '.kivy'))
    # On Android, HOME == /data/user/0/<pkg>/files/app
    _kivy_dir   = os.path.join(os.path.expanduser('~'), '.kivy')
    _icon_dir   = os.path.join(_kivy_dir, 'icon')
    _logs_dir   = os.path.join(_kivy_dir, 'logs')
    for _d in (_kivy_dir, _icon_dir, _logs_dir):
        os.makedirs(_d, exist_ok=True)
except Exception as _e:
    pass  # Non-fatal; Kivy will try again itself

# ── Monkey-patch shutil.copytree so icon-copy errors are non-fatal ──────────
import shutil as _shutil
_orig_copytree = _shutil.copytree

def _safe_copytree(src, dst, **kwargs):
    try:
        return _orig_copytree(src, dst, **kwargs)
    except (_shutil.Error, OSError, PermissionError):
        pass  # Already exists or permission denied — both are fine
_shutil.copytree = _safe_copytree
# ────────────────────────────────────────────────────────────────────────────

try:
    from android.permissions import request_permissions, Permission
    ANDROID = True
except ImportError:
    ANDROID = False

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window
from kivy.utils import platform
from kivy.logger import Logger
from kivy.clock import Clock


def _import_screens():
    try:
        from ui.screens.splash_screen         import SplashScreen
        from ui.screens.dashboard_screen      import DashboardScreen
        from ui.screens.speakers_screen       import SpeakersScreen
        from ui.screens.recordings_screen     import RecordingsScreen
        from ui.screens.queue_screen          import QueueScreen
        from ui.screens.folder_screen         import FolderScreen
        from ui.screens.settings_screen       import SettingsScreen
        from ui.screens.speaker_detail_screen import SpeakerDetailScreen
        Logger.info("Vocald: All screens imported OK")
        return (SplashScreen, DashboardScreen, SpeakersScreen,
                RecordingsScreen, QueueScreen, FolderScreen,
                SettingsScreen, SpeakerDetailScreen)
    except Exception as e:
        Logger.error(f"Vocald: Screen import FAILED: {e}")
        import traceback
        Logger.error(traceback.format_exc())
        raise


class VocaldScreenManager(ScreenManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = FadeTransition(duration=0.2)
        self._build_screens()

    def _build_screens(self):
        screens_cls = _import_screens()
        names = ('splash', 'dashboard', 'speakers', 'recordings',
                 'queue', 'folder', 'settings', 'speaker_detail')
        for cls, name in zip(screens_cls, names):
            self.add_widget(cls(name=name))
        Logger.info(f"Vocald: {len(names)} screens registered")

    def go_to(self, screen_name, direction='left'):
        if self.has_screen(screen_name):
            self.transition.direction = direction
            self.current = screen_name
        else:
            Logger.warning(f"Vocald: Screen '{screen_name}' not found")


class VocaldApp(App):

    title = 'Vocald'

    def build(self):
        Logger.info("Vocald: Build starting...")

        if platform != 'android':
            Window.size = (400, 750)
            Window.clearcolor = (0.04, 0.055, 0.1, 1)

        if ANDROID:
            self._request_permissions()

        try:
            self.sm = VocaldScreenManager()
            Logger.info("Vocald: ScreenManager built OK")
            return self.sm
        except Exception as e:
            Logger.error(f"Vocald: Build FAILED: {e}")
            import traceback
            Logger.error(traceback.format_exc())
            from kivy.uix.label import Label
            return Label(
                text=f'Vocald startup error:\n{e}',
                color=(1, 0.3, 0.3, 1),
            )

    def _request_permissions(self):
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.FOREGROUND_SERVICE,
                Permission.RECEIVE_BOOT_COMPLETED,
            ])
        except Exception as e:
            Logger.error(f"Vocald: Permission error: {e}")

    def on_start(self):
        Logger.info("Vocald: App started — transitioning to dashboard")
        Clock.schedule_once(self._finish_splash, 2.5)

    def _finish_splash(self, dt):
        if hasattr(self, 'sm'):
            self.sm.go_to('dashboard')

    def on_pause(self):
        return True

    def on_resume(self):
        Logger.info("Vocald: Resumed")

    def on_stop(self):
        Logger.info("Vocald: Stopped")


if __name__ == '__main__':
    VocaldApp().run()