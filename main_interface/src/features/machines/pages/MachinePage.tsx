// src/features/machines/pages/MachinesPage.tsx
import { useState } from "react";
import { MachineList } from "../components/MachineList";
import { MachineForm } from "../components/MachineForm";
import { useCreateMachine, useUpdateMachine } from "../hooks/useMachines";
import type { Machine } from "../types";
import toast from "react-hot-toast";

export const MachinesPage = () => {
  const [editingMachine, setEditingMachine] = useState<Machine | null>(null);
  const [showForm, setShowForm] = useState(false);

  const createMachine = useCreateMachine();
  const updateMachine = useUpdateMachine();

  const handleCreate = (data: Omit<Machine, "id" | "etat">) => {
    createMachine.mutate(data, {
      onSuccess: () => {
        toast.success("Machine créée avec succès ✅");
        setShowForm(false);
      },
      onError: (error: any) => {
        toast.error(`Erreur lors de la création : ${error.message}`);
      },
    });
  };

  const handleUpdate = (data: Partial<Machine>) => {
    if (!editingMachine) return;
    updateMachine.mutate(
      { id: editingMachine.id, data },
      {
        onSuccess: () => {
          toast.success("Machine mise à jour avec succès ✨");
          setEditingMachine(null);
          setShowForm(false);
        },
        onError: (error: any) => {
          toast.error(`Erreur lors de la mise à jour : ${error.message}`);
        },
      }
    );
  };

  const toggleForm = () => {
    if (editingMachine) {
      setEditingMachine(null);
    }
    setShowForm(!showForm);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Machines</h1>
        <button
          onClick={toggleForm}
          className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md"
        >
          {showForm ? "Annuler" : "Ajouter une machine"}
        </button>
      </div>

      {showForm && (
        <div
          className={`mb-8 p-4 border rounded-md bg-gray-50 transform transition-all duration-500 ease-in-out 
          ${showForm ? "opacity-100 translate-y-0" : "opacity-0 -translate-y-4"}`}
        >
          <MachineForm
            initialData={editingMachine || {}}
            onCreate={handleCreate}
            onUpdate={handleUpdate}
            isLoading={
              editingMachine ? updateMachine.isPending : createMachine.isPending
            }
            isEdit={!!editingMachine}
          />
          {/*<button
            onClick={() => {
              setEditingMachine(null);
              setShowForm(false);
              toast("Édition annulée ❌", { icon: "🛑" }); // ✅ confirmation toast
            }}
            className="mt-4 bg-gray-300 hover:bg-gray-400 text-gray-800 font-medium py-2 px-4 rounded-md"
          >
            Annuler
          </button>*/}
        </div>
      )}

      <MachineList onEdit={(machine) => {
        setEditingMachine(machine);
        setShowForm(true);
        toast(`Édition de la machine "${machine.nom}" ouverte ✏️`, {
          icon: "🔧",
        });
      }} />
    </div>
  );
};
