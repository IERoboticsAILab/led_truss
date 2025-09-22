## LED Truss Control API

### Abstract
This project provides an open, reproducible LED infrastructure for telepresence on an OptiTrack truss. WS2813 strips are mounted to the truss and driven from a Raspberry Pi via a FastAPI service exposing programmable effects and direct color control. The system integrates with Home Assistant and supports non‑invasive human monitoring (e.g., heart rate via Playwright) to map real‑time biosignals to ambient light displays that communicate mood and presence. The emphasis is infrastructure: clear APIs, modular effects, and end‑to‑end setup so anyone can re‑create the installation from scratch.

FastAPI service to control WS281x LED strips mounted on a truss. Provides REST endpoints for direct color control and several animated visual effects, including integrations for Home Assistant and a heart‑rate visualization.

### Features
- Direct control: clear, set color, set brightness, color by range
- Effects: bitcoin, glow, wave, color wipe, color fade, sparkle, rainbow, rainbow cycle, theater chase, running, heart‑rate
- Heart‑rate visualization using Playwright (Chromium headless)
- Home Assistant Lovelace controls and automations

---

### Hardware
- Raspberry Pi (with PWM-capable GPIO pins, e.g. GPIO18 and GPIO13)
- WS281x-compatible strips (WS2812B/WS2813)
- Proper 5V power supply sized for your LED count (do NOT power long strips from Pi 5V pin)
- Common ground between LED power supply and Raspberry Pi
- Recommended: logic-level shifter for data lines, power injection for long runs

Wiring basics:
- Connect LED GND to Pi GND
- Connect LED data-in to GPIO18 (strip 1) and GPIO13 (strip 2) by default
- Connect LED 5V to external 5V supply; share ground with Pi

Safety notes:
- Each LED can draw up to ~60 mA at full white. Size your power supply accordingly.
- Power inject for long strips to avoid voltage drop.
- Avoid powering full strips from the Pi 5V pin.

---

### Software prerequisites (on Raspberry Pi)
- Python 3.9+
- System packages: libatlas-base-dev (for numpy performance), chromium dependencies for Playwright
- Python packages: fastapi, uvicorn, rpi-ws281x, numpy, requests, pydantic, playwright

Optional but recommended: a Python virtual environment.

---

### Install
```bash
sudo apt update
sudo apt install -y python3-venv libatlas-base-dev

cd ~/
git clone https://github.com/<your-org-or-user>/led_truss.git
cd led_truss

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install fastapi uvicorn[standard] rpi-ws281x numpy requests playwright

# Playwright is required for the heart-rate effect
python -m playwright install chromium
```

If you plan to run without the heart‑rate effect, Playwright can be skipped.

---

### Configure LED layout
Edit `app/core/truss.py` constructor defaults to match your hardware:

```12:20:app/core/truss.py
    def __init__(self, strip1_count=896, strip2_count=894, strip1_pin=18, strip2_pin=13, freq=800000, dma=10, brightness=125):
        # 
        self.STRIP1_COUNT = strip1_count  # Number of LEDs in strip 1
        self.STRIP2_COUNT = strip2_count  # Number of LEDs in strip 2
```

- `strip1_pin` GPIO18 and `strip2_pin` GPIO13 are defaults. Adjust if wired differently.
- `brightness` is global 0–255.

---

### Run the API
```bash
cd ~/led_truss
sudo ./venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Notes:
- `sudo` is often required by `rpi_ws281x` to access PWM.
- Open API docs will be at `http://<pi-ip>:8000/docs` and JSON at `http://<pi-ip>:8000/openapi.json`.

Optional: systemd service
```ini
[Unit]
Description=LED Truss API
After=network-online.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/led_truss
ExecStart=/home/pi/led_truss/venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
Save as `/etc/systemd/system/led-truss.service`, then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now led-truss
```

---

### Quick start (curl)
```bash
# Set all LEDs to white
curl -X POST http://<pi-ip>:8000/control/set-color

# Rainbow cycle (runs continuously until stopped)
curl -X POST http://<pi-ip>:8000/effects/rainbow-cycle -H "Content-Type: application/json" -d '{"wait_ms":50}'

# Clear
curl -X POST http://<pi-ip>:8000/control/clear
```

See the API quick reference below.

---

