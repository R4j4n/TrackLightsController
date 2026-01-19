/**
 * Main App Component
 * Track Lights Controller Frontend
 */

import { useState, useEffect, useCallback } from 'react';
import { api, ApiError } from './api';
import { ControllerStatus, LightColor, LightMode } from './types';
import { ColorButton } from './components/ColorButton';
import { ModeSelector } from './components/ModeSelector';
import { StatusDisplay } from './components/StatusDisplay';
import './App.css';

function App() {
  const [status, setStatus] = useState<ControllerStatus | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  // Fetch status from API
  const fetchStatus = useCallback(async () => {
    try {
      const data = await api.getStatus();
      setStatus(data);
      setIsConnected(true);
      setError(null);
    } catch (err) {
      console.error('Failed to fetch status:', err);
      setIsConnected(false);
      if (err instanceof ApiError) {
        setError(err.message);
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Initial load and polling
  useEffect(() => {
    fetchStatus();

    // Poll for status every 3 seconds
    const interval = setInterval(fetchStatus, 3000);

    return () => clearInterval(interval);
  }, [fetchStatus]);

  // Handle color selection
  const handleColorSelect = async (color: LightColor) => {
    if (isProcessing) return;

    setIsProcessing(true);
    setError(null);

    try {
      await api.setColor(color);
      await fetchStatus(); // Refresh status
    } catch (err) {
      console.error('Failed to set color:', err);
      if (err instanceof ApiError) {
        setError(`Failed to set color: ${err.message}`);
      }
    } finally {
      setIsProcessing(false);
    }
  };

  // Handle mode selection
  const handleModeSelect = async (mode: LightMode) => {
    if (isProcessing) return;

    setIsProcessing(true);
    setError(null);

    try {
      await api.setMode(mode);
      await fetchStatus(); // Refresh status
    } catch (err) {
      console.error('Failed to set mode:', err);
      if (err instanceof ApiError) {
        setError(`Failed to set mode: ${err.message}`);
      }
    } finally {
      setIsProcessing(false);
    }
  };

  // Handle reset
  const handleReset = async () => {
    if (isProcessing) return;

    if (!confirm('Are you sure you want to reset the system? This will turn off the lights and clear all state.')) {
      return;
    }

    setIsProcessing(true);
    setError(null);

    try {
      await api.reset();
      await fetchStatus(); // Refresh status
    } catch (err) {
      console.error('Failed to reset:', err);
      if (err instanceof ApiError) {
        setError(`Failed to reset: ${err.message}`);
      }
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">
            <span className="title-icon">💡</span>
            Track Lights Controller
          </h1>
          <p className="app-subtitle">Control your track lights with style</p>
        </div>
      </header>

      <main className="app-main">
        {error && (
          <div className="error-banner">
            <span className="error-icon">⚠️</span>
            {error}
            <button className="error-dismiss" onClick={() => setError(null)}>×</button>
          </div>
        )}

        <div className="content-grid">
          {/* Status Section */}
          <section className="section status-section">
            <StatusDisplay
              status={status}
              isConnected={isConnected}
              isLoading={isLoading}
            />
          </section>

          {/* Color Controls Section */}
          <section className="section color-section">
            <h2 className="section-title">Light Colors</h2>
            <div className="color-buttons">
              <ColorButton
                color="red"
                isActive={status?.last_color_pressed === 'red'}
                onClick={() => handleColorSelect('red')}
                disabled={isProcessing || !isConnected}
              />
              <ColorButton
                color="green"
                isActive={status?.last_color_pressed === 'green'}
                onClick={() => handleColorSelect('green')}
                disabled={isProcessing || !isConnected}
              />
              <ColorButton
                color="yellow"
                isActive={status?.last_color_pressed === 'yellow'}
                onClick={() => handleColorSelect('yellow')}
                disabled={isProcessing || !isConnected}
              />
            </div>
          </section>

          {/* Mode Controls Section */}
          <section className="section mode-section">
            <ModeSelector
              currentMode={status?.current_mode || null}
              onModeSelect={handleModeSelect}
              disabled={isProcessing || !isConnected}
            />
          </section>

          {/* Reset Button Section */}
          <section className="section reset-section">
            <button
              className="reset-button"
              onClick={handleReset}
              disabled={isProcessing || !isConnected}
            >
              <span className="reset-icon">🔄</span>
              Reset System
            </button>
          </section>
        </div>
      </main>

      <footer className="app-footer">
        <p>Built with React + TypeScript + Vite</p>
        <p className="footer-status">
          {isConnected ? (
            <span className="status-connected">● Connected</span>
          ) : (
            <span className="status-disconnected">● Disconnected</span>
          )}
        </p>
      </footer>
    </div>
  );
}

export default App;
