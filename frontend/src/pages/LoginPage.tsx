import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { loginSchema } from '@/schemas/auth'
import { useAuthStore } from '@/store/auth'
import { Button } from '@/components/Button'
import { FormField } from '@/components/FormField'
import { Alert } from '@/components/Alert'

export function LoginPage() {
  const navigate = useNavigate()
  const { login, isLoading, error, clearError } = useAuthStore()
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({ resolver: zodResolver(loginSchema) })

  const onSubmit = async (data: any) => {
    try {
      await login(data.email, data.contrasena)
      navigate('/dashboard')
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-brand-50 to-brand-100">
      <div className="bg-white rounded-lg shadow-xl p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-brand-600 mb-2">🚗</h1>
          <h2 className="text-2xl font-bold">Respuestos La Tiendita</h2>
          <p className="text-slate-500 mt-2">Gestión de inventario profesional</p>
        </div>

        {error && (
          <Alert type="error" message={error} onClose={clearError} />
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="mt-8 space-y-4">
          <FormField label="Email" error={errors.email?.message as string}>
            <input
              type="email"
              {...register('email')}
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-600"
              placeholder="usuario@example.com"
            />
          </FormField>

          <FormField label="Contraseña" error={errors.contrasena?.message as string}>
            <input
              type="password"
              {...register('contrasena')}
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-600"
              placeholder="••••••••"
            />
          </FormField>

          <Button type="submit" isLoading={isLoading} className="w-full mt-6">
            Iniciar Sesión
          </Button>
        </form>

        <p className="text-center text-sm text-slate-600 mt-6">
          ¿No tienes cuenta?{' '}
          <a href="/registro" className="text-brand-600 hover:underline font-medium">
            Regístrate aquí
          </a>
        </p>
      </div>
    </div>
  )
}
