// src/features/workorders/componenents/WorkOrderForm.tsx


import { useState, useEffect } from 'react';
import type { WorkOrder, WorkOrderWithDetails } from '../types';
import { useCategories } from '../../users/hooks/useCategories';
import { useUsers } from '../../users/hooks/useUsers';
import { useAuthStore } from '../../../store/authStore';
import { useMachines } from "../../machines/hooks/useMachines";
import { useSignalements } from "../../signalements/hooks/useSignalements";
import { normalizeWorkOrderPayload } from "../api/utils"; // utilitaire créé
import type { Machine } from "../../machines/types";
import type { SignalementWithDetails } from '@/features/signalements/types';

import { toast } from "react-toastify";
//import { Link } from "react-router-dom";

interface WorkOrderFormProps {
  initialData?: Partial<WorkOrder>;
  onSubmit: (data: Partial<WorkOrder>) => Promise<WorkOrderWithDetails>; // ✅ plus de void
  isLoading?: boolean;
  signalement?: SignalementWithDetails;   // ✅ nouvelle prop
  onClose?: () => void;                   // ✅ utile pour pop-up
  onCreated?: (workorderId: number) => void; // ✅ callback après création

  
}

export const WorkOrderForm = ({
  initialData = {},
  onSubmit,
  isLoading = false,
  signalement,
  onClose,
  onCreated,

}: WorkOrderFormProps) => {
  const { user } = useAuthStore();
  const [formData, setFormData] = useState<Partial<WorkOrder>>(initialData);

  // ✅ Préremplir machine + signalement si fourni
  useEffect(() => {
    if (signalement) {
      setFormData(prev => ({
        ...prev,
        machine: signalement.machine,
        signalement: signalement.id,
        description: signalement.description ?? prev.description,
      }));
    }
  }, [signalement]);

  const { data: categories } = useCategories();
  const { data: users } = useUsers();


  /*
  const { data: machines } = useMachines(); // récupération des machines
  */
  

  const { data: machinesData } = useMachines();
  const machines: Machine[] = Array.isArray(machinesData)
    ? machinesData
    : (machinesData as any)?.results ?? [];
  
  const { data: signalements } = useSignalements();

  // ✅ Préremplir expert si connecté
  useEffect(() => {
    if (user?.role === 'expert') {
      setFormData(prev => ({ ...prev, expert: user.id }));
    }
  }, [user]);

  // ✅ Filtrer techniciens selon la catégorie choisie
  const techniciens = users?.filter(
    (u) => u.role === 'technicien' && u.categorie === formData.categorie
  ) ?? [];

  const experts = users?.filter((u) => u.role === 'expert') ?? [];

  const handleChange = (field: keyof WorkOrder, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  /*const handleTechnicienToggle = (id: number) => {
    const toastId = `technicien-${id}`; // ID unique par technicien

    setFormData(prev => {
      const current = Array.isArray(prev.techniciens) ? prev.techniciens : [];
      //let updated;

      if (current.includes(id)) {
        //updated = current.filter(t => t !== id);
        // ✅ retirer le technicien
        toast.dismiss(toastId);
        toast.info(`Technicien #${id} retiré du bon de travail`, { id: toastId });
        return { ...prev, techniciens: current.filter(t => t !== id) };
      } else {
        //updated = [...current, id];
        // ✅ ajouter le technicien
        toast.dismiss();
        toast.success(`Technicien #${id} ajouté au bon de travail`);
        return { ...prev, techniciens: [...current, id] };
        }
        //return { ...prev, techniciens: updated };
    });
  };
*/
/*

const handleTechnicienToggle = (id: number) => {
  const toastId = `technicien-${id}`; // ID unique par technicien

  setFormData(prev => {
    const current = Array.isArray(prev.techniciens) ? prev.techniciens : [];

    if (current.includes(id)) {
      // Retirer le technicien
      //toast.dismiss(toastId); // ferme le toast existant
      if (!toast.isActive(toastId)) {
      toast.info(`Technicien #${id} retiré du bon de travail`, { id: toastId } as any);
      }
      return { ...prev, techniciens: current.filter(t => t !== id) };
    } else {
      // Ajouter le technicien
      //toast.dismiss(toastId);
      if (!toast.isActive(toastId)) {
      toast.success(`Technicien #${id} ajouté au bon de travail`, { id: toastId } as any);
      }
      return { ...prev, techniciens: [...current, id] };
    }
  });
};
*/

const handleTechnicienToggle = (id: number) => {
  /*setFormData(prev => {
    const current = Array.isArray(prev.techniciens) ? prev.techniciens : [];
    let updated;
    let action: "add" | "remove";
    
    if (current.includes(id)) {
      updated = current.filter(t => t !== id);
      action = "remove";
    } else {
      updated = [...current, id];
      action = "add";
    }

    // Retourne uniquement le nouvel état
    return { ...prev, techniciens: updated };
  });*/

  setFormData(prev => {
  const current = Array.isArray(prev.techniciens) ? prev.techniciens : [];

  const updated = current.includes(id)
    ? current.filter(t => t !== id)
    : [...current, id];

  // suite du traitement...

  return {
    ...prev,
    techniciens: updated,
  };
});

  // 👉 Affiche le toast en dehors du setter
  const isAlreadyAssigned = (formData.techniciens as number[] | undefined)?.includes(id);

  if (isAlreadyAssigned) {
    toast.info(`Technicien #${id} retiré du bon de travail`);
  } else {
    toast.success(`Technicien #${id} ajouté au bon de travail`);
  }
};


const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();

  // ✅ transformation en payload normalisé
  const payload = normalizeWorkOrderPayload(formData);

  // ✅ validation frontend
  if (!payload.machine) {
    toast.error("Veuillez sélectionner une machine.");
    return;
  }
  if (!payload.categorie) {
    toast.error("Veuillez sélectionner une catégorie.");
    return;
  }
  if (!payload.expert) {
    toast.error("Veuillez sélectionner un expert.");
    return;
  }
  if (!payload.type) {
    toast.error("Veuillez sélectionner un type de maintenance.");
    return;
  }
  if (!payload.priorite) {
    toast.error("Veuillez sélectionner une priorité.");
    return;
  }

  try {
    //await onSubmit(payload);
    const created = await onSubmit(payload);
    // ✅ toast avec lien vers le workorder créé
    toast.success("Bon de travail enregistré avec succès !");
    if (onCreated) onCreated(created.id); // ✅ notifier le parent
    if (onClose) onClose();              // ✅ fermer le pop-up
      // pas ce navigation ici
  } catch (err: any) {
    toast.error("Erreur lors de l'enregistrement du bon de travail.");
    console.error(err);
  }
};


  return (
    <form
      onSubmit={handleSubmit}
      className="space-y-4 bg-white p-6 rounded shadow"
    >
            
      {/* Machine */}
      <div>
        <label className="block text-sm font-medium text-gray-700">Machine</label>
        <select
          value={formData.machine ?? ""}
          onChange={e => handleChange("machine", Number(e.target.value))}
          required
          className="mt-1 block w-full border-gray-300 rounded-md shadow-sm"
        >
          <option value="">-- Sélectionner une machine --</option>
          {machines?.map((m : Machine) => (
            <option key={m.id} value={m.id}>
              {m.nom} – {m.localisation ?? "N/A"} ({m.etat})
            </option>
          ))}
        </select>
      </div>

      {/* Signalement */}
      <div>
        <label className="block text-sm font-medium text-gray-700">Signalement</label>
        <select
          value={formData.signalement ?? ""}
          onChange={e => handleChange("signalement", Number(e.target.value))}
          className="mt-1 block w-full border-gray-300 rounded-md shadow-sm"
        >
          <option value="">-- Aucun signalement --</option>
          {signalements?.map(s => (
            <option key={s.id} value={s.id}>
              #{s.id} - {s.machine_detail?.nom ?? `Machine #${s.machine}`} - {s.statut}
              (créé par {s.cree_par_detail?.username ?? `User #${s.cree_par}`})
            </option>
          ))}
        </select>
      </div>


      {/* Catégorie */}
      <div>
        <label className="block text-sm font-medium text-gray-700">Catégorie</label>
        <select
          value={formData.categorie ?? ''}
          onChange={e => handleChange('categorie', Number(e.target.value))}
          className="mt-1 block w-full border-gray-300 rounded-md shadow-sm"
        >
          <option value="">-- Sélectionner une catégorie --</option>
          {categories?.map(cat => (
            <option key={cat.id} value={cat.id}>
              {cat.nom}
            </option>
          ))}
        </select>
      </div>

      {/* Liste des techniciens (multi-sélection) */}
      <div>
        <label className="block text-sm font-medium text-gray-700">Techniciens</label>
        <div className="space-y-2 max-h-40 overflow-y-auto border rounded-md p-2">
          {techniciens.map(t => (
            <label key={t.id} className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={(formData.techniciens as number[] | undefined)?.includes(t.id) ?? false}
                onChange={() => handleTechnicienToggle(t.id)}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span>{t.username} ({t.categorie_detail?.nom})</span>
            </label>
          ))}
        </div>
      </div>

      {/* Expert */}
      <div>
        <label className="block text-sm font-medium text-gray-700">Expert</label>
        {user?.role === 'expert' ? (
          <input
            type="text"
            value={user.username}
            disabled
            className="mt-1 block w-full border-gray-300 rounded-md shadow-sm bg-gray-100"
          />
        ) : (
          <select
            value={formData.expert ?? ''}
            onChange={e => handleChange('expert', Number(e.target.value))}
            className="mt-1 block w-full border-gray-300 rounded-md shadow-sm"
            required
          >
            <option value="">-- Sélectionner un expert --</option>
            {experts.map(e => (
              <option key={e.id} value={e.id}>
                {e.username}
              </option>
            ))}
          </select>
        )}
      </div>

      
      {/* Type */}
    
<div>
  <label className="block text-sm font-medium text-gray-700">Type</label>
  <select
    value={formData.type ?? ""}
    onChange={e => handleChange("type", e.target.value)}
    required
    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm"
  >
    <option value="">-- Sélectionner un type --</option>
    <option value="corrective">Corrective</option>
    <option value="preventive">Préventive</option>
    <option value="predictive">Prédictive</option>
  </select>
</div>

{/* Priorité */}
<div>
  <label className="block text-sm font-medium text-gray-700">Priorité</label>
  <select
    value={formData.priorite ?? ''}
    onChange={e => handleChange('priorite', e.target.value)}
    required
    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm"
  >
    <option value="">-- Sélectionner une priorité --</option>
    <option value="low">Basse</option>
    <option value="medium">Moyenne</option>
    <option value="high">Haute</option>
  </select>
</div>

{/* Description */}
<div>
  <label className="block text-sm font-medium text-gray-700">Description</label>
  <textarea
    value={formData.description ?? ''}
    onChange={e => handleChange('description', e.target.value)}
    required
    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm"
    placeholder="Décrire le problème ou la demande"
  />
</div>

      {/* Bouton Submit */}
      <div className="flex justify-end space-x-2">
        {onClose && (
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 rounded bg-gray-300 text-gray-800"
          >
            Annuler
          </button>
        )}
        <button
          type="submit"
          disabled={isLoading}
          className={`px-4 py-2 rounded text-white ${isLoading ? 'bg-gray-400' : 'bg-indigo-600 hover:bg-indigo-700'}`}
        >
          {isLoading ? 'Enregistrement...' : 'Enregistrer'}
        </button>
      </div>
    </form>
  );
};
