# gbf_tani/humanizer.py
"""
Humanizer: bot jalan acak WORK_MIN–WORK_MAX, lalu istirahat acak REST_MIN–REST_MAX, diulang terus.
Istirahat hanya dimulai di sela putaran (tidak pernah di tengah battle).

1 akun : loop utama memanggil should_rest() lalu rest() sebelum tiap putaran.
Multi  : thread akun memanggil checkpoint() sebelum tiap putaran; main thread memanggil
         supervise() — begitu waktunya, semua akun ditahan di checkpoint, lalu istirahat bareng.
"""
import random
import threading
import time
from datetime import datetime, timedelta

from gbf_tani import session
from gbf_tani.session import GMT7

# Durasi dalam detik
WORK_MIN, WORK_MAX = 30 * 60, 60 * 60   # jalan 30–60 menit
REST_MIN, REST_MAX = 30 * 60, 60 * 60   # istirahat 30–60 menit

_POLL = 0.5  # detik, seberapa sering cek timer/stop selama nunggu


def _minutes(seconds):
    return round(seconds / 60)


def _clock_after(seconds):
    return (datetime.now(GMT7) + timedelta(seconds=seconds)).strftime("%H:%M")


class Humanizer:
    def __init__(self):
        self._rest_at = None
        self._cond = threading.Condition()
        self._hold = False        # True = akun harus berhenti di checkpoint
        self._paused = 0          # jumlah akun yang sedang ditahan
        self._generation = 0      # naik tiap kali istirahat selesai

    # --- jadwal -------------------------------------------------------------

    def schedule_next(self):
        """Mulai periode jalan baru (acak WORK_MIN–WORK_MAX)."""
        work = random.uniform(WORK_MIN, WORK_MAX)
        self._rest_at = time.time() + work
        return work

    def should_rest(self):
        return self._rest_at is not None and time.time() >= self._rest_at

    def _rest_for(self, stop_check):
        """
        Istirahat acak REST_MIN–REST_MAX sambil terus cek stop_check().
        Return True kalau istirahat selesai normal, False kalau stop_check() minta berhenti.
        """
        rest = random.uniform(REST_MIN, REST_MAX)
        print(f"😴 Humanizer: istirahat {_minutes(rest)} menit (lanjut sekitar jam {_clock_after(rest)} GMT+7)")
        session.begin_pause()  # timer berhenti selama istirahat
        try:
            end = time.time() + rest
            while time.time() < end:
                if stop_check():
                    return False
                time.sleep(min(_POLL, end - time.time()))
        finally:
            session.end_pause()
        work = self.schedule_next()
        print(f"▶️ Humanizer: lanjut jalan, istirahat berikutnya dalam {_minutes(work)} menit")
        return True

    # --- 1 akun -------------------------------------------------------------

    def rest(self, stop_check):
        """Dipanggil loop utama mode 1 akun kalau should_rest()."""
        return self._rest_for(stop_check)

    # --- multi akun ---------------------------------------------------------

    def checkpoint(self, stop_event):
        """Dipanggil thread akun sebelum tiap putaran. Kalau sedang istirahat, tahan di sini."""
        with self._cond:
            if not self._hold:
                return
            self._paused += 1
            self._cond.notify_all()
            generation = self._generation
            while self._generation == generation and not stop_event.is_set():
                self._cond.wait(timeout=_POLL)
            self._paused -= 1

    def supervise(self, alive_count, stop_check):
        """
        Dipanggil main thread mode multi di tiap loop.
        Kalau waktunya istirahat: tahan semua akun, tunggu semuanya selesai putaran, istirahat, lanjut.
        Return False kalau stop_check() minta berhenti (timer habis / error).
        """
        if not self.should_rest():
            return True

        print("⏸️ Humanizer: waktunya istirahat, nunggu semua akun selesai putarannya...")
        with self._cond:
            self._hold = True
            while self._paused < alive_count():
                if stop_check():
                    return False
                self._cond.wait(timeout=_POLL)

        finished = self._rest_for(stop_check)

        with self._cond:
            self._hold = False
            self._generation += 1
            self._cond.notify_all()
        return finished
