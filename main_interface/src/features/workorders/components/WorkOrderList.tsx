// src/features/workorders/components/WorkOrderList.tsx
import { useState } from 'react';
import { useWorkOrders, useDeleteWorkOrder, useUpdateWorkOrder } from '../hooks/useWorkOrders';
import type { WorkOrder, WorkOrderWithDetails } from '../types';
import { WorkOrderDetailModal } from './WorkOrderDetailModal';
import { WorkOrderForm } from './WorkOrderForm';
import { useAuthStore } from '../../../store/authStore';
import { toast } from 'react-hot-toast';

export const WorkOrderList = () => {
  const [currentPage, setCurrentPage] = useState(1); // ✅ pagination
  const { data, isLoading, error } = useWorkOrders({ page: currentPage });
  const workorders = data?.results ?? [];
  const totalCount = data?.count ?? 0;

  const deleteWorkOrder = useDeleteWorkOrder();
  const updateWorkOrder = useUpdateWorkOrder();
  const [selectedWorkOrder, setSelectedWorkOrder] = useState<WorkOrderWithDetails | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const { user } = useAuthStore();

  if (isLoading) return <div className="p-4 text-gray-500">Chargement...</div>;
  if (error) return <div className="p-4 text-red-500">Erreur : {error.message}</div>;

  const handleDelete = (id: number, e: React.MouseEvent) => {
    e.stopPropagation();
    if (confirm('Supprimer ce bon de travail ?')) {
      deleteWorkOrder.mutate(id, {
        onSuccess: () => toast.success('Bon de travail supprimé'),
        onError: () => toast.error('Erreur lors de la suppression'),
      });
    }
  };

  const handleEdit = (wo: WorkOrderWithDetails, e: React.MouseEvent) => {
    e.stopPropagation();
    setSelectedWorkOrder(wo);
    setIsEditModalOpen(true);
  };

  const handleRowClick = (wo: WorkOrderWithDetails) => {
    setSelectedWorkOrder(wo);
    setIsModalOpen(true);
  };

  const handleUpdate = async (data: Partial<WorkOrder>) => {
    if (!selectedWorkOrder) throw new Error("Pas de WorkOrder sélectionné");
    try {
      const updated = await updateWorkOrder.mutateAsync({ id: selectedWorkOrder.id, data });
      toast.success('Bon de travail mis à jour');
      setIsEditModalOpen(false);
      return updated; // ✅ retourne WorkOrderWithDetails
    } catch {
      toast.error('Erreur lors de la mise à jour');
      throw new Error("Update failed");
    }
  };

  const getStatusColor = (etat: string) => {
    switch (etat) {
      case 'clos': return 'bg-gray-300 text-gray-800';
      case 'en_cours': return 'bg-blue-100 text-blue-800';
      case 'valide': return 'bg-purple-100 text-purple-800';
      case 'en_attente': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  //const isAdmin = user?.role === 'admin' || user?.role === 'expert';
  const isAdmin = ['admin', 'expert'].includes(user?.role ?? '');

  return (
    <>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border border-gray-200">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Machine</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Priorité</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">État</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Technicien</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {workorders.map((wo) => (
              <tr
                key={wo.id}
                onClick={() => handleRowClick(wo)}
                className="hover:bg-gray-50 cursor-pointer"
              >
                <td className="px-6 py-4 text-sm text-gray-900">#{wo.id}</td>
                <td className="px-6 py-4 text-sm text-gray-900">
                  {wo.machine_detail?.nom || wo.machine}
                </td>
                <td className="px-6 py-4 text-sm text-gray-500">{wo.type}</td>
                <td className="px-6 py-4 text-sm text-gray-500">{wo.priorite}</td>
                <td className="px-6 py-4">
                  <span className={`px-2 inline-flex text-xs font-semibold rounded-full ${getStatusColor(wo.etat)}`}>
                    {wo.etat}
                  </span>
                </td>
                <td className="px-6 py-4 text-sm text-gray-500">
                  {wo.techniciens_detail && wo.techniciens_detail.length > 0
                    ? wo.techniciens_detail
                        .map(t => `${t.username}${t.categorie_detail ? ` (${t.categorie_detail.nom})` : ''}`)
                        .join(', ')
                    : '-'}
                </td>
                <td className="px-6 py-4 text-sm font-medium">
                  {isAdmin && (
                    <button
                      onClick={(e) => handleEdit(wo, e)}
                      className="text-blue-600 hover:text-blue-900 mr-3"
                    >
                      Modifier
                    </button>
                  )}
                  <button
                    onClick={(e) => handleDelete(wo.id, e)}
                    className="text-red-600 hover:text-red-900"
                  >
                    Supprimer
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* ✅ Pagination */}
      <div className="flex justify-between items-center px-4 py-2 text-sm text-gray-600">
        <button
          disabled={!data?.previous}
          onClick={() => setCurrentPage((p) => Math.max(p - 1, 1))}
          className={`px-2 py-1 rounded ${data?.previous ? "text-blue-600 hover:bg-gray-100" : "text-gray-400 cursor-not-allowed"}`}
        >
          Précédent
        </button>
        <span>
          Page {currentPage} / {Math.ceil(totalCount / 10)}
        </span>
        <button
          disabled={!data?.next}
          onClick={() => setCurrentPage((p) => p + 1)}
          className={`px-2 py-1 rounded ${data?.next ? "text-blue-600 hover:bg-gray-100" : "text-gray-400 cursor-not-allowed"}`}
        >
          Suivant
        </button>
      </div>

      <WorkOrderDetailModal
        workorder={selectedWorkOrder}
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />

      {isEditModalOpen && selectedWorkOrder && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <div className="absolute inset-0 bg-gray-500 opacity-75" onClick={() => setIsEditModalOpen(false)}></div>
          <div className="bg-white rounded-lg shadow-xl max-w-lg w-full p-6 relative z-10">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              Modifier le bon de travail #{selectedWorkOrder.id}
            </h3>
            <WorkOrderForm
              initialData={selectedWorkOrder}
              onSubmit={handleUpdate}
              isLoading={updateWorkOrder.isPending}
            />
          </div>
        </div>
      )}
    </>
  );
};
