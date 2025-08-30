from utils.image_utils import screenshot, match_template, click_image, is_dark_region
import time


def ensure_event_tab():
    """Pastikan kita sudah di tab Event pada backup request."""
    print("ℹ️ Event belum aktif, pindah tab...")

    # Coba klik recent kalau ada
    if match_template(screenshot(), "assets/button/recent.png", threshold=0.7, preprocess=True):
        click_image("assets/button/recent.png", threshold=0.7)
        time.sleep(1)

    for _ in range(3):
        screen = screenshot()

        # cek apakah sudah di event aktif
        if match_template(screen, "assets/button/event_active.png", threshold=0.7, preprocess=True):
            print("✅ Sudah di tab Event (aktif)")
            return True

        # kalau belum aktif, coba klik event
        if match_template(screen, "assets/button/event.png", threshold=0.7, preprocess=True):
            click_image("assets/button/event.png", threshold=0.7)
            time.sleep(1)
            print("✅ Berhasil pindah ke tab Event")
            return True

        time.sleep(0.5)

    print("❌ Gagal menemukan tombol Event (cek asset event.png / resolusi / scaling)")
    return False


def ensure_raid_tab():
    """Pastikan kita sudah di tab Finder pada backup request."""
    print("ℹ️ Raid belum aktif, pindah tab...")

    # Loop beberapa kali untuk cari tombol
    for _ in range(3):
        screen = screenshot()

        # --- 1. Coba cari tombol aktif langsung ---
        coords_active = match_template(
            screen,
            "assets/button/finder_active.png",
            threshold=0.4,
            return_coords=True,
            preprocess=True
        )
        if coords_active:
            print("✅ Sudah di tab Finder (aktif)")
            return True

        # --- 2. Kalau ga ketemu aktif, cari yang normal ---
        coords_normal = match_template(
            screen,
            "assets/button/finder.png",
            threshold=0.4,
            return_coords=True,
            preprocess=True
        )
        if coords_normal:
            click_image("assets/button/finder.png", threshold=0.4)
            time.sleep(1)
            print("✅ Berhasil pindah ke tab Finder")
            return True

        time.sleep(0.5)

    print("❌ Gagal menemukan tombol Finder")
    return False
