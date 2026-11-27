# gbf_tani/session.py
"""Info sesi bot yang sedang jalan: waktu mulai, lama jalan, dan cara berhenti."""
import sys
import threading
import time
from datetime import datetime, timedelta, timezone

from gbf_tani.log import log

GMT7 = timezone(timedelta(hours=7))

# Di-set kalau SEMUA akun harus berhenti (error di salah satu akun).
STOP = threading.Event()

_start_time = None
_paused_total = 0.0     # total detik istirahat humanizer yang sudah selesai
_pause_started = None   # waktu mulai istirahat yang sedang berjalan (None kalau tidak istirahat)


def start():
    """Catat waktu mulai. Dipanggil sekali di awal main()."""
    global _start_time
    _start_time = time.time()


def elapsed_seconds():
    """Detik sejak start() dipanggil (termasuk istirahat)."""
    return time.time() - _start_time


def begin_pause():
    """Humanizer mulai istirahat → waktu aktif berhenti dihitung."""
    global _pause_started
    _pause_started = time.time()


def end_pause():
    """Humanizer selesai istirahat → waktu aktif lanjut dihitung."""
    global _paused_total, _pause_started
    if _pause_started is not None:
        _paused_total += time.time() - _pause_started
        _pause_started = None


def active_seconds():
    """Detik bot benar-benar jalan sejak start() (waktu istirahat humanizer tidak dihitung)."""
    paused = _paused_total
    if _pause_started is not None:
        paused += time.time() - _pause_started
    return elapsed_seconds() - paused


def format_duration(seconds):
    """3725 → '01:02:05' (jam:menit:detik)."""
    seconds = int(seconds)
    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def now_gmt7():
    """Waktu sekarang dalam GMT+7, contoh: '2026-11-27 16:33:05'."""
    return datetime.now(GMT7).strftime("%Y-%m-%d %H:%M:%S")


def stop_for_captcha():
    """
    Captcha muncul → print jam (GMT+7) dan total run time, lalu berhenti.
    Mode 1 akun: program berhenti.
    Mode multi : cuma akun yang kena captcha yang berhenti, akun lain tetap jalan.
    """
    log("⚠️ CAPTCHA terdeteksi → bot berhenti.")
    log(f"🕒 Waktu        : {now_gmt7()} (GMT+7)")
    log(f"⏱️ Total run time: {format_duration(elapsed_seconds())}")
    sys.exit()
