// src/features/signalements/components/SignalementList.tsx
import { useAuth } from "@/features/auth/hooks/useAuth";

import { useState } from "react";
import { useSignalements, useDeleteSignalement, useChangeSignalementStatut } from "../hooks/useSignalements";
import type { SignalementWithDetails, SignalementStatus } from "../types";
import { WorkOrderForm } from "../../workorders/components/WorkOrderForm"; // ✅ importer ton formulaire
import { useCreateWorkOrder } from "@/features/workorders/hooks/useWorkOrders";

export const SignalementList = () => {
  const { data: signalements, isLoading, error } = useSignalements();
  const deleteSignalement = useDeleteSignalement();
  const changeStatut = useChangeSignalementStatut();
  const createWorkOrder = useCreateWorkOrder();

  const [selectedSignalement, setSelectedSignalement] = useState<SignalementWithDetails | null>(null);

  const { user } = useAuth(); // ✅ récupère le rôle de l’utilisateur

  if (isLoading) return <div className="p-4 text-gray-500">Chargement...</div>;
  if (error) return <div className="p-4 text-red-500">Erreur : {error.message}</div>;

  const handleDelete = (id: number) => {
    if (confirm("Supprimer ce signalement ?")) {
      deleteSignalement.mutate(id);
    }
  };

  const handleTransform = (signalement: SignalementWithDetails) => {
    setSelectedSignalement(signalement);
  };

  const handleWorkOrderCreated = (workorderId: number) => {
    if (selectedSignalement) {
      changeStatut.mutate({ id: selectedSignalement.id, statut: "traite" });
      setSelectedSignalement(null); // fermer le pop-up
      console.log("WorkOrder créé avec ID:", workorderId);
    // ou toast.success(`WorkOrder #${workorderId}
    }
  };

  const getStatusColor = (statut: SignalementStatus) => {
    switch (statut) {
      case "nouveau": return "bg-blue-100 text-blue-800";
      case "traite": return "bg-green-100 text-green-800";
      default: return "bg-gray-100 text-gray-800";
    }
  };

  const getStatusLabel = (statut: SignalementStatus) => {
    switch (statut) {
      case "nouveau": return "Nouveau";
      case "traite": return "Traité";
      default: return statut;
    }
  };

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full bg-white border border-gray-200">
        <thead className="bg-gray-100">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Machine</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Description</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Source</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Statut</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Créé par</th>
            {(user?.role === "admin" || user?.role === "expert") && (
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            )}
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {signalements?.map((s) => (
            <tr key={s.id} className="hover:bg-gray-50">
              <td className="px-6 py-4 text-sm text-gray-900">#{s.id}</td>
              <td className="px-6 py-4 text-sm text-gray-900">{s.machine_detail?.nom || s.machine}</td>
              <td className="px-6 py-4 text-sm text-gray-500 max-w-md truncate">{s.description}</td>
              <td className="px-6 py-4 text-sm text-gray-500">{s.source}</td>
              <td className="px-6 py-4">
                <span className={`px-2 inline-flex text-xs font-semibold rounded-full ${getStatusColor(s.statut)}`}>
                  {getStatusLabel(s.statut)}
                </span>
              </td>
              <td className="px-6 py-4 text-sm text-gray-500">{s.cree_par_detail?.username || s.cree_par}</td>
              {(user?.role === "admin" || user?.role === "expert") && (
                <td className="px-6 py-4 text-sm font-medium space-x-4">
                
                <button onClick={() => handleDelete(s.id)} className="text-red-600 hover:text-red-900">
                  Supprimer
                </button>
                
                {s.statut === "nouveau" && (
                  <button onClick={() => handleTransform(s)} className="text-blue-600 hover:text-blue-900">
                    Transformer en WorkOrder
                  </button>
                )}
              </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>

      {/* ✅ Pop-up WorkOrderForm */}
      {selectedSignalement && (
        <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50">
    <div className="bg-white p-6 rounded shadow-lg w-[600px]">
      
        <WorkOrderForm
          signalement={selectedSignalement}
          onSubmit={async (payload) => {
            const created = await createWorkOrder.mutateAsync(payload);
            return created; // WorkOrderWithDetails
          }}
          onClose={() => setSelectedSignalement(null)}
          onCreated={handleWorkOrderCreated}
          isLoading={createWorkOrder.isPending}
        />
        </div>
  </div>
      )}


    </div>

  );
};
