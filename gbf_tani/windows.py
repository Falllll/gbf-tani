# gbf_tani/windows.py
"""
Cari jendela browser game lewat Windows (pygetwindow, ikut ter-install bersama pyautogui).
Posisi dicatat SEKALI saat bot start, lalu dipakai terus — jendela jangan digeser selama bot jalan.
"""
import ctypes

import pyautogui  # import duluan: pyautogui mengaktifkan DPI awareness, jadi koordinat jendela = koordinat klik
import pygetwindow

# Judul tab game. Judul jendela Chrome = "<judul tab aktif> - Google Chrome"
GAME_TITLE = "Granblue Fantasy"

# DwmGetWindowAttribute: jendela "cloaked" = ada tapi tidak tampil (virtual desktop lain, dll.)
_DWMWA_CLOAKED = 14


class GameWindow:
    """Satu jendela game dengan area yang dicatat saat start."""

    def __init__(self, title, left, top, width, height):
        self.title = title
        self._region = (left, top, width, height)

    def region(self):
        """(left, top, width, height) di layar."""
        return self._region

    def describe(self):
        left, top, width, height = self._region
        return f"x={left}, y={top} ({width}×{height}) — {self.title}"


def _is_game_title(title):
    return title == GAME_TITLE or title.startswith(GAME_TITLE + " - ")


def _is_cloaked(win):
    """True kalau Windows menyembunyikan jendela ini (misalnya ada di virtual desktop lain)."""
    hwnd = getattr(win, "_hWnd", None)
    if hwnd is None:
        return False
    try:
        cloaked = ctypes.c_int(0)
        result = ctypes.windll.dwmapi.DwmGetWindowAttribute(
            ctypes.c_void_p(hwnd), _DWMWA_CLOAKED, ctypes.byref(cloaked), ctypes.sizeof(cloaked)
        )
        return result == 0 and cloaked.value != 0
    except (AttributeError, OSError):
        return False


def _clip_to_screen(win):
    """Potong area jendela ke batas layar utama (jendela bisa sedikit keluar layar karena border Windows)."""
    screen_w, screen_h = pyautogui.size()
    left = max(0, win.left)
    top = max(0, win.top)
    right = min(screen_w, win.left + win.width)
    bottom = min(screen_h, win.top + win.height)
    return left, top, right - left, bottom - top


def find_game_windows():
    """
    Jendela game yang benar-benar tampil di layar utama, urut dari kiri ke kanan → Akun 1, 2, 3, ...
    Diabaikan: jendela di-minimize, di virtual desktop lain, atau di luar layar utama.
    """
    found = []
    for win in pygetwindow.getAllWindows():
        if not _is_game_title(win.title) or win.isMinimized or _is_cloaked(win):
            continue
        left, top, width, height = _clip_to_screen(win)
        if width > 0 and height > 0:
            found.append(GameWindow(win.title, left, top, width, height))

    found.sort(key=lambda w: (w.region()[0], w.region()[1]))
    return found
