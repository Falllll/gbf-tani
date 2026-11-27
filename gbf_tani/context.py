# gbf_tani/context.py
"""
Konteks per akun (per thread).

Mode 1 akun : tidak ada jendela terdaftar → screenshot & klik pakai layar penuh (perilaku lama).
Mode multi  : tiap akun jalan di thread sendiri dan terikat ke satu jendela browser.
              Semua koordinat di flows/game/vision RELATIF ke jendela itu; baru diubah
              ke koordinat layar (to_screen) tepat sebelum pyautogui dipanggil.
              Posisi jendela dibaca langsung dari Windows setiap kali dipakai,
              jadi jendela boleh digeser selama bot jalan.
"""
import threading

# Mouse & screenshot cuma satu → semua panggilan pyautogui antre lewat lock ini.
INPUT_LOCK = threading.RLock()

_local = threading.local()


def set_account(index, window):
    """Dipanggil sekali di awal thread akun. window = objek jendela dari gbf_tani.windows."""
    _local.index = index
    _local.window = window
    _local.state = {}


def region():
    """Area jendela akun ini (left, top, width, height) saat ini, None kalau mode 1 akun."""
    window = getattr(_local, "window", None)
    if window is None:
        return None
    return window.region()


def account_label():
    """'[Akun 2] ' di mode multi, '' di mode 1 akun."""
    index = getattr(_local, "index", None)
    return f"[Akun {index}] " if index else ""


def to_screen(x, y):
    """Koordinat relatif jendela → koordinat layar."""
    r = region()
    if r is None:
        return x, y
    return x + r[0], y + r[1]


def state():
    """Dict state milik akun ini (contoh: karakter terakhir yang dipilih di mode manual)."""
    if not hasattr(_local, "state"):
        _local.state = {}
    return _local.state
