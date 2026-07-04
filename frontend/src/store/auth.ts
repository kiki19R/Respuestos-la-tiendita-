import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { Usuario } from '@/types'
import { authService } from '@/services/auth'

interface AuthStore {
  usuario: Usuario | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
  login: (email: string, contrasena: string) => Promise<void>
  registro: (data: any) => Promise<void>
  obtenerUsuario: () => Promise<void>
  logout: () => void
  clearError: () => void
}

export const useAuthStore = create<AuthStore>()()
  persist(
    (set, get) => ({
      usuario: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (email: string, contrasena: string) => {
        set({ isLoading: true, error: null })
        try {
          const result = await authService.login({ email, contrasena })
          set({
            usuario: result.usuario,
            isAuthenticated: true,
            isLoading: false,
          })
        } catch (error: any) {
          set({
            error: error.response?.data?.detail || 'Error al iniciar sesión',
            isLoading: false,
          })
          throw error
        }
      },

      registro: async (data: any) => {
        set({ isLoading: true, error: null })
        try {
          const result = await authService.registro(data)
          set({
            usuario: result.usuario,
            isAuthenticated: true,
            isLoading: false,
          })
        } catch (error: any) {
          set({
            error: error.response?.data?.detail || 'Error al registrar',
            isLoading: false,
          })
          throw error
        }
      },

      obtenerUsuario: async () => {
        try {
          const usuario = await authService.obtenerUsuario()
          set({ usuario, isAuthenticated: true })
        } catch (error) {
          set({ isAuthenticated: false, usuario: null })
        }
      },

      logout: () => {
        authService.logout()
        set({ usuario: null, isAuthenticated: false })
      },

      clearError: () => set({ error: null }),
    }),
    {
      name: 'auth-store',
    }
  )
