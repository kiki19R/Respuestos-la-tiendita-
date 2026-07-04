import { z } from 'zod'

export const loginSchema = z.object({
  email: z.string().email('Email inválido'),
  contrasena: z.string().min(8, 'Mínimo 8 caracteres'),
})

export const registroSchema = z
  .object({
    email: z.string().email('Email inválido'),
    nombre_completo: z.string().min(3, 'Mínimo 3 caracteres'),
    contrasena: z.string().min(8, 'Mínimo 8 caracteres'),
    contrasena_confirmacion: z.string(),
    rol: z.enum(['vendedor', 'gerente', 'admin']).default('vendedor'),
  })
  .refine((data) => data.contrasena === data.contrasena_confirmacion, {
    message: 'Las contraseñas no coinciden',
    path: ['contrasena_confirmacion'],
  })

export type LoginRequest = z.infer<typeof loginSchema>
export type RegistroRequest = z.infer<typeof registroSchema>
