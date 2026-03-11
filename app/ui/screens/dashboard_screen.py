"""
Vocald - Dashboard Screen
Module 1: Main hub showing stats + bottom navigation
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


class DashboardScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        root = BoxLayout(orientation='vertical')

        with root.canvas.before:
            Color(*get_color_from_hex('#0A0E1A'))
            self.bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda i, v: setattr(self.bg, 'pos', v),
                  size=lambda i, v: setattr(self.bg, 'size', v))

        root.add_widget(self._build_topbar())

        scroll = ScrollView(size_hint=(1, 1))
        content = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(16),
            padding=[dp(16), dp(16), dp(16), dp(16)],
        )
        content.bind(minimum_height=content.setter('height'))
        content.add_widget(self._build_status_banner())
        content.add_widget(self._build_stat_tiles())
        content.add_widget(self._build_section_header('Recent Activity'))
        for i in range(3):
            content.add_widget(self._build_activity_placeholder())
        scroll.add_widget(content)
        root.add_widget(scroll)

        root.add_widget(self._build_bottom_nav())
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
            halign='left',
            text_size=(None, None),
        ))
        bar.add_widget(Label(
            text='● ACTIVE',
            font_size=dp(11),
            color=get_color_from_hex('#00E676'),
            size_hint_x=None,
            width=dp(80),
        ))
        return bar

    def _build_status_banner(self):
        banner = BoxLayout(
            size_hint=(1, None),
            height=dp(64),
            padding=[dp(16), dp(12), dp(16), dp(12)],
            spacing=dp(12),
        )
        with banner.canvas.before:
            Color(*get_color_from_hex('#0D1F2D'))
            self._banner_bg = RoundedRectangle(
                pos=banner.pos, size=banner.size, radius=[dp(12)])
        banner.bind(
            pos=lambda i, v: self._redraw_rounded(i),
            size=lambda i, v: self._redraw_rounded(i),
        )
        self._banner_widget = banner

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

    def _redraw_rounded(self, instance):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(*get_color_from_hex('#0D1F2D'))
            RoundedRectangle(pos=instance.pos, size=instance.size, radius=[dp(12)])

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
            ('0', 'In Queue',              '#FFB300'),
            ('0', 'Failed',                '#FF3D57'),
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
            halign='left',
            text_size=(None, None),
        ))
        return box

    def _build_activity_placeholder(self):
        row = BoxLayout(
            size_hint=(1, None),
            height=dp(60),
            padding=[dp(14), dp(10), dp(14), dp(10)],
        )
        with row.canvas.before:
            Color(*get_color_from_hex('#111827'))
            self._row_bg = RoundedRectangle(
                pos=row.pos, size=row.size, radius=[dp(10)])
        row.bind(
            pos=lambda i, v: self._redraw_rounded(i),
            size=lambda i, v: self._redraw_rounded(i),
        )
        row.add_widget(Label(
            text='No recordings yet',
            font_size=dp(13),
            color=get_color_from_hex('#3D4A5C'),
        ))
        return row

    def _build_bottom_nav(self):
        nav = BoxLayout(size_hint=(1, None), height=dp(62))
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
        for icon, label, screen_name in nav_items:
            btn = Button(
                text=f'{icon}\n{label}',
                font_size=dp(10),
                background_color=(0, 0, 0, 0),
                color=get_color_from_hex('#00D4FF') if screen_name == 'dashboard'
                      else get_color_from_hex('#3D4A5C'),
            )
            btn.screen_name = screen_name
            btn.bind(on_release=self._on_nav)
            nav.add_widget(btn)
        return nav

    def _on_nav(self, btn):
        if self.manager:
            self.manager.go_to(btn.screen_name)


class StatTile(FloatLayout):

    def __init__(self, value, label, color, **kwargs):
        super().__init__(**kwargs)
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