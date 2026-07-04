import { apiClient } from './api'
import { AuthTokens, Usuario } from '@/types'
import { LoginRequest, RegistroRequest } from '@/schemas/auth'

export const authService = {
  async login(data: LoginRequest): Promise<AuthTokens> {
    const response = await apiClient.post<AuthTokens>('/api/v1/auth/login', data)
    apiClient.setTokens(response.data)
    return response.data
  },

  async registro(data: RegistroRequest): Promise<AuthTokens> {
    const response = await apiClient.post<AuthTokens>('/api/v1/auth/registro', data)
    apiClient.setTokens(response.data)
    return response.data
  },

  async obtenerUsuario(): Promise<Usuario> {
    const response = await apiClient.get<Usuario>('/api/v1/auth/me')
    return response.data
  },

  logout() {
    apiClient.clearTokens()
  },
}
