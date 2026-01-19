# Simple Setup Guide

## Quick Start

### 1. Set Your Backend IP

Edit `frontend/.env` and set your backend IP address:

```bash
VITE_API_URL=http://YOUR_BACKEND_IP:8000
```

**Example:**
```bash
VITE_API_URL=http://192.168.1.99:8000
```

### 2. Start the Backend

```bash
python api.py
```

The API will run on `http://0.0.0.0:8000` (accessible from network).

### 3. Start the Frontend

```bash
cd frontend
npm run dev
```

The frontend will run on `http://localhost:5173`.

### 4. Access the App

- **Same machine**: `http://localhost:5173`
- **From network**: `http://YOUR_DEVICE_IP:5173`

## That's It!

The backend automatically accepts connections from any origin, so you just need to:
1. Set the backend IP in `frontend/.env`
2. Start both servers
3. Access from browser

## Finding Your IP Address

**Mac/Linux:**
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

**Raspberry Pi:**
```bash
hostname -I
```

**Windows:**
```bash
ipconfig
```

## Example Setup

If your Raspberry Pi is at `192.168.1.99`:

**File: `frontend/.env`**
```bash
VITE_API_URL=http://192.168.1.99:8000
```

Then access the frontend from any device at:
- `http://192.168.1.99:5173` (from network)
- `http://localhost:5173` (from the Pi itself)

Done!
