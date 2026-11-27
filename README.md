# Screen-State Automation Framework

A Python framework for automating repetitive UI sequences in applications that expose no API.
It determines the current screen state by matching reference images against live screen captures
with OpenCV, then dispatches the corresponding input actions through PyAutoGUI.

Originally built to automate repetitive sequences in a browser game, but the state-detection
engine is deliberately game-agnostic — the behaviour is defined entirely by configuration and
reference images, not by code.

---

## How it works

The core loop is a simple state machine driven by computer vision rather than by an API:

1. **Capture** — a screenshot of the target region is taken.
2. **Match** — OpenCV `matchTemplate` compares that capture against a set of reference images
   in `assets/`, each representing a known UI state.
3. **Resolve** — the highest-confidence match above the configured threshold becomes the
   current state. If nothing clears the threshold, the loop waits rather than guessing.
4. **Act** — the action mapped to that state in `config.json` is dispatched via PyAutoGUI.
5. **Repeat** — with a randomised delay, so timing is not perfectly uniform.

Because state is derived from what is actually on screen rather than from an assumed sequence,
the loop recovers from unexpected screens instead of blindly continuing.

---

## Design notes

**Configuration over code.** Reference images, thresholds, coordinates and action sequences all
live in `config.json` and `data.json`. Adapting the tool to a different application means
replacing images and editing configuration — the engine itself is untouched.

**Separated concerns.** State detection, action dispatch and configuration loading are separate
modules, so the matching strategy can be changed without rewriting the action layer.

**Fail-safe by default.** Two safeguards are built in:

- **Auto-termination** — the process exits automatically after a configured duration, so an
  unattended run cannot continue indefinitely.
- **PyAutoGUI failsafe** — moving the cursor to a screen corner aborts execution immediately.

---

## Requirements

- Python **3.12.10**
- pip (bundled with the Python installer)

## Installation

```bash
git clone https://github.com/Falllll/gbf-tani.git
cd gbf-tani
pip install -r requirements.txt
```

Then create your own `config.json` from the example:

```bash
cp config.example.json config.json
```

## Configuration

| File | Purpose |
|------|---------|
| `config.json` | Which raid to run and how (see below) |
| `data.json` | State definitions and their associated reference images |
| `assets/` | Reference images used for template matching |

### `config.json`

```json
{
    "raid_id": 163,
    "finder": false,
    "full_auto": true,
    "timer": true,
    "timer_seconds": "1 * 60 * 60"
}
```

| Key | Value | Meaning |
|-----|-------|---------|
| `raid_id` | number | Raid `id` from `data.json` |
| `finder` | `true` / `false` | `true` = join raids from the Finder tab, `false` = solo |
| `full_auto` | `true` / `false` | `true` = full auto, `false` = run the steps in `manual.json` (start from `example.json`) |
| `timer` | `true` / `false` | `true` = stop automatically after `timer_seconds`, `false` = run until stopped manually |
| `timer_seconds` | number or `"a * b * c"` | Run time in seconds when `timer` is `true`, e.g. `3600` or `"1 * 60 * 60"` (1 hour) |

`finder`, `full_auto` and `timer` must be written without quotes. JSON cannot hold a formula,
so a calculated `timer_seconds` must be quoted (`"1 * 60 * 60"`); only numbers and `*` are
accepted. If any key is missing or invalid, the bot stops at startup and says which key is wrong.

Reference images must be captured at the same resolution and scaling as the target application.
Template matching is not scale-invariant, so a mismatched display scale is the most common
cause of failed detection.

## Usage

```bash
python main.py
```

The process reports the detected state each cycle and terminates automatically once the
configured duration elapses.

## Project structure

```
gbf-tani/
├── main.py                  # entry point (main loop + optional timer)
├── config.json              # raid_id, finder, full_auto, timer (copy from config.example.json)
├── data.json                # raid list + reference image per raid
├── manual.json              # step list for manual mode
├── assets/                  # reference images (buttons, pages, party, raids)
└── gbf_tani/
    ├── config.py            # loads config.json + data.json
    ├── assets.py            # every reference-image path in one place
    ├── vision/              # low level, knows nothing about the game
    │   ├── capture.py       # screenshot
    │   ├── matcher.py       # template matching
    │   └── mouse.py         # clicking
    ├── game/                # game-specific actions
    │   ├── buttons.py       # reload, bookmark, auto, OK, quick summon, wait for auto
    │   ├── popups.py        # raid popups, pending battle, captcha, result, summon select
    │   └── party.py         # skills & summons (pixel offsets)
    └── flows/               # bot flows
        ├── navigator.py     # check_tab: routing per mode
        ├── finder.py        # find & join a raid
        ├── battle.py        # handle_battle + full auto
        ├── manual.py        # manual mode driven by manual.json
        └── pending_battle.py
```

---

## Limitations

- Template matching is sensitive to resolution, DPI scaling and colour profile changes.
- The tool controls the real cursor and keyboard, so it requires an active, unobstructed display.
- No OCR — states must be distinguishable by image, not by text content.

## Disclaimer

This project was written as a personal exercise in computer vision and automation design.
Automating third-party software may conflict with that software's terms of service. Anyone
using or adapting this code is responsible for ensuring their use complies with the terms of
the application they are automating. It is provided for educational purposes, without warranty.

## License

MIT
