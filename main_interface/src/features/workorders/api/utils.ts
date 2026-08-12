// src/features/workorders/api/utils.ts

//typage strict de données = par ids via api
//tout champ =number 
import type { WorkOrder } from "../types";

type IdOrObject = number | { id: number };

export function normalizeWorkOrderPayload(data: Partial<WorkOrder>) {
  return {
    ...data,
    machine: data.machine != null
      ? (typeof data.machine === "object" ? (data.machine as any).id : data.machine)
      : null,
    categorie: data.categorie != null
      ? (typeof data.categorie === "object" ? (data.categorie as any).id : data.categorie)
      : null,
    expert: data.expert != null
      ? (typeof data.expert === "object" ? (data.expert as any).id : data.expert)
      : null,
    techniciens: Array.isArray(data.techniciens)
      ? (data.techniciens as IdOrObject[]).map(t =>
          typeof t === "object" ? t.id : t
        )
      : [],
  };
}
