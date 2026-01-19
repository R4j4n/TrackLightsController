# Configuration Guide

This project uses environment variables for easy configuration. All settings are centralized in `.env` files.

## Quick Setup

### 1. Configure Your Device IP

Edit the `.env` file in the root directory:

```bash
# Change this to your device's actual IP address
DEVICE_IP=192.168.1.244
```

### 2. Update Frontend Configuration

The frontend will automatically use the API URL. You can customize it in `frontend/.env`:

```bash
VITE_API_URL=http://192.168.1.244:8000
```

**Important**: The IP address in `frontend/.env` should match the `DEVICE_IP` in the root `.env` file.

## Configuration Files

### Root `.env` (Backend Configuration)

Located at: `/.env`

```bash
# Device IP Address (change this to your device's IP)
DEVICE_IP=192.168.1.244

# API Server Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Frontend Dev Server Configuration
FRONTEND_PORT=5173

# Environment (development or production)
ENVIRONMENT=development
```

### Frontend `.env`

Located at: `/frontend/.env`

```bash
# API URL - Update the IP to match your device
VITE_API_URL=http://192.168.1.244:8000
```

## How It Works

### CORS Configuration

The API automatically configures CORS (Cross-Origin Resource Sharing) based on your environment variables:

- **Localhost Access**: `http://localhost:5173`
- **Loopback Access**: `http://127.0.0.1:5173`
- **Network Access**: `http://{DEVICE_IP}:5173`
- **Development Mode**: Also allows `*` (all origins)

This means you can access the frontend from:
- The same machine (localhost)
- Other devices on your network (using the device IP)

### Dynamic IP Setup

When you change the `DEVICE_IP` in `.env`:

1. The API automatically allows CORS from `http://{DEVICE_IP}:5173`
2. The frontend uses the `VITE_API_URL` to connect to the API
3. Everything works seamlessly without code changes

## Common Scenarios

### Running on the Same Machine

Use `localhost` in the frontend `.env`:

```bash
VITE_API_URL=http://localhost:8000
```

### Accessing from Another Device

Use your device's IP address in both files:

Root `.env`:
```bash
DEVICE_IP=192.168.1.244
```

Frontend `.env`:
```bash
VITE_API_URL=http://192.168.1.244:8000
```

### Finding Your Device IP

**On Mac/Linux:**
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

**On Raspberry Pi:**
```bash
hostname -I
```

**On Windows:**
```bash
ipconfig
```

## Installation

After changing configuration, install the new dependency:

```bash
pip install -r requirements.txt
```

This will install `python-dotenv` which is required for loading environment variables.

## Starting the Servers

### Backend (API)

```bash
python api.py
```

The API will start on the configured `API_HOST:API_PORT` (default: `0.0.0.0:8000`)

### Frontend

```bash
cd frontend
npm run dev
```

The frontend will start on the configured `FRONTEND_PORT` (default: `5173`)

## Production Deployment

For production, change the environment:

```bash
ENVIRONMENT=production
```

This will:
- Disable the `*` wildcard in CORS
- Only allow specific origins
- Improve security

## Troubleshooting

### CORS Errors

If you see CORS errors in the browser console:

1. Check that `DEVICE_IP` in `.env` matches your actual device IP
2. Verify `VITE_API_URL` in `frontend/.env` uses the correct IP
3. Restart both the API and frontend servers
4. Clear browser cache (hard refresh: Ctrl+Shift+R / Cmd+Shift+R)

### Connection Refused

If the frontend can't connect to the API:

1. Verify the API is running (`python api.py`)
2. Check the API is accessible at the configured IP and port
3. Ensure firewall isn't blocking the connection
4. Try using `localhost` if on the same machine

### Environment Variables Not Loading

1. Make sure `.env` files exist in the correct locations
2. Install python-dotenv: `pip install python-dotenv`
3. Restart the servers after changing `.env` files

## Summary

**To change your device IP:**

1. Update `DEVICE_IP` in `/.env`
2. Update `VITE_API_URL` in `/frontend/.env`
3. Restart both servers
4. Refresh your browser

That's it! The CORS and API configuration will automatically adjust.
