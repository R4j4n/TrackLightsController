"""
FastAPI Backend for Track Lights Controller
Controls lights via GPIO-connected switches on Raspberry Pi
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
import logging
from contextlib import asynccontextmanager

from gpio_controller import GPIOController, LightMode, LightColor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Global controller instance
controller: Optional[GPIOController] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    global controller

    # Startup
    logger.info("Starting Track Lights Controller API")
    controller = GPIOController()
    yield

    # Shutdown
    logger.info("Shutting down Track Lights Controller API")
    if controller:
        controller.cleanup()


# Initialize FastAPI app
app = FastAPI(
    title="Track Lights Controller API",
    description="Control track lights via GPIO-connected switches on Raspberry Pi",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS - Allow all origins for easy development
# Simply change the IP in frontend/.env and it will work
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("CORS configured to allow all origins")


# Request/Response Models
class ColorRequest(BaseModel):
    """Request to set a specific color"""
    color: LightColor = Field(..., description="Color to activate (red, green, yellow)")


class ModeRequest(BaseModel):
    """Request to set a specific mode"""
    mode: LightMode = Field(..., description="Mode to activate")


class ModePressRequest(BaseModel):
    """Request to press the mode button a specific number of times"""
    count: int = Field(1, ge=1, le=6, description="Number of times to press SW4 (1-6)")


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "Track Lights Controller API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "status": "/status",
            "color": "/color",
            "mode": "/mode",
            "mode_press": "/mode/press",
            "reset": "/reset"
        }
    }


@app.get("/status")
async def get_status():
    """
    Get current status of the lights controller

    Returns:
        Current mode, last color pressed, and available options
    """
    if not controller:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Controller not initialized"
        )

    return controller.get_status()


@app.post("/color")
async def set_color(request: ColorRequest):
    """
    Press a color switch (SW1, SW2, or SW3)

    Args:
        request: Color to activate

    Returns:
        Action confirmation with details
    """
    print("color changedddd....")
    if not controller:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Controller not initialized"
        )

    try:
        result = controller.press_color_switch(request.color)
        logger.info(f"Color set to {request.color.value}")
        return result
    except Exception as e:
        logger.error(f"Error setting color: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to set color: {str(e)}"
        )


@app.post("/mode")
async def set_mode(request: ModeRequest):
    """
    Set the light mode by pressing SW4 the required number of times

    This endpoint remembers the last SW4 state and calculates how many
    presses are needed to reach the target mode.

    Args:
        request: Target mode to activate

    Returns:
        Action confirmation with mode details
    """
    if not controller:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Controller not initialized"
        )

    try:
        result = controller.set_mode(request.mode)
        logger.info(f"Mode set to {request.mode.value}")
        return result
    except Exception as e:
        logger.error(f"Error setting mode: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to set mode: {str(e)}"
        )


@app.post("/mode/press")
async def press_mode_button(request: ModePressRequest):
    """
    Press the mode switch (SW4) a specific number of times

    This allows manual control of SW4 presses, cycling through modes.

    Args:
        request: Number of times to press SW4

    Returns:
        Action confirmation with resulting mode
    """
    if not controller:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Controller not initialized"
        )

    try:
        result = controller.press_mode_switch(request.count)
        logger.info(f"Mode button pressed {request.count} time(s)")
        return result
    except Exception as e:
        logger.error(f"Error pressing mode button: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to press mode button: {str(e)}"
        )


@app.get("/modes")
async def list_modes():
    """
    List all available modes and their press counts

    Returns:
        Dictionary of modes with their corresponding SW4 press counts
    """
    return {
        "modes": [
            {"name": "breathe_colors", "press_count": 1, "description": "Breathe Colors"},
            {"name": "color_duration", "press_count": 2, "description": "Display each color for set duration"},
            {"name": "track_direction", "press_count": 3, "description": "Run lights along track direction"},
            {"name": "circular_pattern", "press_count": 4, "description": "Run lights in circular pattern"},
            {"name": "white_mode", "press_count": 5, "description": "Set lights to White Mode"},
            {"name": "off", "press_count": 6, "description": "Turn off the lights"}
        ]
    }


@app.get("/colors")
async def list_colors():
    """
    List all available colors

    Returns:
        List of available colors
    """
    return {
        "colors": [
            {"name": "red", "switch": "SW1", "gpio": 17},
            {"name": "green", "switch": "SW2", "gpio": 18},
            {"name": "yellow", "switch": "SW3", "gpio": 27}
        ]
    }


@app.post("/reset")
async def reset_system():
    """
    Reset the system by turning off lights and clearing state

    This endpoint will:
    1. Turn off the lights (set to OFF mode via 6 presses of SW4)
    2. Reset the internal state counter to 0
    3. Clear the last color pressed

    After reset, you can start fresh from the beginning.

    Returns:
        Reset confirmation with status
    """
    if not controller:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Controller not initialized"
        )

    try:
        result = controller.reset()
        logger.info("System reset successfully")
        return result
    except Exception as e:
        logger.error(f"Error resetting system: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reset system: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """
    Health check endpoint

    Returns:
        Health status of the API
    """
    return {
        "status": "healthy",
        "controller_initialized": controller is not None,
        "gpio_available": controller.get_status()["gpio_available"] if controller else False
    }


# Error handlers
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle value errors"""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn

    # Run the API server
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
