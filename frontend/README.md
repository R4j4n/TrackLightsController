# Track Lights Controller - Frontend

Modern React frontend for controlling track lights via the FastAPI backend.

## Features

- 🎨 **Color Control** - Select Red, Green, or Yellow lights with vibrant, animated buttons
- 🌈 **Mode Selection** - Switch between 6 different light modes with intuitive cards
- 📊 **Real-time Status** - Live status display showing current mode, color, and GPIO availability
- 🔄 **Auto-sync** - Automatically polls API every 3 seconds to stay in sync
- 💾 **State Persistence** - Reflects backend state even after restarts
- 📱 **Responsive Design** - Works beautifully on desktop, tablet, and mobile
- ✨ **Smooth Animations** - Delightful animations and transitions throughout

## Tech Stack

- **React 19** - Latest React with hooks
- **TypeScript** - Type-safe code
- **Vite** - Lightning-fast dev server and build tool
- **CSS3** - Modern styling with animations and gradients

## Getting Started

### Prerequisites

- Node.js 18+ installed
- Track Lights Controller API running on `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install
```

### Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` if your API is running on a different URL:
```
VITE_API_URL=http://your-api-url:8000
```

### Development

Start the development server:

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Production Build

Build for production:

```bash
npm run build
```

Preview the production build:

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ColorButton.tsx      # Color selection button component
│   │   ├── ColorButton.css      # Color button styles
│   │   ├── ModeSelector.tsx     # Mode selection grid component
│   │   ├── ModeSelector.css     # Mode selector styles
│   │   ├── StatusDisplay.tsx    # Status display component
│   │   └── StatusDisplay.css    # Status display styles
│   ├── api.ts                   # API service layer
│   ├── types.ts                 # TypeScript type definitions
│   ├── App.tsx                  # Main application component
│   ├── App.css                  # Main application styles
│   ├── main.tsx                 # Application entry point
│   └── index.css                # Global styles
├── public/                      # Static assets
├── .env.example                 # Environment variables template
├── vite.config.ts               # Vite configuration
├── tsconfig.json                # TypeScript configuration
└── package.json                 # Project dependencies
```

## Usage

### Color Control

Click on any color button (Red, Green, Yellow) to activate that light color. The active color will have a glowing animation and an indicator badge.

### Mode Selection

Choose from 6 different light modes:

1. **Breathe Colors** 🌈 - Smoothly cycle through colors
2. **Color Duration** ⏱️ - Display each color for a set duration
3. **Track Direction** ➡️ - Run lights along the track direction
4. **Circular Pattern** 🔄 - Run lights in a circular pattern
5. **White Mode** 💡 - Set all lights to white
6. **Turn Off** ⚫ - Turn off all lights

### System Reset

Click the "Reset System" button to:
- Turn off all lights
- Clear the controller state
- Return to the initial state

A confirmation dialog will appear before resetting.

## API Integration

The frontend communicates with the backend API using these endpoints:

- `GET /status` - Fetch current controller status
- `POST /color` - Set light color
- `POST /mode` - Set light mode
- `POST /reset` - Reset the system

The app automatically handles:
- Connection status
- Error messages
- Loading states
- Optimistic UI updates

## Customization

### Change Colors

Edit `src/components/ColorButton.tsx` to customize color values:

```typescript
const COLOR_CONFIG = {
  red: {
    bg: '#ef4444',      // Background color
    hoverBg: '#dc2626', // Hover state
    shadow: 'rgba(239, 68, 68, 0.5)', // Shadow color
  },
  // ...
};
```

### Adjust Polling Interval

Edit `src/App.tsx` to change how often status is fetched:

```typescript
// Poll for status every 3 seconds (change 3000 to desired milliseconds)
const interval = setInterval(fetchStatus, 3000);
```

### Theme Customization

Edit `src/App.css` to change the color scheme:

```css
.app {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  /* Change gradient colors here */
}
```

## Troubleshooting

### Can't connect to API

1. Make sure the backend API is running on `http://localhost:8000`
2. Check the `.env` file has the correct `VITE_API_URL`
3. Look for CORS errors in the browser console
4. Ensure the API is accessible from your machine

### CORS Issues

If you encounter CORS errors, add CORS middleware to your FastAPI backend:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Build Errors

1. Clear node_modules and reinstall:
```bash
rm -rf node_modules package-lock.json
npm install
```

2. Clear Vite cache:
```bash
rm -rf node_modules/.vite
```

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## License

MIT License
