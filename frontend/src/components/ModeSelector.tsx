/**
 * Mode Selector Component
 * Grid of mode selection cards
 */

import { LightMode, ModeInfo } from '../types';
import './ModeSelector.css';

interface ModeSelectorProps {
  currentMode: LightMode | null;
  onModeSelect: (mode: LightMode) => void;
  disabled?: boolean;
}

const MODES: ModeInfo[] = [
  {
    name: 'breathe_colors',
    press_count: 1,
    description: 'Breathe Colors',
    icon: '',
  },
  {
    name: 'color_duration',
    press_count: 2,
    description: 'Color Duration',
    icon: '',
  },
  {
    name: 'track_direction',
    press_count: 3,
    description: 'Track Direction',
    icon: '',
  },
  {
    name: 'circular_pattern',
    press_count: 4,
    description: 'Circular Pattern',
    icon: '',
  },
  {
    name: 'white_mode',
    press_count: 5,
    description: 'White Mode',
    icon: '',
  },
  {
    name: 'off',
    press_count: 6,
    description: 'Turn Off',
    icon: '',
  },
];

export function ModeSelector({ currentMode, onModeSelect, disabled }: ModeSelectorProps) {
  return (
    <div className="mode-selector">
      <h2 className="mode-selector-title">Light Modes</h2>
      <div className="mode-grid">
        {MODES.map((mode) => (
          <button
            key={mode.name}
            className={`mode-card ${currentMode === mode.name ? 'active' : ''}`}
            onClick={() => onModeSelect(mode.name)}
            disabled={disabled}
            aria-label={`Set mode to ${mode.description}`}
          >
            <div className="mode-info">
              <div className="mode-name">{mode.description}</div>
              <div className="mode-press-count">{mode.press_count} press{mode.press_count !== 1 ? 'es' : ''}</div>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
