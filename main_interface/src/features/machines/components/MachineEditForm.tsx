// src/features/machines/components/MachineEditForm.tsx
import { MachineForm } from "./MachineForm";
import { useUpdateMachine } from "../hooks/useMachines";
import type { Machine } from "../types";
import toast from "react-hot-toast";

interface MachineEditFormProps {
  machine: Machine;
  onClose: () => void; // pour fermer le formulaire après édition
}

export const MachineEditForm = ({ machine, onClose }: MachineEditFormProps) => {
  const updateMachine = useUpdateMachine();

  const handleUpdate = (data: Partial<Machine>) => {
    updateMachine.mutate(
      { id: machine.id, data },
      {
        onSuccess: () => {
          toast.success("Machine mise à jour avec succès ✨");
          onClose();
        },
        onError: (error: any) => {
          toast.error(`Erreur lors de la mise à jour : ${error.message}`);
        },
      }
    );
  };

  return (
    <div className="p-4 border rounded-md bg-gray-50">
      <h2 className="text-lg font-semibold mb-4">Modifier la machine</h2>
      <MachineForm
        initialData={machine}
        onUpdate={handleUpdate}   // ✅ on utilise onUpdate au lieu de onSubmit
        isLoading={updateMachine.isPending}
        isEdit={true}             // ✅ active le champ "etat"
      />
      
      <button
        onClick={onClose}
        className="mt-4 bg-gray-300 hover:bg-gray-400 text-gray-800 font-medium py-2 px-4 rounded-md"
      >
        Annuler
      </button>
      
    </div>
  );
};
