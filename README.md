# Track Lights Controller API

FastAPI backend for controlling track lights via GPIO-connected switches on Raspberry Pi.

## Hardware Setup

### GPIO Pin Configuration

| Switch | Function | GPIO Pin | Physical Pin |
|--------|----------|----------|--------------|
| SW1 | Red Light | GPIO 17 | Pin 11 |
| SW2 | Green Light | GPIO 18 | Pin 12 |
| SW3 | Yellow Light | GPIO 27 | Pin 13 |
| SW4 | Mode Control | GPIO 22 | Pin 15 |
| GND | Ground | GND | Pin 6/9/14/20/25/30/34/39 |

### Wiring

Connect each switch between the respective GPIO pin and GND. The software will pull pins HIGH (idle) and LOW (pressed) to simulate button presses.

## Software Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the API Server

```bash
python api.py
```

The API will start on `http://0.0.0.0:8000`

### 3. Run as a Service (Optional)

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/lightscontroller.service
```

Add the following content:

```ini
[Unit]
Description=Track Lights Controller API
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/tracklights/lightscontroller
ExecStart=/usr/bin/python3 /home/tracklights/lightscontroller/api.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable lightscontroller.service
sudo systemctl start lightscontroller.service
```

## API Endpoints

### GET `/`
Get API information and available endpoints.

### GET `/status`
Get current controller status including active mode and last color pressed.

**Response:**
```json
{
  "gpio_available": true,
  "current_mode_press_count": 3,
  "current_mode": "track_direction",
  "last_color_pressed": "red",
  "available_modes": [...],
  "available_colors": [...]
}
```

### POST `/color`
Press a color switch (SW1, SW2, or SW3).

**Request:**
```json
{
  "color": "red"
}
```

**Valid colors:** `red`, `green`, `yellow`

**Response:**
```json
{
  "action": "color_switch_pressed",
  "color": "red",
  "gpio_pin": 17,
  "timestamp": 1234567890.123
}
```

### POST `/mode`
Set the light mode by automatically pressing SW4 the required number of times.

**Request:**
```json
{
  "mode": "breathe_colors"
}
```

**Valid modes:**
- `breathe_colors` - 1 press: Breathe Colors
- `color_duration` - 2 presses: Display each color for set duration
- `track_direction` - 3 presses: Run lights along track direction
- `circular_pattern` - 4 presses: Run lights in circular pattern
- `white_mode` - 5 presses: Set lights to White Mode
- `off` - 6 presses: Turn off the lights

**Response:**
```json
{
  "action": "mode_switch_pressed",
  "press_count": 2,
  "total_mode_presses": 3,
  "current_mode": "track_direction",
  "gpio_pin": 22,
  "timestamp": 1234567890.123
}
```

### POST `/mode/press`
Manually press SW4 a specific number of times.

**Request:**
```json
{
  "count": 2
}
```

**Response:**
```json
{
  "action": "mode_switch_pressed",
  "press_count": 2,
  "total_mode_presses": 2,
  "current_mode": "color_duration",
  "gpio_pin": 22,
  "timestamp": 1234567890.123
}
```

### POST `/reset`
Reset the system by turning off lights and clearing all state.

This endpoint will:
1. Turn off the lights (set to OFF mode via SW4)
2. Reset the internal state counter to 0
3. Clear the last color pressed

Perfect for starting fresh from the beginning.

**Response:**
```json
{
  "action": "system_reset",
  "lights_off": true,
  "state_cleared": true,
  "current_mode_press_count": 0,
  "timestamp": 1234567890.123,
  "message": "System reset successfully. Lights are off and ready to start from beginning."
}
```

### GET `/modes`
List all available modes and their press counts.

### GET `/colors`
List all available colors and their GPIO mappings.

### GET `/health`
Health check endpoint.

## Usage Examples

### Using curl

#### Set Red Light
```bash
curl -X POST http://localhost:8000/color \
  -H "Content-Type: application/json" \
  -d '{"color": "red"}'
