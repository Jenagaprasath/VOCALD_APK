"""
Vocald - Splash Screen
Module 1: Animated loading screen shown on app launch
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.utils import get_color_from_hex


class SplashScreen(Screen):
    """Animated splash screen with Vocald branding."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        layout = FloatLayout()

        # Background
        with layout.canvas.before:
            Color(*get_color_from_hex('#0A0E1A'))
            self.bg_rect = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=self._update_bg, size=self._update_bg)

        # Center content
        center = BoxLayout(
            orientation='vertical',
            size_hint=(0.7, 0.3),
            pos_hint={'center_x': 0.5, 'center_y': 0.52},
            spacing=dp(12),
        )

        # App icon placeholder (waveform visual)
        icon_label = Label(
            text='◈',
            font_size=dp(56),
            color=get_color_from_hex('#00D4FF'),
            size_hint_y=None,
            height=dp(70),
            opacity=0,
        )
        icon_label.id = 'icon'

        # App name
        name_label = Label(
            text='VOCALD',
            font_size=dp(32),
            bold=True,
            color=get_color_from_hex('#F0F4FF'),
            letter_spacing=dp(6),
            size_hint_y=None,
            height=dp(45),
            opacity=0,
        )

        # Tagline
        tag_label = Label(
            text='Speaker Identification Engine',
            font_size=dp(13),
            color=get_color_from_hex('#8892A4'),
            size_hint_y=None,
            height=dp(20),
            opacity=0,
        )

        center.add_widget(icon_label)
        center.add_widget(name_label)
        center.add_widget(tag_label)
        layout.add_widget(center)

        # Version label bottom
        version_label = Label(
            text='v1.0.0  •  Offline Mode',
            font_size=dp(11),
            color=get_color_from_hex('#3D4A5C'),
            size_hint=(1, None),
            height=dp(30),
            pos_hint={'center_x': 0.5, 'y': 0.04},
        )
        layout.add_widget(version_label)

        # Loading bar
        self.loading_bar = LoadingBar(
            size_hint=(0.6, None),
            height=dp(3),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
        )
        layout.add_widget(self.loading_bar)

        self.add_widget(layout)

        # Store refs for animation
        self._icon = icon_label
        self._name = name_label
        self._tag = tag_label

    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def on_enter(self):
        """Start animations when screen is shown."""
        Clock.schedule_once(self._animate_in, 0.1)
        Clock.schedule_once(self._start_loading, 0.4)

    def _animate_in(self, dt):
        """Fade in branding elements with stagger."""
        anim_icon = Animation(opacity=1, duration=0.5)
        anim_name = Animation(opacity=1, duration=0.6)
        anim_tag  = Animation(opacity=1, duration=0.5)

        anim_icon.start(self._icon)
        Clock.schedule_once(lambda dt: anim_name.start(self._name), 0.2)
        Clock.schedule_once(lambda dt: anim_tag.start(self._tag), 0.4)

    def _start_loading(self, dt):
        """Animate loading bar."""
        self.loading_bar.start()


class LoadingBar(FloatLayout):
    """Animated teal loading bar."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._progress = 0
        with self.canvas:
            # Track
            Color(*get_color_from_hex('#1C2537'))
            self.track = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[dp(2)]
            )
            # Fill
            Color(*get_color_from_hex('#00D4FF'))
            self.fill = RoundedRectangle(
                pos=self.pos, size=(0, self.height), radius=[dp(2)]
            )
        self.bind(pos=self._update, size=self._update)

    def _update(self, *args):
        self.track.pos = self.pos
        self.track.size = self.size
        self.fill.pos = self.pos
        self.fill.size = (self.width * self._progress, self.height)

    def start(self):
        """Animate fill from 0 to 100%."""
        anim = Animation(_progress=1.0, duration=1.8)
        anim.bind(on_progress=lambda *a: self._update())
        anim.start(self)