"""
Vocald - Dashboard Screen
Module 1: Main hub showing stats overview + bottom navigation
"""

from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.clock import Clock


class DashboardScreen(Screen):
    """Main dashboard — stats + quick actions + bottom nav."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        root = BoxLayout(orientation='vertical')

        # ── Top bar ───────────────────────────────────────────────
        root.add_widget(self._build_topbar())

        # ── Scrollable content ────────────────────────────────────
        scroll = ScrollView(size_hint=(1, 1))
        content = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(16),
            padding=[dp(16), dp(16), dp(16), dp(16)],
        )
        content.bind(minimum_height=content.setter('height'))

        # Status banner
        content.add_widget(self._build_status_banner())

        # Stat tiles row
        content.add_widget(self._build_stat_tiles())

        # Recent activity header
        content.add_widget(self._build_section_header('Recent Activity'))

        # Placeholder activity items
        for i in range(3):
            content.add_widget(self._build_activity_placeholder(i))

        scroll.add_widget(content)
        root.add_widget(scroll)

        # ── Bottom navigation ─────────────────────────────────────
        root.add_widget(self._build_bottom_nav())

        # Background
        with root.canvas.before:
            Color(*get_color_from_hex('#0A0E1A'))
            self.bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda i, v: setattr(self.bg, 'pos', v),
                  size=lambda i, v: setattr(self.bg, 'size', v))

        self.add_widget(root)

    def _build_topbar(self):
        bar = BoxLayout(
            size_hint=(1, None),
            height=dp(60),
            padding=[dp(16), 0, dp(16), 0],
        )
        with bar.canvas.before:
            Color(*get_color_from_hex('#0D1220'))
            self._topbar_bg = Rectangle(pos=bar.pos, size=bar.size)
        bar.bind(pos=lambda i, v: setattr(self._topbar_bg, 'pos', v),
                 size=lambda i, v: setattr(self._topbar_bg, 'size', v))

        bar.add_widget(Label(
            text='VOCALD',
            font_size=dp(20),
            bold=True,
            color=get_color_from_hex('#F0F4FF'),
            letter_spacing=dp(3),
            halign='left',
            text_size=(None, None),
        ))

        # Status dot
        status = Label(
            text='● ACTIVE',
            font_size=dp(11),
            color=get_color_from_hex('#00E676'),
            size_hint_x=None,
            width=dp(80),
            halign='right',
        )
        bar.add_widget(status)
        return bar

    def _build_status_banner(self):
        """Monitoring status card."""
        banner = BoxLayout(
            size_hint=(1, None),
            height=dp(64),
            padding=[dp(16), dp(12), dp(16), dp(12)],
            spacing=dp(12),
        )
        with banner.canvas.before:
            Color(*get_color_from_hex('#0D1F2D'))
            RoundedRectangle(pos=banner.pos, size=banner.size, radius=[dp(12)])
            Color(*get_color_from_hex('#00D4FF'))
            Line(
                rounded_rectangle=(banner.x, banner.y,
                                   banner.width, banner.height, dp(12)),
                width=dp(1)
            )
        banner.bind(
            pos=self._redraw_banner,
            size=self._redraw_banner,
        )
        self._banner = banner

        banner.add_widget(Label(
            text='◈',
            font_size=dp(24),
            color=get_color_from_hex('#00D4FF'),
            size_hint_x=None,
            width=dp(36),
        ))

        info = BoxLayout(orientation='vertical', spacing=dp(2))
        info.add_widget(Label(
            text='Monitoring: Not configured',
            font_size=dp(13),
            bold=True,
            color=get_color_from_hex('#F0F4FF'),
            halign='left',
            text_size=(None, None),
        ))
        info.add_widget(Label(
            text='Tap to select a folder',
            font_size=dp(11),
            color=get_color_from_hex('#8892A4'),
            halign='left',
            text_size=(None, None),
        ))
        banner.add_widget(info)
        return banner

    def _redraw_banner(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(*get_color_from_hex('#0D1F2D'))
            RoundedRectangle(pos=instance.pos, size=instance.size, radius=[dp(12)])
            Color(*get_color_from_hex('#00D4FF'))
            Line(
                rounded_rectangle=(instance.x, instance.y,
                                   instance.width, instance.height, dp(12)),
                width=dp(1)
            )

    def _build_stat_tiles(self):
        grid = GridLayout(
            cols=2,
            size_hint=(1, None),
            height=dp(160),
            spacing=dp(10),
        )

        stats = [
            ('0', 'Speakers\nIdentified', '#00D4FF'),
            ('0', 'Recordings\nProcessed', '#00E676'),
            ('0', 'In Queue',             '#FFB300'),
            ('0', 'Failed',               '#FF3D57'),
        ]

        for value, label, color in stats:
            grid.add_widget(StatTile(value=value, label=label, color=color))

        return grid

    def _build_section_header(self, title):
        box = BoxLayout(size_hint=(1, None), height=dp(32))
        box.add_widget(Label(
            text=title.upper(),
            font_size=dp(11),
            color=get_color_from_hex('#8892A4'),
            letter_spacing=dp(2),
            halign='left',
            text_size=(None, None),
        ))
        return box

    def _build_activity_placeholder(self, index):
        """Placeholder activity row."""
        row = BoxLayout(
            size_hint=(1, None),
            height=dp(60),
            padding=[dp(14), dp(10), dp(14), dp(10)],
            spacing=dp(12),
        )
        with row.canvas.before:
            Color(*get_color_from_hex('#111827'))
            RoundedRectangle(pos=row.pos, size=row.size, radius=[dp(10)])
        row.bind(
            pos=lambda i, v: self._redraw_card(i),
            size=lambda i, v: self._redraw_card(i),
        )

        row.add_widget(Label(
            text='—',
            font_size=dp(13),
            color=get_color_from_hex('#3D4A5C'),
        ))
        row.add_widget(Label(
            text='No recordings yet',
            font_size=dp(13),
            color=get_color_from_hex('#3D4A5C'),
        ))
        return row

    def _redraw_card(self, instance):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(*get_color_from_hex('#111827'))
            RoundedRectangle(pos=instance.pos, size=instance.size, radius=[dp(10)])

    def _build_bottom_nav(self):
        """Bottom navigation bar."""
        nav = BoxLayout(
            size_hint=(1, None),
            height=dp(62),
        )
        with nav.canvas.before:
            Color(*get_color_from_hex('#0D1220'))
            self._nav_bg = Rectangle(pos=nav.pos, size=nav.size)
        nav.bind(pos=lambda i, v: setattr(self._nav_bg, 'pos', v),
                 size=lambda i, v: setattr(self._nav_bg, 'size', v))

        nav_items = [
            ('⊞', 'Home',       'dashboard'),
            ('◉', 'Speakers',   'speakers'),
            ('▤', 'Recordings', 'recordings'),
            ('◎', 'Queue',      'queue'),
            ('⚙', 'Settings',   'settings'),
        ]

        for icon, label, screen in nav_items:
            btn = NavButton(icon=icon, label=label, screen=screen,
                            active=(screen == 'dashboard'))
            btn.bind(on_release=self._on_nav)
            nav.add_widget(btn)

        return nav

    def _on_nav(self, btn):
        self.manager.go_to(btn.screen)


class StatTile(FloatLayout):
    """Individual stat tile widget."""

    def __init__(self, value, label, color, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)

        with self.canvas.before:
            Color(*get_color_from_hex('#111827'))
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
        self.bind(pos=self._redraw, size=self._redraw)

        inner = BoxLayout(
            orientation='vertical',
            padding=[dp(14), dp(12), dp(14), dp(12)],
            spacing=dp(4),
        )

        inner.add_widget(Label(
            text=value,
            font_size=dp(30),
            bold=True,
            color=get_color_from_hex(color),
            halign='left',
            text_size=(None, None),
        ))
        inner.add_widget(Label(
            text=label,
            font_size=dp(11),
            color=get_color_from_hex('#8892A4'),
            halign='left',
            text_size=(None, None),
        ))
        self.add_widget(inner)

    def _redraw(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size


class NavButton(BoxLayout):
    """Bottom nav button."""

    def __init__(self, icon, label, screen, active=False, **kwargs):
        super().__init__(**kwargs)
        self.screen = screen
        self.orientation = 'vertical'
        self.size_hint_x = 1
        self.spacing = dp(2)
        self.padding = [0, dp(8), 0, dp(4)]

        color = get_color_from_hex('#00D4FF') if active else get_color_from_hex('#3D4A5C')

        self.icon_lbl = Label(
            text=icon,
            font_size=dp(20),
            color=color,
            size_hint_y=None,
            height=dp(26),
        )
        self.text_lbl = Label(
            text=label,
            font_size=dp(9),
            color=color,
            size_hint_y=None,
            height=dp(14),
        )
        self.add_widget(self.icon_lbl)
        self.add_widget(self.text_lbl)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            return True

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.dispatch('on_release')
            return True

    def register_event_type(self, *args):
        pass

    def __init_subclass__(cls, **kwargs):
        pass