"""
Vocald App Theme
Dark forensic/intelligence aesthetic — deep navy, electric teal, sharp whites
"""

from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.metrics import dp


class VocaldTheme:
    """
    Central theme definition for Vocald.
    Dark intelligence-grade aesthetic.
    """

    # ── Primary Palette ────────────────────────────────────────────
    bg_primary      = get_color_from_hex('#0A0E1A')   # Deep navy black
    bg_secondary    = get_color_from_hex('#111827')   # Card background
    bg_tertiary     = get_color_from_hex('#1C2537')   # Elevated surface

    # ── Accent Colors ──────────────────────────────────────────────
    accent_primary  = get_color_from_hex('#00D4FF')   # Electric teal
    accent_success  = get_color_from_hex('#00E676')   # Green - identified
    accent_warning  = get_color_from_hex('#FFB300')   # Amber - processing
    accent_danger   = get_color_from_hex('#FF3D57')   # Red - error/unknown
    accent_purple   = get_color_from_hex('#7C4DFF')   # Purple - AI/ML

    # ── Text Colors ────────────────────────────────────────────────
    text_primary    = get_color_from_hex('#F0F4FF')   # Near white
    text_secondary  = get_color_from_hex('#8892A4')   # Muted grey-blue
    text_disabled   = get_color_from_hex('#3D4A5C')   # Disabled

    # ── Border / Divider ───────────────────────────────────────────
    border_color    = get_color_from_hex('#1E2D42')
    divider_color   = get_color_from_hex('#162030')

    # ── Spacing & Sizing ───────────────────────────────────────────
    padding_xs      = dp(4)
    padding_sm      = dp(8)
    padding_md      = dp(16)
    padding_lg      = dp(24)
    padding_xl      = dp(32)

    radius_sm       = dp(6)
    radius_md       = dp(12)
    radius_lg       = dp(20)

    # ── Typography ─────────────────────────────────────────────────
    font_heading    = 'Roboto'
    font_body       = 'Roboto'
    font_mono       = 'RobotoMono'

    size_h1         = dp(28)
    size_h2         = dp(22)
    size_h3         = dp(18)
    size_body       = dp(14)
    size_caption    = dp(12)
    size_tiny       = dp(10)

    # ── Nav Bar ────────────────────────────────────────────────────
    nav_height      = dp(60)
    nav_bg          = get_color_from_hex('#0D1220')

    # ── Status colors map ──────────────────────────────────────────
    STATUS_COLORS = {
        'identified':  get_color_from_hex('#00E676'),
        'unknown':     get_color_from_hex('#FF3D57'),
        'processing':  get_color_from_hex('#FFB300'),
        'queued':      get_color_from_hex('#8892A4'),
        'failed':      get_color_from_hex('#FF3D57'),
    }

    def apply(self):
        """Apply global window theme."""
        Window.clearcolor = self.bg_primary

    @staticmethod
    def hex(color_hex: str):
        """Convert hex string to Kivy color tuple."""
        return get_color_from_hex(color_hex)

    @staticmethod
    def with_alpha(color: tuple, alpha: float) -> tuple:
        """Return color with custom alpha."""
        return (color[0], color[1], color[2], alpha)