import { apiClient } from './api'
import { Producto } from '@/types'

export const productoService = {
  async crear(data: any): Promise<Producto> {
    const response = await apiClient.post<Producto>('/api/v1/productos', data)
    return response.data
  },

  async listar(skip: number = 0, limit: number = 100): Promise<Producto[]> {
    const response = await apiClient.get<Producto[]>('/api/v1/productos', {
      params: { skip, limit },
    })
    return response.data
  },

  async buscar(nombre: string, skip: number = 0, limit: number = 100): Promise<Producto[]> {
    const response = await apiClient.get<Producto[]>('/api/v1/productos/buscar', {
      params: { nombre, skip, limit },
    })
    return response.data
  },

  async obtenerPorCodigo(codigo: string): Promise<Producto> {
    const response = await apiClient.get<Producto>(`/api/v1/productos/codigo/${codigo}`)
    return response.data
  },

  async obtener(id: number): Promise<Producto> {
    const response = await apiClient.get<Producto>(`/api/v1/productos/${id}`)
    return response.data
  },

  async actualizar(id: number, data: any): Promise<Producto> {
    const response = await apiClient.put<Producto>(`/api/v1/productos/${id}`, data)
    return response.data
  },

  async actualizarPrecio(id: number, precio_venta: number): Promise<Producto> {
    const response = await apiClient.patch<Producto>(
      `/api/v1/productos/${id}/precio`,
      {},
      { params: { precio_venta } }
    )
    return response.data
  },
}
