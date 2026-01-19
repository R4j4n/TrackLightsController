/**
 * Status Display Component
 * Shows current light state with visual feedback
 */

import { ControllerStatus } from '../types';
import './StatusDisplay.css';

interface StatusDisplayProps {
  status: ControllerStatus | null;
  isConnected: boolean;
  isLoading: boolean;
}

export function StatusDisplay({ status, isConnected, isLoading }: StatusDisplayProps) {
  const getModeDisplayName = (mode: string | null) => {
    if (!mode) return 'Unknown';

    const modeNames: Record<string, string> = {
      breathe_colors: 'Breathe Colors',
      color_duration: 'Color Duration',
      track_direction: 'Track Direction',
      circular_pattern: 'Circular Pattern',
      white_mode: 'White Mode',
      off: 'Off',
    };

    return modeNames[mode] || mode;
  };

  const getColorDisplay = (color: string | null) => {
    if (!color) return null;

    return {
      name: color.charAt(0).toUpperCase() + color.slice(1),
      color: color,
    };
  };

  if (isLoading) {
    return (
      <div className="status-display loading">
        <div className="status-spinner"></div>
        <p>Connecting...</p>
      </div>
    );
  }

  if (!isConnected || !status) {
    return (
      <div className="status-display disconnected">
        <h3>Disconnected</h3>
        <p>Unable to connect to controller</p>
      </div>
    );
  }

  const colorDisplay = getColorDisplay(status.last_color_pressed);

  return (
    <div className="status-display connected">
      <div className="status-header">
        <div className="connection-indicator">
          <div className="connection-dot"></div>
          <span>Connected</span>
        </div>
      </div>

      <div className="status-grid">
        <div className="status-item">
          <div className="status-label">Current Mode</div>
          <div className="status-value mode-value">
            {getModeDisplayName(status.current_mode)}
          </div>
          <div className="status-detail">
            Press count: {status.current_mode_press_count}
          </div>
        </div>

        <div className="status-item">
          <div className="status-label">Last Color</div>
          <div
            className="status-value color-value"
            style={colorDisplay ? {
              '--color-dot': colorDisplay.color === 'red' ? 'var(--color-red)' :
                            colorDisplay.color === 'green' ? 'var(--color-green)' :
                            colorDisplay.color === 'yellow' ? 'var(--color-yellow)' : 'transparent'
            } as React.CSSProperties : undefined}
          >
            {colorDisplay ? colorDisplay.name : <span className="no-color">No color selected</span>}
          </div>
        </div>

        <div className="status-item">
          <div className="status-label">GPIO Status</div>
          <div className={`status-value gpio-value ${status.gpio_available ? 'available' : 'unavailable'}`}>
            {status.gpio_available ? (
              <>
                <span className="status-check">✓</span>
                Available
              </>
            ) : (
              <>
                <span className="status-cross">✗</span>
                Simulation Mode
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
