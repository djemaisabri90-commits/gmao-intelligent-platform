import { useMachines, useDeleteMachine } from "../hooks/useMachines";
import type { Machine } from "../types";
import toast from "react-hot-toast";
import { useState } from "react";

interface MachineListProps {
  onEdit: (machine: Machine) => void;
}

export const MachineList = ({ onEdit }: MachineListProps) => {
  
  
  const { data: machines, isLoading, error } = useMachines();
  const deleteMachine = useDeleteMachine();
  const [deletingId, setDeletingId] = useState<number | null>(null);

  if (isLoading) return <div className="p-4 text-gray-500">Chargement...</div>;
  if (error) return <div className="p-4 text-red-500">Erreur : {error.message}</div>;

  const handleDelete = (id: number) => {
    if (confirm("Supprimer cette machine ?")) {
      setDeletingId(id); // ✅ active animation
      setTimeout(() => {
        deleteMachine.mutate(id, {
          onSuccess: () => {
            toast.success("Machine supprimée avec succès 🗑️");
            setDeletingId(null);
          },
          onError: (error: any) => {
            toast.error(`Erreur lors de la suppression : ${error.message}`);
            setDeletingId(null);
          },
        });
      }, 500); // délai pour laisser l’animation jouer
    }
  };

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full bg-white border border-gray-200">
        <thead className="bg-gray-100">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Nom
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              État
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Localisation
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {machines?.map((machine: Machine) => (
            <tr
              key={machine.id}
              className={`hover:bg-gray-50 transition-all duration-500 ease-in-out transform
                ${deletingId === machine.id ? "bg-red-100 opacity-0 scale-y-0" : "opacity-100 scale-y-100"}`}
            >
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {machine.nom}
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                {/* badge état */}
                {machine.etat}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {machine.localisation || "-"}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                <button
                  onClick={() => onEdit(machine)}
                  className="text-blue-600 hover:text-blue-900 transition-colors duration-300"
                >
                  Modifier
                </button>
                <button
                  onClick={() => handleDelete(machine.id)}
                  className="text-red-600 hover:text-red-900 ml-2 transition-colors duration-300"
                >
                  Supprimer
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
