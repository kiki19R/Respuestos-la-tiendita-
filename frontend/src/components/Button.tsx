import React from 'react'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  isLoading?: boolean
}

export function Button({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  children,
  disabled,
  ...props
}: ButtonProps) {
  const variantClasses = {
    primary: 'bg-brand-600 hover:bg-brand-700 text-white',
    secondary: 'bg-slate-200 hover:bg-slate-300 text-slate-900',
    danger: 'bg-red-600 hover:bg-red-700 text-white',
  }

  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  }

  return (
    <button
      disabled={disabled || isLoading}
      className={`rounded-lg font-medium transition-colors ${variantClasses[variant]} ${sizeClasses[size]} disabled:opacity-50 disabled:cursor-not-allowed`}
      {...props}
    >
      {isLoading ? 'Cargando...' : children}
    </button>
  )
}
