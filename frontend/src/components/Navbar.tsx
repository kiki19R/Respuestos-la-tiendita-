import React from 'react'
import { useAuthStore } from '@/store/auth'
import { LogOut, User } from 'lucide-react'

export function Navbar() {
  const { usuario, logout } = useAuthStore()

  const handleLogout = () => {
    logout()
    window.location.href = '/login'
  }

  return (
    <nav className="bg-white shadow-md">
      <div className="container flex items-center justify-between py-4">
        <div className="flex items-center gap-2">
          <div className="text-2xl font-bold text-brand-600">🚗 Respuestos</div>
        </div>

        <div className="flex items-center gap-6">
          {usuario && (
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2">
                <User size={20} className="text-slate-600" />
                <div>
                  <p className="font-medium">{usuario.nombre_completo}</p>
                  <p className="text-xs text-slate-500 capitalize">{usuario.rol}</p>
                </div>
              </div>
              <button
                onClick={handleLogout}
                className="flex items-center gap-2 px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg"
              >
                <LogOut size={18} />
                Salir
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  )
}
