/**
 * TypeScript type definitions for the Todo application.
 */

export interface User {
  id: string;
  email: string;
  created_at: string;
}

export interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string | null;
  status: boolean;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
}

export interface TaskUpdate {
  title: string;
  description?: string | null;
}

export interface ApiError {
  error: {
    code: string;
    message: string;
    details?: Record<string, any>;
  };
}

export interface ApiResponse<T> {
  data?: T;
  error?: ApiError;
}
