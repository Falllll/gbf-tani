import threading
import time
import traceback

from gbf_tani import context, session
from gbf_tani.config import accounts, humanizer, mode, timer, timer_seconds
from gbf_tani.flows.navigator import check_tab
from gbf_tani.humanizer import Humanizer
from gbf_tani.log import log


def main():
    print("🚀 Bot start...")
    if timer:
        note = " jalan (waktu istirahat humanizer tidak dihitung)" if humanizer else ""
        print(f"⏱️ Timer aktif: bot berhenti setelah {timer_seconds / 3600:g} jam{note}")

    rest = Humanizer() if humanizer else None

    if accounts == 1:
        session.start()
        _start_humanizer(rest)
        run_single(rest)
    else:
        run_multi(rest)


def _start_humanizer(rest):
    if rest:
        work = rest.schedule_next()
        print(f"🧍 Humanizer aktif: istirahat pertama dalam {round(work / 60)} menit")


def _timer_done():
    # active_seconds() = elapsed_seconds() kalau humanizer mati (tidak pernah ada istirahat)
    return timer and session.active_seconds() >= timer_seconds


def _print_limit():
    print(f"Runtime limit reached ({timer_seconds / 3600:g} hours). Exiting.")


# ---------------------------------------------------------------------------
# 1 akun: layar penuh, satu loop (perilaku lama)
# ---------------------------------------------------------------------------

def run_single(rest=None):
    while True:
        if _timer_done():
            _print_limit()
            break
        if rest and rest.should_rest():
            rest.rest(stop_check=lambda: False)  # timer tidak jalan selama istirahat
        check_tab(mode)


# ---------------------------------------------------------------------------
# Multi akun: satu thread per jendela, gantian pakai mouse
# ---------------------------------------------------------------------------

def run_multi(rest=None):
    from gbf_tani.windows import GAME_TITLE, find_game_windows

    windows = find_game_windows()
    if len(windows) != accounts:
        found = "".join(f"\n   {i}. {w.describe()}" for i, w in enumerate(windows, start=1))
        raise SystemExit(
            f'❌ config.json minta {accounts} akun, tapi ketemu {len(windows)} jendela "{GAME_TITLE}":'
            f"{found or chr(10) + '   (tidak ada)'}\n"
            f"   Buka {accounts} jendela browser, tab aktifnya harus tab game, jangan di-minimize."
        )

    for index, window in enumerate(windows, start=1):
        left, top, width, height = window.region()
        print(f"🪟 Akun {index}: jendela di x={left}, y={top} ({width}×{height})")

    session.start()
    _start_humanizer(rest)
    threads = [
        threading.Thread(target=_account_loop, args=(index, window, rest), name=f"akun-{index}", daemon=True)
        for index, window in enumerate(windows, start=1)
    ]
    for thread in threads:
        thread.start()

    def alive_count():
        return sum(t.is_alive() for t in threads)

    def must_stop():
        return session.STOP.is_set() or _timer_done()  # _timer_done() tidak bisa True selama istirahat

    while not session.STOP.is_set() and alive_count():
        if _timer_done():
            _print_limit()
            break
        if rest and not rest.supervise(alive_count, stop_check=must_stop):
            if _timer_done():
                _print_limit()
            break
        time.sleep(0.5)
    else:
        if not any(t.is_alive() for t in threads):
            print("⛔ Semua akun sudah berhenti.")
    # main selesai → thread akun (daemon) yang masih jalan ikut berhenti


def _account_loop(index, window, rest=None):
    context.set_account(index, window)
    try:
        while not session.STOP.is_set():
            if rest:
                rest.checkpoint(session.STOP)
            check_tab(mode)
    except SystemExit:
        log("⛔ Akun ini berhenti.")
    except Exception:
        log("❌ Error, semua akun dihentikan:\n" + traceback.format_exc())
        session.STOP.set()


if __name__ == "__main__":
    main()
