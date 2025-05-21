# LED Strip Control API — Curl Commands & Parameters

## 🖥️ Setup
- **SSH into the Raspberry Pi**
  ```bash
  ssh pi@10.205.3.54
  # password: raspberry
  ```

- **Run the API**
  ```bash
  cd led_truss/
  sudo /home/pi/led_truss/venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
  ```

---

## 🎛️ Direct Control Endpoints

### `POST /control/clear`
Turns off all LEDs.

```bash
curl -X POST http://10.205.3.54:8000/control/clear
```

---

### `POST /control/set-color`
Sets all LEDs to a color (defaults to white if not provided).

```bash
curl -X POST http://10.205.3.54:8000/control/set-color -H "Content-Type: application/json" -d '{"color":{"r":255,"g":255,"b":255}}'
```

- `r`, `g`, `b`: Integer values from 0 to 255

---

### `POST /control/set-brightness`
Sets global brightness level.

```bash
curl -X POST http://10.205.3.54:8000/control/set-brightness -H "Content-Type: application/json" -d '{"brightness":125}'
```

- `brightness`: 0 to 255

---

### `POST /control/set-color-range-percent`
Sets color between two percentage positions.

```bash
curl -X POST http://10.205.3.54:8000/control/set-color-range-percent -H "Content-Type: application/json" -d '{"color":{"r":255,"g":0,"b":0},"start_percent":0.2,"end_percent":0.5}'
```

- `start_percent`, `end_percent`: float values between 0.0 and 1.0

---

### `POST /control/set-color-range-exact`
Sets color between two LED indices.

```bash
curl -X POST http://10.205.3.54:8000/control/set-color-range-exact -H "Content-Type: application/json" -d '{"color":{"r":0,"g":0,"b":255},"start_index":10,"end_index":50}'
```

- `start_index`, `end_index`: integer indices (e.g. 0 to 1800)

---

## 🌈 Effects Endpoints

### `POST /effects/bitcoin`
Tracks Bitcoin price with color updates.

```bash
curl -X POST http://10.205.3.54:8000/effects/bitcoin -H "Content-Type: application/json" -d '{"duration":60,"time_threshold_in_secs":30}'
```

- `duration`: total seconds to monitor  
- `time_threshold_in_secs`: seconds per color change window

---

### `POST /effects/glow`
Pulsing glow effect.

```bash
curl -X POST http://10.205.3.54:8000/effects/glow -H "Content-Type: application/json" -d '{"color":{"r":0,"g":255,"b":0},"frames":300,"wait_ms":10}'
```

- `frames`: number of frames  
- `wait_ms`: delay in milliseconds between frames

---

### `POST /effects/wave`
Cosine wave animation.

```bash
curl -X POST http://10.205.3.54:8000/effects/wave -H "Content-Type: application/json" -d '{"color":{"r":255,"g":0,"b":0},"frames":300,"cycles":2,"speed":0.1,"wait_ms":10}'
```

- `cycles`: number of full waves  
- `speed`: float, e.g. 0.1  
- `wait_ms`: delay in ms per frame

---

### `POST /effects/color-wipe`
Wipes color across strip.

```bash
curl -X POST http://10.205.3.54:8000/effects/color-wipe -H "Content-Type: application/json" -d '{"color":{"r":255,"g":255,"b":0},"wait_ms":50}'
```

- `wait_ms`: delay per LED pixel

---

### `POST /effects/color-fade`
Fades from one color to another.

```bash
curl -X POST http://10.205.3.54:8000/effects/color-fade -H "Content-Type: application/json" -d '{"color_from":{"r":0,"g":0,"b":0},"color_to":{"r":255,"g":255,"b":255},"wait_ms":20,"steps":100}'
```

- `steps`: number of color steps  
- `wait_ms`: delay per step

---

### `POST /effects/sparkle`
Random sparkle pixels.

```bash
curl -X POST http://10.205.3.54:8000/effects/sparkle -H "Content-Type: application/json" -d '{"color":{"r":255,"g":255,"b":255},"wait_ms":50,"cummulative":false}'
```

- `color`: optional, RGB  
- `cummulative`: true or false

---

### `POST /effects/rainbow`
Rainbow gradient fade.

```bash
curl -X POST http://10.205.3.54:8000/effects/rainbow -H "Content-Type: application/json" -d '{"wait_ms":50,"iterations":1}'
```

- `iterations`: how many cycles to run

---

### `POST /effects/rainbow-cycle`
Evenly distributed rainbow cycle.

```bash
curl -X POST http://10.205.3.54:8000/effects/rainbow-cycle -H "Content-Type: application/json" -d '{"wait_ms":50,"iterations":5}'
```

---

### `POST /effects/theater-chase`
Chase effect with optional color.

```bash
curl -X POST http://10.205.3.54:8000/effects/theater-chase -H "Content-Type: application/json" -d '{"color":{"r":255,"g":0,"b":255},"wait_ms":50,"iterations":10}'
```

---

### `POST /effects/running`
Moving bar of light.

```bash
curl -X POST http://10.205.3.54:8000/effects/running -H "Content-Type: application/json" -d '{"wait_ms":10,"duration_ms":18000,"width":1}'
```

- `duration_ms`: total effect time  
- `width`: number of pixels in the bar