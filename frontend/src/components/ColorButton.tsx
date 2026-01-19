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
    bg: '#ef4444',
    hoverBg: '#dc2626',
    shadow: 'rgba(239, 68, 68, 0.5)',
  },
  green: {
    label: 'Green',
    bg: '#22c55e',
    hoverBg: '#16a34a',
    shadow: 'rgba(34, 197, 94, 0.5)',
  },
  yellow: {
    label: 'Yellow',
    bg: '#eab308',
    hoverBg: '#ca8a04',
    shadow: 'rgba(234, 179, 8, 0.5)',
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
        '--button-bg': config.bg,
        '--button-hover-bg': config.hoverBg,
        '--button-shadow': config.shadow,
      } as React.CSSProperties}
      aria-label={`Set light to ${config.label}`}
    >
      <div className="color-button-inner">
        <div className="color-circle"></div>
        <span className="color-label">{config.label}</span>
      </div>
      {isActive && <div className="active-indicator">●</div>}
    </button>
  );
}
