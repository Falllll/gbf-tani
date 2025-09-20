# utils/image.py
import time
import logging
from utils.screenshot import screenshot, match_template

def wait_for_image(template_path: str, check_interval: float = 2.0,
                   threshold: float = 0.7, timeout: float = None) -> bool:
    """
    Tunggu hingga template/gambar tertentu muncul di layar.
    :param template_path: Path template gambar.
    :param check_interval: Jeda pengecekan antar loop (detik).
    :param threshold: Skor minimal match.
    :param timeout: Batas waktu tunggu (detik), None = tanpa batas.
    :return: True jika ditemukan, False jika timeout.
    """
    start = time.time()
    while True:
        screen = screenshot()
        if match_template(screen, template_path, threshold=threshold):
            logging.info(f"✅ Template ditemukan: {template_path}")
            return True

        if timeout and (time.time() - start) > timeout:
            logging.warning(f"❌ Timeout menunggu template: {template_path}")
            return False

        time.sleep(check_interval)


def check_image_once(template_path: str, threshold: float = 0.7) -> bool:
    """
    Cek sekali apakah template ada di layar.
    :param template_path: Path template gambar.
    :param threshold: Skor minimal match.
    :return: True jika match, False jika tidak.
    """
    screen = screenshot()
    found = match_template(screen, template_path, threshold=threshold)
    logging.debug(f"Check image {template_path} → {found}")
    return found
