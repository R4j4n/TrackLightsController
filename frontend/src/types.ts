/**
 * TypeScript types for Track Lights Controller API
 */

export type LightColor = 'red' | 'green' | 'yellow';

export type LightMode =
  | 'breathe_colors'
  | 'color_duration'
  | 'track_direction'
  | 'circular_pattern'
  | 'white_mode'
  | 'off';

export interface ControllerStatus {
  gpio_available: boolean;
  current_mode_press_count: number;
  current_mode: LightMode | null;
  last_color_pressed: LightColor | null;
  available_modes: string[];
  available_colors: string[];
}

export interface ColorResponse {
  action: string;
  color: LightColor;
  gpio_pin: number;
  timestamp: number;
}

export interface ModeResponse {
  action: string;
  press_count?: number;
  total_mode_presses: number;
  current_mode: LightMode;
  gpio_pin: number;
  timestamp: number;
}

export interface ResetResponse {
  action: string;
  lights_off: boolean;
  state_cleared: boolean;
  current_mode_press_count: number;
  timestamp: number;
  message: string;
}

export interface ModeInfo {
  name: LightMode;
  press_count: number;
  description: string;
  icon: string;
}
