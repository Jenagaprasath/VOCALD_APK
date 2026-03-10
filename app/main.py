# Vocald - Entry Point
"""
Vocald - Automatic Speaker Identification App
Module 1: App Shell + Screen Manager + Navigation
"""

import os
import sys

# Android-specific setup
try:
    from android.permissions import request_permissions, Permission  # noqa
    ANDROID = True
except ImportError:
    ANDROID = False

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window
from kivy.utils import platform
from kivy.logger import Logger

# Import screens
from ui.screens.splash_screen import SplashScreen
from ui.screens.dashboard_screen import DashboardScreen
from ui.screens.speakers_screen import SpeakersScreen
from ui.screens.recordings_screen import RecordingsScreen
from ui.screens.queue_screen import QueueScreen
from ui.screens.folder_screen import FolderScreen
from ui.screens.settings_screen import SettingsScreen
from ui.screens.speaker_detail_screen import SpeakerDetailScreen

# Import theme
from ui.app_theme import VocaldTheme

# Import utils
from utils.logger import setup_logger
from utils.constants import APP_NAME, APP_VERSION


class VocaldScreenManager(ScreenManager):
    """Main screen manager for Vocald app."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = FadeTransition(duration=0.2)
        self._build_screens()

    def _build_screens(self):
        """Register all screens."""
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
        """Navigate to a screen by name."""
        if self.has_screen(screen_name):
            self.transition.direction = direction
            self.current = screen_name
        else:
            Logger.warning(f"Vocald: Screen '{screen_name}' not found")


class VocaldApp(App):
    """Main Vocald Application."""

    title = APP_NAME
    theme = None

    def build(self):
        """Build and return the root widget."""
        # Setup logging
        setup_logger()
        Logger.info(f"Vocald: Starting {APP_NAME} v{APP_VERSION}")

        # Apply theme
        self.theme = VocaldTheme()
        self.theme.apply()

        # Set window background (desktop testing)
        if platform != 'android':
            Window.size = (400, 750)
            Window.clearcolor = self.theme.bg_primary

        # Request Android permissions
        if ANDROID:
            self._request_permissions()

        # Build screen manager
        self.sm = VocaldScreenManager()
        return self.sm

    def _request_permissions(self):
        """Request required Android permissions."""
        try:
            from android.permissions import request_permissions, Permission
            permissions = [
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_CALL_LOG,
                Permission.FOREGROUND_SERVICE,
                Permission.RECEIVE_BOOT_COMPLETED,
            ]
            request_permissions(permissions)
            Logger.info("Vocald: Android permissions requested")
        except Exception as e:
            Logger.error(f"Vocald: Permission request failed: {e}")

    def on_start(self):
        """Called when app starts."""
        Logger.info("Vocald: App started")
        # Navigate to dashboard after splash
        from kivy.clock import Clock
        Clock.schedule_once(self._finish_splash, 2.5)

    def _finish_splash(self, dt):
        """Transition from splash to dashboard."""
        self.sm.go_to('dashboard')

    def on_pause(self):
        """Allow app to be paused on Android."""
        Logger.info("Vocald: App paused")
        return True

    def on_resume(self):
        """Called when app resumes from pause."""
        Logger.info("Vocald: App resumed")

    def on_stop(self):
        """Called when app stops."""
        Logger.info("Vocald: App stopped")


if __name__ == '__main__':
    VocaldApp().run()


    