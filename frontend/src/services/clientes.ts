import { apiClient } from './api'
import { Cliente } from '@/types'

export const clienteService = {
  async crear(data: any): Promise<Cliente> {
    const response = await apiClient.post<Cliente>('/api/v1/clientes', data)
    return response.data
  },

  async listar(skip: number = 0, limit: number = 100): Promise<Cliente[]> {
    const response = await apiClient.get<Cliente[]>('/api/v1/clientes', {
      params: { skip, limit },
    })
    return response.data
  },

  async buscar(nombre: string, skip: number = 0, limit: number = 100): Promise<Cliente[]> {
    const response = await apiClient.get<Cliente[]>('/api/v1/clientes/buscar', {
      params: { nombre, skip, limit },
    })
    return response.data
  },

  async obtener(id: number): Promise<Cliente> {
    const response = await apiClient.get<Cliente>(`/api/v1/clientes/${id}`)
    return response.data
  },

  async actualizar(id: number, data: any): Promise<Cliente> {
    const response = await apiClient.put<Cliente>(`/api/v1/clientes/${id}`, data)
    return response.data
  },

  async eliminar(id: number): Promise<void> {
    await apiClient.delete(`/api/v1/clientes/${id}`)
  },
}
