# gbf_tani/log.py
from gbf_tani import context


def log(message):
    """print() dengan label akun di depan ('[Akun 2] ...') kalau mode multi."""
    print(f"{context.account_label()}{message}")
