# LED Strip Control API Documentation

## System Setup

To activate the LED control system:

1. Power on all LED strip power supplies (ensure correct voltage) and the Raspberry Pi.
2. Start the API (replace the path as needed):
   ```bash
   cd ~/led_truss
   sudo /home/pi/led_truss/venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

OpenAPI docs: `http://<pi-ip>:8000/docs`

---

## General Endpoints

- `GET /` — health/welcome message
- `GET /effects` — returns `effects_map.json` metadata (descriptions, params, defaults)

---

## 🎛️ Direct Control Endpoints

**Base URL:** `/control`

### `POST /clear`

Turns off all LEDs.

**Request Body:** None  
**Response:**
```json
{ "status": "success" }
```

---

### `POST /set-color`

Sets all LEDs to a color or white if not provided.

**Request Body:**
```json
{
  "color": { "r": 255, "g": 255, "b": 255 } // optional
}
```

---

### `POST /set-brightness`

Sets overall brightness (0–255).

**Request Body:**
```json
{
  "brightness": 125
}
```

---

### `POST /set-color-range-percent`

Colors a percentage range of the strip.

**Request Body:**
```json
{
  "color": { "r": 255, "g": 255, "b": 255 },
  "start_percent": 0.0,
  "end_percent": 1.0
}
```

---

### `POST /set-color-range-exact`

Colors an exact index range.

**Request Body:**
```json
{
  "color": { "r": 255, "g": 255, "b": 255 },
  "start_index": 0,
  "end_index": 1800
}
```

---

## 🌈 Visual Effects Endpoints

**Base URL:** `/effects`

### `POST /bitcoin`

Monitors BTC price and shows changes.

**Request Body:**
```json
{
  "duration": 60,
  "time_threshold_in_secs": 30
}
```

---

### `POST /glow`

Pulsing glow with custom color.

**Request Body:**
```json
{
  "color": { "r": 255, "g": 255, "b": 255 },
  "frames": 300,
  "wait_ms": 10
}
```

---

### `POST /wave`

Animated wave using cosine curves.

**Request Body:**
```json
{
  "color": { "r": 255, "g": 255, "b": 255 },
  "frames": 300,
  "cycles": 2,
  "speed": 0.1,
  "wait_ms": 10
}
```

---

### `POST /color-wipe`

Sequential pixel color wipe.

**Request Body:**
```json
{
  "color": { "r": 255, "g": 0, "b": 0 },
  "wait_ms": 50
}
```

---

### `POST /color-fade`

Fades from one color to another.

**Request Body:**
```json
{
  "color_from": { "r": 0, "g": 0, "b": 0 },
  "color_to": { "r": 255, "g": 255, "b": 255 },
  "wait_ms": 20,
  "steps": 100
}
```

---

### `POST /sparkle`

Random pixel sparkle effect.

**Request Body:**
```json
{
  "color": { "r": 255, "g": 255, "b": 0 }, // optional
  "wait_ms": 50,
  "cummulative": false
}
```

---

### `POST /rainbow`

Rainbow fade over full strip.

**Request Body:**
```json
{
  "wait_ms": 50,
  "iterations": 1
}
```

---

### `POST /rainbow-cycle`

Uniformly distributed rainbow cycling.

**Request Body:**
```json
{
  "wait_ms": 50,
  "iterations": 5
}
```

---

### `POST /theater-chase`

Moving theater-style dots.

**Request Body:**
```json
{
  "color": { "r": 255, "g": 0, "b": 255 }, // optional
  "wait_ms": 50,
  "iterations": 10
}
```

---

### `POST /running`

Moves a bright segment across the strip.

**Request Body:**
```json
{
  "wait_ms": 10,
  "duration_ms": 18000,
  "width": 1
}
```

---

### `POST /heart-rate`

Monitors a heart-rate widget URL and displays color-coded status (green → yellow → red) with a pulsing glow at the BPM frequency.

Dependencies: Playwright Chromium must be installed on the host.

**Request Body:**
```json
{
  "url": "https://app.hyperate.io/74524/",
  "duration": 300,
  "poll_interval": 1.0,
  "min_hr": 40,
  "yellow_start": 75,
  "red_start": 120,
  "max_hr": 200
}
```

Notes:
- The page must contain an element with class `.heartrate` that contains the numeric BPM.
- `poll_interval` is in hertz (times per second).
