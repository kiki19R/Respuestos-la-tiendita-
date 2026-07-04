/**
 * Tipos globales de la aplicación
 */

export interface Usuario {
  id: number
  email: string
  nombre_completo: string
  rol: 'admin' | 'gerente' | 'vendedor'
  activo: boolean
  fecha_creacion: string
}

export interface AuthTokens {
  access_token: string
  refresh_token: string
  token_type: string
  usuario: Usuario
}

export interface Cliente {
  id: number
  nombre: string
  cedula?: string
  telefono?: string
  email?: string
  direccion?: string
  tipo: 'Consumidor Final' | 'Empresa'
  fecha_registro: string
}

export interface Proveedor {
  id: number
  nombre: string
  rif?: string
  telefono?: string
  email?: string
  contacto?: string
  direccion?: string
  activo: boolean
}

export interface Producto {
  id: number
  codigo: string
  nombre: string
  descripcion?: string
  precio_compra?: number
  precio_venta: number
  proveedor_id?: number
  activo: boolean
  cantidad_inventario?: number
}

export interface Inventario {
  id: number
  producto_id: number
  cantidad: number
  cantidad_minima: number
  ubicacion?: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  skip: number
  limit: number
}

export interface ApiError {
  detail: string
  status_code?: number
}
