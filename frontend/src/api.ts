/**
 * API Service for Track Lights Controller
 */

import type {
  ControllerStatus,
  ColorResponse,
  ModeResponse,
  ResetResponse,
  LightColor,
  LightMode,
} from './types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiError extends Error {
  constructor(
    message: string,
    public statusCode?: number
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T> {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new ApiError(
        errorData.detail || `API error: ${response.statusText}`,
        response.status
      );
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(
      error instanceof Error ? error.message : 'Network error occurred'
    );
  }
}

export const api = {
  /**
   * Get current controller status
   */
  async getStatus(): Promise<ControllerStatus> {
    return fetchApi<ControllerStatus>('/status');
  },

  /**
   * Set light color
   */
  async setColor(color: LightColor): Promise<ColorResponse> {
    return fetchApi<ColorResponse>('/color', {
      method: 'POST',
      body: JSON.stringify({ color }),
    });
  },

  /**
   * Set light mode
   */
  async setMode(mode: LightMode): Promise<ModeResponse> {
    return fetchApi<ModeResponse>('/mode', {
      method: 'POST',
      body: JSON.stringify({ mode }),
    });
  },

  /**
   * Press mode button manually
   */
  async pressModeButton(count: number): Promise<ModeResponse> {
    return fetchApi<ModeResponse>('/mode/press', {
      method: 'POST',
      body: JSON.stringify({ count }),
    });
  },

  /**
   * Reset system
   */
  async reset(): Promise<ResetResponse> {
    return fetchApi<ResetResponse>('/reset', {
      method: 'POST',
    });
  },

  /**
   * Health check
   */
  async healthCheck(): Promise<{ status: string; controller_initialized: boolean }> {
    return fetchApi('/health');
  },
};

export { ApiError };