```

#### Set to Breathe Colors Mode
```bash
curl -X POST http://localhost:8000/mode \
  -H "Content-Type: application/json" \
  -d '{"mode": "breathe_colors"}'
```

#### Press Mode Button Twice
```bash
curl -X POST http://localhost:8000/mode/press \
  -H "Content-Type: application/json" \
  -d '{"count": 2}'
```

#### Get Current Status
```bash
curl http://localhost:8000/status
```

#### Reset System
```bash
curl -X POST http://localhost:8000/reset
```

### Using Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Set green light
response = requests.post(f"{BASE_URL}/color", json={"color": "green"})
print(response.json())

# Set to circular pattern mode
response = requests.post(f"{BASE_URL}/mode", json={"mode": "circular_pattern"})
print(response.json())

# Reset system (turn off lights and clear state)
response = requests.post(f"{BASE_URL}/reset")
print(response.json())

# Get status
response = requests.get(f"{BASE_URL}/status")
print(response.json())
```

### Using JavaScript/Fetch

```javascript
const BASE_URL = 'http://localhost:8000';

// Set yellow light
fetch(`${BASE_URL}/color`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ color: 'yellow' })
})
  .then(res => res.json())
  .then(data => console.log(data));

// Turn off lights
fetch(`${BASE_URL}/mode`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ mode: 'off' })
})
  .then(res => res.json())
  .then(data => console.log(data));

// Reset system
fetch(`${BASE_URL}/reset`, {
  method: 'POST'
})
  .then(res => res.json())
  .then(data => console.log(data));
```

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## How It Works

### Mode State Management

The API remembers the current state of SW4 (which mode is active based on press count). When you request a specific mode:

1. The API calculates how many presses are needed to reach the target mode
2. It simulates the required number of button presses
3. The system cycles through modes 1→2→3→4→5→6→1...

**Example:** If currently in mode 5 (White Mode) and you want mode 2 (Color Duration):
- System will press SW4 three times: 5→6→1→2

### Persistent State Storage

The API automatically saves its state to disk after every mode or color change. This means:

- **Survives restarts:** If the API crashes or is restarted, it remembers the last mode and color
- **State file location:** `/home/tracklights/lightscontroller/state.json`
- **Automatic sync:** No manual intervention needed - state is saved automatically
- **Atomic writes:** Uses temporary file + rename to prevent corruption

**State file example:**
```json
{
  "current_mode_press_count": 3,
  "last_color_pressed": "red",
  "last_updated": "2026-01-19T15:30:45.123456"
}
```

**On startup:**
1. API reads `state.json` if it exists
2. Restores the last known mode and color
3. If file doesn't exist or is corrupted, starts with defaults (mode 0, no color)

**On reset:**
- The `/reset` endpoint clears the state file completely
- System returns to fresh state (mode 0, no color)

### GPIO Control

The system controls GPIO pins as outputs to simulate button presses:
- **Idle state:** GPIO HIGH
- **Pressed state:** GPIO LOW for ~200ms
- **Released state:** Back to GPIO HIGH

This mimics a physical button press that the light controller can detect.

## Troubleshooting

### GPIO Permission Issues

If you get permission errors accessing GPIO:

```bash
sudo usermod -a -G gpio $USER
sudo chmod g+rw /dev/gpiomem
```

Then log out and back in.

### Module Import Errors

If RPi.GPIO fails to import, the system will run in simulation mode (useful for testing on non-Pi systems).

### Port Already in Use

If port 8000 is already in use:

```bash
# Find and kill the process
sudo lsof -t -i:8000 | xargs kill -9

# Or change the port in api.py
```

## Development

### Project Structure

```
lightscontroller/
├── api.py                 # FastAPI application
├── gpio_controller.py     # GPIO control logic
├── state_manager.py       # Persistent state storage
├── state.json            # State file (auto-generated)
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

### Testing Without Hardware

The system will automatically run in simulation mode if `RPi.GPIO` is not available. All API calls will work normally, logging simulated button presses instead of actual GPIO control.

## License

MIT License
