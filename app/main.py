"""
Vocald - Entry Point
Module 1: App Shell + Screen Manager
"""

import os
import sys

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

# --- Safe imports with clear error logging ---
def _import_screens():
    try:
        from ui.screens.splash_screen       import SplashScreen
        from ui.screens.dashboard_screen    import DashboardScreen
        from ui.screens.speakers_screen     import SpeakersScreen
        from ui.screens.recordings_screen   import RecordingsScreen
        from ui.screens.queue_screen        import QueueScreen
        from ui.screens.folder_screen       import FolderScreen
        from ui.screens.settings_screen     import SettingsScreen
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
        (SplashScreen, DashboardScreen, SpeakersScreen,
         RecordingsScreen, QueueScreen, FolderScreen,
         SettingsScreen, SpeakerDetailScreen) = _import_screens()

        screens = [
            SplashScreen(name='splash'),
            DashboardScreen(name='dashboard'),
            SpeakersScreen(name='speakers'),
            RecordingsScreen(name='recordings'),
            QueueScreen(name='queue'),
            FolderScreen(name='folder'),
            SettingsScreen(name='settings'),
            SpeakerDetailScreen(name='speaker_detail'),
        ]
        for screen in screens:
            self.add_widget(screen)
        Logger.info(f"Vocald: {len(screens)} screens registered")

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
            # Return minimal fallback UI
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
            Logger.info("Vocald: Android permissions requested")
        except Exception as e:
            Logger.error(f"Vocald: Permission error: {e}")

    def on_start(self):
        Logger.info("Vocald: App started — transitioning to dashboard")
        Clock.schedule_once(self._finish_splash, 2.5)

    def _finish_splash(self, dt):
        self.sm.go_to('dashboard')

    def on_pause(self):
        return True

    def on_resume(self):
        Logger.info("Vocald: Resumed")

    def on_stop(self):
        Logger.info("Vocald: Stopped")


if __name__ == '__main__':
    VocaldApp().run()