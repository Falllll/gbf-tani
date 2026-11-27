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

## Configuration

| File | Purpose |
|------|---------|
| `config.json` | Runtime settings — match threshold, delays, run duration, action mappings |
| `data.json` | State definitions and their associated reference images |
| `assets/` | Reference images used for template matching |

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
├── main.py                  # entry point (main loop + runtime limit)
├── config.json              # raid_id, mode (finder/solo/event), setup (fa/manual)
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
