import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { Navbar } from '@/components/Navbar'
import { ProtectedRoute } from '@/components/ProtectedRoute'
import { useAuthStore } from '@/store/auth'
import { TrendingUp, Users, Package, BarChart3 } from 'lucide-react'

export function DashboardPage() {
  const { usuario } = useAuthStore()

  const stats = [
    { label: 'Ventas del Mes', value: '$45,230', icon: TrendingUp, color: 'text-green-600' },
    { label: 'Clientes', value: '1,234', icon: Users, color: 'text-blue-600' },
    { label: 'Productos', value: '567', icon: Package, color: 'text-purple-600' },
    { label: 'Órdenes Pendientes', value: '12', icon: BarChart3, color: 'text-orange-600' },
  ]

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-slate-50">
        <Navbar />
        <main className="container py-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold">Bienvenido, {usuario?.nombre_completo}!</h1>
            <p className="text-slate-600 mt-2">Panel de control del sistema ERP</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {stats.map((stat, idx) => {
              const Icon = stat.icon
              return (
                <div key={idx} className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-slate-600 text-sm font-medium">{stat.label}</p>
                      <p className="text-2xl font-bold mt-2">{stat.value}</p>
                    </div>
                    <Icon className={`${stat.color}`} size={32} />
                  </div>
                </div>
              )
            })}
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4">Acciones Rápidas</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <a href="/ventas/nueva" className="p-4 border border-brand-200 rounded-lg hover:bg-brand-50 transition">
                <p className="font-medium text-brand-600">Nueva Venta</p>
              </a>
              <a href="/clientes" className="p-4 border border-slate-200 rounded-lg hover:bg-slate-50 transition">
                <p className="font-medium">Gestionar Clientes</p>
              </a>
              <a href="/productos" className="p-4 border border-slate-200 rounded-lg hover:bg-slate-50 transition">
                <p className="font-medium">Gestionar Productos</p>
              </a>
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  )
}
