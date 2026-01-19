# Track Lights Controller - Complete Setup Guide

Complete guide for setting up and running both the backend API and frontend UI.

## Project Overview

A full-stack application for controlling track lights via Raspberry Pi GPIO:

- **Backend**: FastAPI + Python controlling GPIO switches
- **Frontend**: React + TypeScript modern UI
- **Features**: Color control, mode switching, real-time status, state persistence

## Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌──────────────┐
│  React Frontend │ HTTP    │   FastAPI API    │  GPIO   │  Light       │
│  (Port 5173)    │────────▶│   (Port 8000)    │────────▶│  Controller  │
└─────────────────┘         └──────────────────┘         └──────────────┘
                                     │
                                     ▼
                              ┌──────────────┐
                              │  state.json  │
                              │  (Persist)   │
                              └──────────────┘
```

## Prerequisites

### For Backend
- Raspberry Pi (any model with GPIO)
- Python 3.8+
- GPIO access permissions

### For Frontend
- Node.js 18+
- npm or yarn

## Quick Start

### 1. Backend Setup

```bash
# Navigate to project root
cd /home/tracklights/lightscontroller

# Install Python dependencies
pip install -r requirements.txt

# Start the API server
python api.py
```

The API will be available at `http://localhost:8000`

View API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd /home/tracklights/lightscontroller/frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Detailed Setup

### Backend Configuration

#### GPIO Permissions

If you get permission errors:

```bash
sudo usermod -a -G gpio $USER
sudo chmod g+rw /dev/gpiomem
# Log out and back in for changes to take effect
```

#### Run as System Service

Create `/etc/systemd/system/lightscontroller.service`:

```ini
[Unit]
Description=Track Lights Controller API
After=network.target

[Service]
Type=simple
User=tracklights
WorkingDirectory=/home/tracklights/lightscontroller
ExecStart=/usr/bin/python3 /home/tracklights/lightscontroller/api.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable lightscontroller.service
sudo systemctl start lightscontroller.service
sudo systemctl status lightscontroller.service
```

### Frontend Configuration

#### Environment Variables

Create `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

For production (Raspberry Pi IP):

```env
VITE_API_URL=http://192.168.1.XXX:8000
```

#### Production Build

```bash
cd frontend
npm run build

# Serve the build
npm run preview
# OR use a static server like nginx
```

#### Deploy with Nginx

1. Build the frontend:
```bash
cd frontend
npm run build
```

2. Configure nginx:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /home/tracklights/lightscontroller/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # API proxy
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Usage

### 1. Start the Backend

```bash
cd /home/tracklights/lightscontroller
python api.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 2. Start the Frontend

In a new terminal:

```bash
cd /home/tracklights/lightscontroller/frontend
npm run dev
```

You should see:
```
  VITE v7.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### 3. Access the UI

Open your browser to `http://localhost:5173`

You should see:
- ✅ Connected status indicator
- 🎨 Three color buttons (Red, Green, Yellow)
- 🌈 Six mode selection cards
- 📊 Real-time status display
- 🔄 Reset system button

## Testing

### Test Backend API

```bash
# Health check
curl http://localhost:8000/health

# Get status
curl http://localhost:8000/status

# Set color
curl -X POST http://localhost:8000/color \
  -H "Content-Type: application/json" \
  -d '{"color": "red"}'

# Set mode
curl -X POST http://localhost:8000/mode \
  -H "Content-Type: application/json" \
  -d '{"mode": "breathe_colors"}'

# Reset
curl -X POST http://localhost:8000/reset
```

### Test Frontend

1. Click on a color button - should light up with animation
2. Click on a mode card - should become active
3. Check status display updates
4. Try the reset button

## Features

### Backend Features

- ✅ GPIO control for 4 switches (SW1-SW4)
- ✅ Smart mode switching (calculates required SW4 presses)
- ✅ State persistence across restarts
- ✅ Simulation mode for non-Pi systems
- ✅ RESTful API with auto-generated docs
- ✅ CORS enabled for frontend access
- ✅ Comprehensive error handling and logging

### Frontend Features

- ✅ Modern, responsive UI with animations
- ✅ Real-time status polling (every 3 seconds)
- ✅ Color selection with visual feedback
- ✅ 6 different light modes
- ✅ Connection status indicator
- ✅ Error handling with user-friendly messages
- ✅ Mobile-friendly design
- ✅ TypeScript for type safety

## Project Structure

```
lightscontroller/
├── api.py                      # FastAPI application
├── gpio_controller.py          # GPIO control logic
├── state_manager.py            # State persistence
├── state.json                 # State file (auto-generated)
├── requirements.txt            # Python dependencies
├── README.md                   # Backend documentation
├── SETUP_GUIDE.md             # This file
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── ColorButton.tsx/css
    │   │   ├── ModeSelector.tsx/css
    │   │   └── StatusDisplay.tsx/css
    │   ├── api.ts              # API client
    │   ├── types.ts            # TypeScript types
    │   ├── App.tsx/css         # Main component
    │   └── main.tsx/index.css
    ├── public/
    ├── .env.example
    ├── vite.config.ts
    ├── package.json
    └── README.md               # Frontend documentation
```

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`
```bash
pip install -r requirements.txt
```

**Problem**: `Permission denied: '/dev/gpiomem'`
```bash
sudo usermod -a -G gpio $USER
# Log out and back in
```

**Problem**: Port 8000 already in use
```bash
sudo lsof -t -i:8000 | xargs kill -9
# Or change port in api.py
```

### Frontend Issues

**Problem**: Can't connect to API
- Ensure backend is running on port 8000
- Check `.env` file has correct `VITE_API_URL`
- Look for CORS errors in browser console

**Problem**: `npm install` fails
```bash
rm -rf node_modules package-lock.json
npm install
```

**Problem**: TypeScript errors
```bash
npm run build
# Check output for specific errors
```

### General Issues

**Problem**: State not persisting
- Check `state.json` file exists and is writable
- Look for errors in backend logs

**Problem**: Frontend shows "Disconnected"
- Ensure backend is running
- Check network connectivity
- Verify CORS is configured correctly

## Development Tips

### Backend Development

- Check logs: `tail -f /var/log/syslog` (if running as service)
- Use reload mode: `uvicorn api:app --reload`
- Test with curl or Postman

### Frontend Development

- Hot reload is automatic with Vite
- Use browser DevTools for debugging
- Check Network tab for API calls
- Use React DevTools extension

## Production Deployment

### Checklist

- [ ] Set secure CORS origins in `api.py`
- [ ] Use environment variables for sensitive config
- [ ] Set up systemd service for backend
- [ ] Build frontend for production
- [ ] Configure nginx/apache as reverse proxy
- [ ] Set up SSL/TLS certificates
- [ ] Configure firewall rules
- [ ] Set up monitoring and logging
- [ ] Create backup strategy for `state.json`

### Security Considerations

1. **CORS**: Restrict to specific domains in production
2. **Authentication**: Add auth middleware if exposing to internet
3. **HTTPS**: Use SSL certificates for production
4. **Firewall**: Only expose necessary ports
5. **Updates**: Keep dependencies up to date

## API Endpoints Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/status` | Get current status |
| POST | `/color` | Set light color |
| POST | `/mode` | Set light mode |
| POST | `/mode/press` | Press mode button N times |
| POST | `/reset` | Reset system |
| GET | `/modes` | List available modes |
| GET | `/colors` | List available colors |
| GET | `/health` | Health check |
| GET | `/docs` | Swagger UI |
| GET | `/redoc` | ReDoc |

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation at `/docs`
3. Check browser console for errors
4. Review backend logs

## License

MIT License
