// src/features/machines/schemas/machineSchema.ts
import { z } from 'zod';

export const machineSchema = z.object({
  nom: z.string().min(1, "Le nom est requis"),
  description: z.string().optional(),
  localisation: z.string().optional(),
  type: z.string().optional(),
  date_installation: z.string().optional(),
  etat: z.enum(['SERVICE', 'PANNE', 'MAINTENANCE']),
});

export type MachineFormData = z.infer<typeof machineSchema>;