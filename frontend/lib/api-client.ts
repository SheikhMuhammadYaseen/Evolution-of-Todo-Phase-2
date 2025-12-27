/**
 * API client for communicating with the FastAPI backend.
 * Handles JWT token attachment and error responses.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export class ApiClient {
  private static getHeaders(token?: string): Headers {
    const headers = new Headers({
      'Content-Type': 'application/json',
    });

    if (token) {
      headers.set('Authorization', `Bearer ${token}`);
    }

    return headers;
  }

  static async request<T>(
    endpoint: string,
    options: RequestInit = {},
    token?: string
  ): Promise<T> {
    const url = `${API_URL}${endpoint}`;
    const headers = this.getHeaders(token);

    const response = await fetch(url, {
      ...options,
      headers: {
        ...Object.fromEntries(headers),
        ...(options.headers || {}),
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error?.message || 'An error occurred');
    }

    // Handle 204 No Content responses (e.g., DELETE operations)
    if (response.status === 204) {
      return {} as T;
    }

    return response.json();
  }

  static async get<T>(endpoint: string, token?: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' }, token);
  }

  static async post<T>(
    endpoint: string,
    data: any,
    token?: string
  ): Promise<T> {
    return this.request<T>(
      endpoint,
      {
        method: 'POST',
        body: JSON.stringify(data),
      },
      token
    );
  }

  static async put<T>(
    endpoint: string,
    data: any,
    token?: string
  ): Promise<T> {
    return this.request<T>(
      endpoint,
      {
        method: 'PUT',
        body: JSON.stringify(data),
      },
      token
    );
  }

  static async delete<T>(endpoint: string, token?: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' }, token);
  }

  static async patch<T>(endpoint: string, token?: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'PATCH' }, token);
  }
}
