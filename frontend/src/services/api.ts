import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { jwtDecode } from 'jwt-decode';
import { toast } from 'react-hot-toast';

// Types
export interface ApiConfig {
  baseURL: string;
  timeout: number;
  headers?: Record<string, string>;
}

export interface TokenData {
  exp: number;
  user_id: number;
  role: string;
}

// API Configuration
const API_CONFIG: ApiConfig = {
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
};

// Cache configuration
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes
const cache = new Map<string, { data: any; timestamp: number }>();

class ApiService {
  private api: AxiosInstance;
  private tokenRefreshPromise: Promise<string> | null = null;

  constructor() {
    this.api = axios.create(API_CONFIG);
    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor
    this.api.interceptors.request.use(
      (config) => {
        const token = this.getAccessToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.api.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            const newToken = await this.refreshToken();
            originalRequest.headers.Authorization = `Bearer ${newToken}`;
            return this.api(originalRequest);
          } catch (refreshError) {
            this.handleAuthError();
            return Promise.reject(refreshError);
          }
        }

        return Promise.reject(error);
      }
    );
  }

  private getAccessToken(): string | null {
    return localStorage.getItem('access_token');
  }

  private getRefreshToken(): string | null {
    return localStorage.getItem('refresh_token');
  }

  private setTokens(access: string, refresh: string) {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
  }

  private clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  private isTokenExpired(token: string): boolean {
    try {
      const decoded = jwtDecode<TokenData>(token);
      return decoded.exp * 1000 < Date.now();
    } catch {
      return true;
    }
  }

  private async refreshToken(): Promise<string> {
    if (this.tokenRefreshPromise) {
      return this.tokenRefreshPromise;
    }

    this.tokenRefreshPromise = new Promise(async (resolve, reject) => {
      try {
        const refreshToken = this.getRefreshToken();
        if (!refreshToken) {
          throw new Error('No refresh token available');
        }

        const response = await axios.post(`${API_CONFIG.baseURL}/auth/refresh/`, {
          refresh: refreshToken,
        });

        const { access, refresh } = response.data;
        this.setTokens(access, refresh);
        resolve(access);
      } catch (error) {
        this.clearTokens();
        reject(error);
      } finally {
        this.tokenRefreshPromise = null;
      }
    });

    return this.tokenRefreshPromise;
  }

  private handleAuthError() {
    this.clearTokens();
    window.location.href = '/login';
  }

  // Cache management
  private getCacheKey(url: string, params?: any): string {
    return `${url}${params ? JSON.stringify(params) : ''}`;
  }

  private getFromCache(key: string): any | null {
    const cached = cache.get(key);
    if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
      return cached.data;
    }
    cache.delete(key);
    return null;
  }

  private setCache(key: string, data: any) {
    cache.set(key, { data, timestamp: Date.now() });
  }

  private clearCache() {
    cache.clear();
  }

  // Generic request methods
  async get<T>(url: string, config?: AxiosRequestConfig, useCache = true): Promise<T> {
    const cacheKey = this.getCacheKey(url, config?.params);
    
    if (useCache) {
      const cached = this.getFromCache(cacheKey);
      if (cached) return cached;
    }

    try {
      const response: AxiosResponse<T> = await this.api.get(url, config);
      
      if (useCache) {
        this.setCache(cacheKey, response.data);
      }
      
      return response.data;
    } catch (error) {
      this.handleApiError(error);
      throw error;
    }
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    try {
      const response: AxiosResponse<T> = await this.api.post(url, data, config);
      return response.data;
    } catch (error) {
      this.handleApiError(error);
      throw error;
    }
  }

  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    try {
      const response: AxiosResponse<T> = await this.api.put(url, data, config);
      return response.data;
    } catch (error) {
      this.handleApiError(error);
      throw error;
    }
  }

  async patch<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    try {
      const response: AxiosResponse<T> = await this.api.patch(url, data, config);
      return response.data;
    } catch (error) {
      this.handleApiError(error);
      throw error;
    }
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    try {
      const response: AxiosResponse<T> = await this.api.delete(url, config);
      return response.data;
    } catch (error) {
      this.handleApiError(error);
      throw error;
    }
  }

  // File upload with progress
  async uploadFile<T>(
    url: string,
    file: File,
    onProgress?: (progress: number) => void
  ): Promise<T> {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response: AxiosResponse<T> = await this.api.post(url, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          if (onProgress && progressEvent.total) {
            const progress = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            onProgress(progress);
          }
        },
      });
      return response.data;
    } catch (error) {
      this.handleApiError(error);
      throw error;
    }
  }

  // Error handling
  private handleApiError(error: any) {
    let message = 'An unexpected error occurred';

    if (error.response) {
      const { status, data } = error.response;
      
      switch (status) {
        case 400:
          message = data.message || 'Bad request';
          break;
        case 401:
          message = 'Unauthorized access';
          break;
        case 403:
          message = 'Access forbidden';
          break;
        case 404:
          message = 'Resource not found';
          break;
        case 422:
          message = data.message || 'Validation error';
          break;
        case 500:
          message = 'Internal server error';
          break;
        default:
          message = data.message || `Error ${status}`;
      }
    } else if (error.request) {
      message = 'Network error - please check your connection';
    } else {
      message = error.message || 'An error occurred';
    }

    toast.error(message);
  }

  // Authentication methods
  async login(credentials: { email: string; password: string; role: string }) {
    try {
      const response = await this.post<{
        user: any;
        access: string;
        refresh: string;
      }>('/auth/login/', credentials);

      this.setTokens(response.access, response.refresh);
      return response;
    } catch (error) {
      throw error;
    }
  }

  async register(userData: any) {
    try {
      const response = await this.post<{
        user: any;
        access: string;
        refresh: string;
      }>('/auth/register/', userData);

      this.setTokens(response.access, response.refresh);
      return response;
    } catch (error) {
      throw error;
    }
  }

  async logout() {
    try {
      await this.post('/auth/logout/');
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      this.clearTokens();
      this.clearCache();
    }
  }

  async getCurrentUser() {
    try {
      return await this.get<any>('/auth/user/');
    } catch (error) {
      throw error;
    }
  }

  // Utility methods
  isAuthenticated(): boolean {
    const token = this.getAccessToken();
    return token ? !this.isTokenExpired(token) : false;
  }

  getTokenData(): TokenData | null {
    const token = this.getAccessToken();
    if (!token) return null;

    try {
      return jwtDecode<TokenData>(token);
    } catch {
      return null;
    }
  }

  // Cache management
  invalidateCache(pattern?: string) {
    if (pattern) {
      for (const key of cache.keys()) {
        if (key.includes(pattern)) {
          cache.delete(key);
        }
      }
    } else {
      this.clearCache();
    }
  }
}

// Create singleton instance
export const apiService = new ApiService();

// Export for use in other modules
export default apiService;