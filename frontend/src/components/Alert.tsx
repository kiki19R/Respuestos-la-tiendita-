import React from 'react'
import { AlertCircle } from 'lucide-react'

interface AlertProps {
  type: 'error' | 'success' | 'warning' | 'info'
  title?: string
  message: string
  onClose?: () => void
}

export function Alert({ type, title, message, onClose }: AlertProps) {
  const colors = {
    error: 'bg-red-50 border-red-200 text-red-800',
    success: 'bg-green-50 border-green-200 text-green-800',
    warning: 'bg-yellow-50 border-yellow-200 text-yellow-800',
    info: 'bg-blue-50 border-blue-200 text-blue-800',
  }

  return (
    <div className={`border rounded-lg p-4 ${colors[type]}`}>
      <div className="flex items-start gap-3">
        <AlertCircle size={20} className="flex-shrink-0 mt-0.5" />
        <div className="flex-1">
          {title && <p className="font-semibold mb-1">{title}</p>}
          <p>{message}</p>
        </div>
        {onClose && (
          <button
            onClick={onClose}
            className="text-sm font-medium opacity-70 hover:opacity-100"
          >
            ✕
          </button>
        )}
      </div>
    </div>
  )
}
