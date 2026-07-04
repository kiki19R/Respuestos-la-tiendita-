import React, { useEffect } from 'react'
import { useAuthStore } from '@/store/auth'

interface ProtectedRouteProps {
  children: React.ReactNode
  requiredRole?: string
}

export function ProtectedRoute({ children, requiredRole }: ProtectedRouteProps) {
  const { isAuthenticated, usuario } = useAuthStore()

  useEffect(() => {
    if (!isAuthenticated) {
      window.location.href = '/login'
    }
  }, [isAuthenticated])

  if (!isAuthenticated || !usuario) {
    return <div>Cargando...</div>
  }

  if (requiredRole && usuario.rol !== requiredRole) {
    return <div>No tienes permisos para acceder a esta página</div>
  }

  return <>{children}</>
}