### API overview
- Root: `GET /` → welcome message
- Effects map: `GET /effects` → returns metadata from `effects_map.json`
- Direct control endpoints are under `/control/*`
- Effects endpoints are under `/effects/*`

See the API quick reference below.

---

### Home Assistant integration
This repository includes example YAML under `home_assistant_config/`:
- `rest_commands.yaml` builds the correct endpoint URL and payloads
- `input_numbers.yaml`, `input_booleans.yaml`, `input_selects.yaml`, `input_texts.yaml` provide UI helpers
- `lights.yaml` defines a color picker helper light
- `automations.yaml` keeps the helper light and RGB inputs in sync
- `lovelace_led_control.yaml` is a dashboard layout for controls

Steps:
1. Copy the YAML contents into your Home Assistant configuration (adjust IPs).
2. Ensure the REST command URL points to your Pi IP.
3. Reload YAML / restart, then add the Lovelace dashboard JSON as a view.

Note: The heart‑rate effect requires an accessible URL that renders an element with the `.heartrate` class (e.g. Hyperate). See params in `effects_map.json` and docs.

---

### Troubleshooting
- No LEDs change: verify 5V power, common ground, and data direction (DIN vs DOUT).
- Colors flicker or wrong: add a logic-level shifter and series resistor (~300–500 Ω) on data line; ensure correct ground.
- `PermissionError` or no output: run with `sudo`.
- Heart‑rate effect fails: install Playwright Chromium and ensure the URL is reachable from the Pi.
- CORS for browser clients: CORS is allowed for all origins by default; lock down in `app/main.py` for production.

---

### Security
- Default CORS is permissive; restrict `allow_origins` for production.
- If exposed beyond LAN, put the API behind a reverse proxy with auth.
- Change default passwords on your Pi; use a firewall or VLAN when possible.

---

### Project layout
```text
app/
  core/           # Hardware controller and DI
  effects/        # Effects metadata loader
  models/         # Pydantic request schemas
  routers/        # FastAPI routers (/control, /effects)
home_assistant_config/  # Example HA integration YAML
effects_map.json  # Descriptions and defaults for effects
```

---

### API quick reference

All effects run continuously until a new effect starts or you clear the LEDs. To stop and clear: `POST /control/clear`.

- Base URL: `http://<pi-ip>:8000`
- OpenAPI docs: `http://<pi-ip>:8000/docs`
- Effects metadata (names, params, defaults): `GET /effects`
 
Control endpoints:
- `POST /control/clear` — no body
- `POST /control/set-color` — `{ "color": {"r": 255, "g": 255, "b": 255 } }` (optional color)
- `POST /control/set-brightness` — `{ "brightness": 125 }`
- `POST /control/set-color-range-percent` — `{ "color": {..}, "start_percent": 0.0, "end_percent": 1.0 }`
- `POST /control/set-color-range-exact` — `{ "color": {..}, "start_index": 0, "end_index": 1800 }`

Effects endpoints (see `GET /effects` for full parameter schemas):
- `POST /effects/bitcoin` — `{ "time_threshold_in_secs": 30 }`
- `POST /effects/glow` — `{ "color": {..}, "wait_ms": 10 }`
- `POST /effects/wave` — `{ "color": {..}, "cycles": 1, "speed": 0.1, "wait_ms": 10 }`
- `POST /effects/color-wipe` — `{ "color": {..}, "wait_ms": 50 }`
- `POST /effects/color-fade` — `{ "color_from": {..}, "color_to": {..}, "wait_ms": 20, "steps": 100 }`
- `POST /effects/sparkle` — `{ "color": {..} | null, "wait_ms": 50, "cummulative": false }`
- `POST /effects/rainbow` — `{ "wait_ms": 50 }`
- `POST /effects/rainbow-cycle` — `{ "wait_ms": 50 }`
- `POST /effects/theater-chase` — `{ "color": {..} | null, "wait_ms": 50 }`
- `POST /effects/running` — `{ "wait_ms": 10, "width": 1 }`
- `POST /effects/heart-rate` — `{ "url": "https://...", "poll_interval": 1.0, "min_hr": 40, "yellow_start": 75, "red_start": 120, "max_hr": 200, "pulse": true }`

Notes:
- Start a new effect to stop the previous one automatically.
- Use `/control/clear` to stop and turn off all LEDs.

### License
MIT (or your preferred license). Update as appropriate.
