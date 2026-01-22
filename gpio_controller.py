"""
GPIO Controller for Track Lights System
Simulates switch presses by controlling GPIO pins on Raspberry Pi
"""

import time
from enum import Enum
from typing import Optional
import logging

from state_manager import StateManager

try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except (ImportError, RuntimeError):
    GPIO_AVAILABLE = False
    print("Warning: RPi.GPIO not available. Running in simulation mode.")


class LightMode(str, Enum):
    """Light modes corresponding to SW4 press count"""
    BREATHE_COLORS = "breathe_colors"      # 1 press
    COLOR_DURATION = "color_duration"       # 2 presses
    TRACK_DIRECTION = "track_direction"     # 3 presses
    CIRCULAR_PATTERN = "circular_pattern"   # 4 presses
    WHITE_MODE = "white_mode"               # 5 presses
    OFF = "off"                             # 6 presses


class LightColor(str, Enum):
    """Light colors for SW1-SW3"""
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"


class GPIOController:
    """Controller for managing GPIO switches"""

    # GPIO Pin Configuration
    PIN_SW1_RED = 17
    PIN_SW2_GREEN = 18
    PIN_SW3_YELLOW = 27
    PIN_SW4_MODE = 22

    # Mode press count mapping
    MODE_PRESS_COUNT = {
        LightMode.BREATHE_COLORS: 1,
        LightMode.COLOR_DURATION: 2,
        LightMode.TRACK_DIRECTION: 3,
        LightMode.CIRCULAR_PATTERN: 4,
        LightMode.WHITE_MODE: 5,
        LightMode.OFF: 6,
    }

    # Reverse mapping
    PRESS_COUNT_TO_MODE = {v: k for k, v in MODE_PRESS_COUNT.items()}

    def __init__(self):
        """Initialize GPIO controller"""
        self.logger = logging.getLogger(__name__)

        # Initialize state manager
        self.state_manager = StateManager()

        # Load saved state from disk
        saved_state = self.state_manager.load_state()
        self.current_mode_press_count = saved_state["current_mode_press_count"]

        # Convert saved color string back to enum
        last_color_str = saved_state["last_color_pressed"]
        if last_color_str:
            try:
                self.last_color_pressed = LightColor(last_color_str)
            except ValueError:
                self.logger.warning(f"Invalid saved color '{last_color_str}', ignoring")
                self.last_color_pressed = None
        else:
            self.last_color_pressed = None

        if GPIO_AVAILABLE:
            # Set up GPIO using BCM numbering
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)

            # Configure pins as outputs (we're simulating button presses)
            GPIO.setup(self.PIN_SW1_RED, GPIO.OUT, initial=GPIO.HIGH)
            GPIO.setup(self.PIN_SW2_GREEN, GPIO.OUT, initial=GPIO.HIGH)
            GPIO.setup(self.PIN_SW3_YELLOW, GPIO.OUT, initial=GPIO.HIGH)
            GPIO.setup(self.PIN_SW4_MODE, GPIO.OUT, initial=GPIO.HIGH)

            self.logger.info("GPIO initialized successfully")
        else:
            self.logger.warning("Running in simulation mode - GPIO not available")

        self.logger.info(f"Controller initialized - mode_count: {self.current_mode_press_count}, last_color: {self.last_color_pressed}")

    def _simulate_button_press(self, pin: int, duration: float = 0.2) -> None:
        """
        Simulate a button press by pulling the pin LOW then HIGH

        Args:
            pin: GPIO pin number
            duration: How long to hold the button press (seconds)
        """
        if GPIO_AVAILABLE:
            GPIO.output(pin, GPIO.LOW)  # Button pressed
            time.sleep(duration)
            GPIO.output(pin, GPIO.HIGH)  # Button released
            time.sleep(0.1)  # Small delay between presses
        else:
            self.logger.info(f"[SIMULATION] Button press on GPIO {pin} for {duration}s")
            time.sleep(duration)

    def press_color_switch(self, color: LightColor) -> dict:
        """
        Press a color switch (SW1, SW2, or SW3)

        Args:
            color: Color to activate

        Returns:
            Status information
        """
        pin_map = {
            LightColor.RED: self.PIN_SW1_RED,
            LightColor.GREEN: self.PIN_SW2_GREEN,
            LightColor.YELLOW: self.PIN_SW3_YELLOW,
        }

        pin = pin_map[color]
        self._simulate_button_press(pin)
        self.last_color_pressed = color

        # Pressing a color button resets the mode cycle on the hardware
        # Reset mode press count so next mode selection calculates correctly
        self.current_mode_press_count = 0

        # Save state after color change
        self.state_manager.save_state(
            self.current_mode_press_count,
            self.last_color_pressed.value
        )

        self.logger.info(f"Pressed {color.value} switch (GPIO {pin})")

        return {
            "action": "color_switch_pressed",
            "color": color.value,
            "gpio_pin": pin,
            "timestamp": time.time()
        }

    def press_mode_switch(self, count: int = 1) -> dict:
        """
        Press the mode switch (SW4) a specified number of times

        Args:
            count: Number of times to press the switch

        Returns:
            Status information including new mode
        """
        for i in range(count):
            self._simulate_button_press(self.PIN_SW4_MODE)
            self.current_mode_press_count = (self.current_mode_press_count % 6) + 1
            self.logger.info(f"Mode switch press {i+1}/{count} - count now: {self.current_mode_press_count}")

            # Small delay between multiple presses
            if i < count - 1:
                time.sleep(0.02)

        current_mode = self.PRESS_COUNT_TO_MODE[self.current_mode_press_count]

        # Save state after mode change
        self.state_manager.save_state(
            self.current_mode_press_count,
            self.last_color_pressed.value if self.last_color_pressed else None
        )

        return {
            "action": "mode_switch_pressed",
            "press_count": count,
            "total_mode_presses": self.current_mode_press_count,
            "current_mode": current_mode.value,
            "gpio_pin": self.PIN_SW4_MODE,
            "timestamp": time.time()
        }

    def set_mode(self, target_mode: LightMode) -> dict:
        """
        Set the light to a specific mode by pressing SW4 the required number of times

        Args:
            target_mode: Desired mode

        Returns:
            Status information
        """
        target_count = self.MODE_PRESS_COUNT[target_mode]
        current_count = self.current_mode_press_count

        # Calculate how many presses needed (cycles through 1-6)
        # Special case: current_count = 0 means no mode is set yet (initial/reset state)
        if current_count == 0:
            # From initial state, just press target_count times
            presses_needed = target_count
        elif target_count == current_count:
            presses_needed = 0
        elif target_count > current_count:
            presses_needed = target_count - current_count
        else:
            # Need to cycle around (e.g., from 5 to 2 = 3 presses: 5->6->1->2)
            presses_needed = (6 - current_count) + target_count

        self.logger.info(f"Setting mode to {target_mode.value}: need {presses_needed} presses")

        if presses_needed > 0:
            return self.press_mode_switch(presses_needed)
        else:
            return {
                "action": "mode_already_set",
                "current_mode": target_mode.value,
                "total_mode_presses": self.current_mode_press_count,
                "timestamp": time.time()
            }

    def reset(self) -> dict:
        """
        Reset the system by turning off the lights and resetting state to beginning

        This sets the lights to OFF mode (6 presses) and resets the internal state,
        allowing you to start from the beginning.

        Returns:
            Status information about the reset
        """
        # First, set to OFF mode (6 presses)
        result = self.set_mode(LightMode.OFF)

        # Reset internal state to start from beginning
        self.current_mode_press_count = 0
        self.last_color_pressed = None

        # Clear saved state file
        self.state_manager.clear_state()

        self.logger.info("System reset - lights off, state cleared")

        return {
            "action": "system_reset",
            "lights_off": True,
            "state_cleared": True,
            "current_mode_press_count": self.current_mode_press_count,
            "timestamp": time.time(),
            "message": "System reset successfully. Lights are off and ready to start from beginning."
        }

    def get_status(self) -> dict:
        """
        Get current status of the controller

        Returns:
            Current status information
        """
        current_mode = self.PRESS_COUNT_TO_MODE.get(
            self.current_mode_press_count,
            None
        )

        return {
            "gpio_available": GPIO_AVAILABLE,
            "current_mode_press_count": self.current_mode_press_count,
            "current_mode": current_mode.value if current_mode else None,
            "last_color_pressed": self.last_color_pressed.value if self.last_color_pressed else None,
            "available_modes": [mode.value for mode in LightMode],
            "available_colors": [color.value for color in LightColor],
        }

    def cleanup(self) -> None:
        """Clean up GPIO resources"""
        if GPIO_AVAILABLE:
            GPIO.cleanup()
            self.logger.info("GPIO cleaned up")
