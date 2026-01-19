/**
 * Color Button Component
 * Interactive button for selecting light colors
 */

import { LightColor } from '../types';
import './ColorButton.css';

interface ColorButtonProps {
  color: LightColor;
  isActive: boolean;
  onClick: () => void;
  disabled?: boolean;
}

const COLOR_CONFIG = {
  red: {
    label: 'Red',
    color: '#ef4444',
  },
  green: {
    label: 'Green',
    color: '#22c55e',
  },
  yellow: {
    label: 'Yellow',
    color: '#fbbf24',
  },
};

export function ColorButton({ color, isActive, onClick, disabled }: ColorButtonProps) {
  const config = COLOR_CONFIG[color];

  return (
    <button
      className={`color-button ${isActive ? 'active' : ''}`}
      onClick={onClick}
      disabled={disabled}
      style={{
        '--button-color': config.color,
      } as React.CSSProperties}
      aria-label={`Set light to ${config.label}`}
    >
      <div className="color-button-inner">
        <div className="color-circle"></div>
        <span className="color-label">{config.label}</span>
      </div>
    </button>
  );
}
