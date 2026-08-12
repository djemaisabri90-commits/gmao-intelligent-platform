// src/features/workorders/pages/WorkOrdersPage.tsx

import { useState } from 'react';
import { WorkOrderList } from '../components/WorkOrderList';
import { WorkOrderForm } from '../components/WorkOrderForm';
import { useCreateWorkOrder } from '../hooks/useWorkOrders';
import type { WorkOrder } from '../types';
import { toast } from 'react-hot-toast';

export const WorkOrdersPage = () => {
  const [showForm, setShowForm] = useState(false);
  const createWorkOrder = useCreateWorkOrder();

  const handleCreate = async (data: Partial<WorkOrder>) => {
  try {
    const result = await createWorkOrder.mutateAsync(data); // ✅ retourne WorkOrderWithDetails
    setShowForm(false);
    return result; // ✅ important pour satisfaire WorkOrderFormProps
  } catch (err) {
    toast.error("Erreur lors de la création du bon de travail");
    console.error(err);
    throw err; // ✅ relance l’erreur pour que WorkOrderForm puisse l’attraper
  }
};

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Bons de travail</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md"
        >
          {showForm ? 'Annuler' : 'Créer un bon de travail'}
        </button>
      </div>

      {showForm && (
        <div className="mb-8 p-4 border rounded-md bg-gray-50">
          <WorkOrderForm onSubmit={handleCreate} isLoading={createWorkOrder.isPending} />
        </div>
      )}

      <WorkOrderList />
    </div>
  );
};
