# GBF-TANI

Bot farming Granblue Fantasy (experimental).

## Requirements
- Python **3.12.10** → [Download di sini](https://www.python.org/downloads/release/python-31210/)
- pip (sudah termasuk di installer Python)

## Install
```bash
pip install -r requirements.txt
```

## Jalankan
Dari root project (folder yang berisi `main.py`):
```bash
python main.py
```

## Struktur
```
gbf-tani/
├── main.py                  # entry point (loop utama + batas runtime)
├── config.json              # raid_id, mode (finder/solo/event), setup (fa/manual)
├── data.json                # daftar raid + template-nya
├── manual.json              # langkah mode manual
├── assets/                  # template gambar (button, page, party, raids)
└── gbf_tani/
    ├── config.py            # baca config.json + data.json
    ├── assets.py            # semua path template di satu tempat
    ├── vision/              # lapisan bawah, tidak tahu apa-apa soal game
    │   ├── capture.py       # screenshot
    │   ├── matcher.py       # template matching
    │   └── mouse.py         # klik
    ├── game/                # aksi spesifik GBF
    │   ├── buttons.py       # reload, bookmark, auto, OK, quick summon, tunggu auto
    │   ├── popups.py        # popup raid, pending battle, captcha, result, select summon
    │   └── party.py         # skill & summon (offset pixel)
    └── flows/               # alur bot
        ├── navigator.py     # check_tab: routing per mode
        ├── finder.py        # cari & join raid
        ├── battle.py        # handle_battle + full auto
        ├── manual.py        # mode manual dari manual.json
        └── pending_battle.py
```
