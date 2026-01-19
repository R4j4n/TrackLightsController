"""
State Manager for Track Lights Controller
Handles persistent storage of controller state across restarts
"""

import json
import os
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from pathlib import Path


class StateManager:
    """Manages persistent state storage for the lights controller"""

    def __init__(self, state_file: str = "state.json"):
        """
        Initialize state manager

        Args:
            state_file: Path to the state file (relative or absolute)
        """
        self.logger = logging.getLogger(__name__)

        # Use absolute path relative to this module's directory
        if not os.path.isabs(state_file):
            module_dir = os.path.dirname(os.path.abspath(__file__))
            self.state_file = os.path.join(module_dir, state_file)
        else:
            self.state_file = state_file

        self.logger.info(f"State file location: {self.state_file}")

    def save_state(self, current_mode_press_count: int, last_color_pressed: Optional[str]) -> bool:
        """
        Save current state to disk

        Uses atomic write (write to temp file, then rename) to prevent corruption

        Args:
            current_mode_press_count: Current SW4 press count (0-6)
            last_color_pressed: Last color that was pressed (or None)

        Returns:
            True if save successful, False otherwise
        """
        try:
            state_data = {
                "current_mode_press_count": current_mode_press_count,
                "last_color_pressed": last_color_pressed,
                "last_updated": datetime.now().isoformat()
            }

            # Write to temporary file first (atomic operation)
            temp_file = f"{self.state_file}.tmp"

            with open(temp_file, 'w') as f:
                json.dump(state_data, f, indent=2)

            # Atomically replace the old file with the new one
            os.replace(temp_file, self.state_file)

            self.logger.debug(f"State saved: mode_count={current_mode_press_count}, color={last_color_pressed}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to save state: {str(e)}")
            return False

    def load_state(self) -> Dict[str, Any]:
        """
        Load state from disk

        Returns:
            Dictionary with 'current_mode_press_count' and 'last_color_pressed'
            Returns defaults if file doesn't exist or is corrupted
        """
        default_state = {
            "current_mode_press_count": 0,
            "last_color_pressed": None
        }

        if not os.path.exists(self.state_file):
            self.logger.info("No state file found, starting with defaults")
            return default_state

        try:
            with open(self.state_file, 'r') as f:
                state_data = json.load(f)

            # Validate required fields
            if "current_mode_press_count" not in state_data:
                self.logger.warning("State file missing 'current_mode_press_count', using defaults")
                return default_state

            # Validate mode press count range
            mode_count = state_data["current_mode_press_count"]
            if not isinstance(mode_count, int) or mode_count < 0 or mode_count > 6:
                self.logger.warning(f"Invalid mode_press_count: {mode_count}, using defaults")
                return default_state

            loaded_state = {
                "current_mode_press_count": mode_count,
                "last_color_pressed": state_data.get("last_color_pressed")
            }

            last_updated = state_data.get("last_updated", "unknown")
            self.logger.info(f"State loaded: mode_count={mode_count}, color={loaded_state['last_color_pressed']}, last_updated={last_updated}")

            return loaded_state

        except json.JSONDecodeError as e:
            self.logger.error(f"Corrupted state file: {str(e)}, using defaults")
            return default_state
        except Exception as e:
            self.logger.error(f"Failed to load state: {str(e)}, using defaults")
            return default_state

    def clear_state(self) -> bool:
        """
        Clear the state file (used during reset)

        Returns:
            True if cleared successfully, False otherwise
        """
        try:
            if os.path.exists(self.state_file):
                os.remove(self.state_file)
                self.logger.info("State file cleared")
            return True
        except Exception as e:
            self.logger.error(f"Failed to clear state file: {str(e)}")
            return False

    def get_state_file_path(self) -> str:
        """
        Get the absolute path to the state file

        Returns:
            Absolute path to state file
        """
        return self.state_file

    def state_file_exists(self) -> bool:
        """
        Check if state file exists

        Returns:
            True if state file exists, False otherwise
        """
        return os.path.exists(self.state_file)
