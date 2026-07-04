import axios, { AxiosInstance, AxiosError } from 'axios'
import { AuthTokens } from '@/types'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

class ApiClient {
  private client: AxiosInstance
  private accessToken: string | null = null

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Interceptor para agregar token
    this.client.interceptors.request.use((config) => {
      if (this.accessToken) {
        config.headers.Authorization = `Bearer ${this.accessToken}`
      }
      return config
    })

    // Interceptor para manejo de errores
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          this.handleUnauthorized()
        }
        return Promise.reject(error)
      }
    )

    // Cargar token del localStorage
    this.loadToken()
  }

  private loadToken() {
    const tokens = localStorage.getItem('tokens')
    if (tokens) {
      try {
        const parsed = JSON.parse(tokens)
        this.accessToken = parsed.access_token
      } catch (e) {
        localStorage.removeItem('tokens')
      }
    }
  }

  private handleUnauthorized() {
    localStorage.removeItem('tokens')
    this.accessToken = null
    window.location.href = '/login'
  }

  setTokens(tokens: AuthTokens) {
    this.accessToken = tokens.access_token
    localStorage.setItem('tokens', JSON.stringify(tokens))
  }

  clearTokens() {
    this.accessToken = null
    localStorage.removeItem('tokens')
  }

  // GET
  get<T = any>(url: string, config?: any) {
    return this.client.get<T>(url, config)
  }

  // POST
  post<T = any>(url: string, data?: any, config?: any) {
    return this.client.post<T>(url, data, config)
  }

  // PUT
  put<T = any>(url: string, data?: any, config?: any) {
    return this.client.put<T>(url, data, config)
  }

  // PATCH
  patch<T = any>(url: string, data?: any, config?: any) {
    return this.client.patch<T>(url, data, config)
  }

  // DELETE
  delete<T = any>(url: string, config?: any) {
    return this.client.delete<T>(url, config)
  }
}

export const apiClient = new ApiClient()
