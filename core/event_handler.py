from utils.image_utils import screenshot, match_template, click_image, is_dark_region
import time


def ensure_event_tab():
    """Pastikan kita sudah di tab Event pada backup request."""
    print("ℹ️ Event belum aktif, pindah tab...")

    if match_template(screenshot(), "assets/button/recent.png", threshold=0.85):
        click_image("assets/button/recent.png", threshold=0.85)
        time.sleep(1)

    for _ in range(3):
        screen = screenshot()
        coords = match_template(screen, "assets/button/event.png", threshold=0.4, return_coords=True)

        if coords:
            x, y, conf = coords

            if is_dark_region(screen, (x, y)):  # sudah aktif
                print("✅ Sudah di tab Event (aktif)")
                return True
            else:
                click_image("assets/button/event.png", threshold=0.4)
                time.sleep(1)
                print("✅ Berhasil pindah ke tab Event")
                return True

        time.sleep(0.5)

    print("❌ Gagal menemukan tombol event")
    return False
