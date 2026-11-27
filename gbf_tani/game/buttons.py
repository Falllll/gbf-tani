# gbf_tani/game/buttons.py
import time

from gbf_tani import assets
from gbf_tani.vision.capture import screenshot
from gbf_tani.vision.matcher import match_template, find_image
from gbf_tani.vision.mouse import click_image


# ---------------------------------------------------------------------------
# Cek dulu (preprocess), kalau kelihatan baru klik
# ---------------------------------------------------------------------------

def _click_if_visible(button, label, wait):
    """Cek tombol di screenshot baru (threshold 0.4), klik kalau ada, lalu tunggu."""
    if match_template(screenshot(), button, threshold=0.4, preprocess=True):
        print(label)
        click_image(button, threshold=0.4)
        time.sleep(wait)
        return True
    return False


def button_refresh():
    """
    Klik tombol refresh kalau ada.
    NOTE: selalu return False (perilaku lama dipertahankan) — caller tidak pernah `continue` karena ini.
    """
    _click_if_visible(assets.BTN_REFRESH, "🔄 Tombol refresh ditemukan, klik untuk refresh layar...", wait=1)
    return False


def button_reload():
    """Klik tombol reload kalau ada. Return True kalau diklik."""
    return _click_if_visible(assets.BTN_RELOAD, "🔄 Tombol reload ditemukan, klik untuk refresh layar...", wait=2)


def button_bookmark():
    """Klik tombol bookmark kalau ada. Return True kalau diklik."""
    return _click_if_visible(assets.BTN_BOOKMARK, "🔖 Tombol bookmark ditemukan, klik untuk balik ke bookmark...", wait=2)


# ---------------------------------------------------------------------------
# Klik langsung (tanpa cek preprocess)
# ---------------------------------------------------------------------------

def click_bookmark():
    return click_image(assets.BTN_BOOKMARK, threshold=0.7)


def click_back(threshold=0.5):
    return click_image(assets.BTN_BACK, threshold=threshold)


def click_auto_button(debug=False):
    return click_image(assets.BTN_AUTO, threshold=0.8, debug=debug)


def click_reload_button(debug=False):
    """Dipakai mode manual buat 'refresh' setelah aksi (klik reload.png)."""
    return click_image(assets.BTN_RELOAD, threshold=0.8, debug=debug)


def click_ok_button(debug=False):
    return click_image(assets.BTN_OK, threshold=0.8, debug=debug)


def click_quick_summon_button(debug=True):
    """Klik tombol quick summon (coba quick_summon.png lalu quick_summon2.png)."""
    for path in (assets.BTN_QUICK_SUMMON, assets.BTN_QUICK_SUMMON_2):
        result = click_image(path, threshold=0.8, debug=debug)
        if result:
            return result

    if debug:
        print("[DEBUG] quick_summon button tidak ditemukan")
    return None


# ---------------------------------------------------------------------------
# Kombinasi reset
# ---------------------------------------------------------------------------

def reload_then_bookmark(delay=0.3):
    """Klik reload lalu bookmark (tanpa cek dulu)."""
    click_image(assets.BTN_RELOAD, threshold=0.7)
    time.sleep(delay)
    click_bookmark()


def reset_to_bookmark():
    """Reload (kalau tombolnya ada), tunggu 1 detik, lalu klik bookmark."""
    button_reload()
    time.sleep(1)
    click_bookmark()


# ---------------------------------------------------------------------------
# Tunggu
# ---------------------------------------------------------------------------

def wait_for_auto_button(timeout=30, interval=0.5, debug=False):
    """Tunggu sampai tombol auto muncul. Return True kalau ketemu, False kalau timeout."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if find_image(assets.BTN_AUTO, threshold=0.8, debug=debug):
            if debug:
                print("✅ Tombol auto muncul!")
            return True
        time.sleep(interval)

    if debug:
        print("❌ Tombol auto tidak ketemu setelah timeout")
    return False
