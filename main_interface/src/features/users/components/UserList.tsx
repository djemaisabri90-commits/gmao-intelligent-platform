import { useState } from "react";
import { useUsers, useDeleteUser, useUpdateUser } from "../hooks/useUsers";
import type { User } from "../types";
import { UserModal } from "./UserModal";
import toast from "react-hot-toast";

export const UserList = () => {
  const { data: users, isLoading, error } = useUsers();
  const deleteUser = useDeleteUser();
  const updateUser = useUpdateUser();

  const [modalAction, setModalAction] = useState<"edit" | "delete" | "changePassword" | null>(null);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);

  if (isLoading) return <div className="p-4 text-gray-500">Chargement...</div>;
  if (error) return <div className="p-4 text-red-500">Erreur : {(error as Error).message}</div>;

  const sortedUsers = users ? [...users].sort((a, b) => b.id - a.id) : [];

  const handleDelete = (id: number) => {
    deleteUser.mutate(id, {
      onSuccess: () => toast.success("Utilisateur supprimé"),
      onError: () => toast.error("Erreur lors de la suppression"),
    });
    setModalAction(null);
    setSelectedUser(null);
  };

  const handleUpdate = (data: Partial<User>) => {
    if (!selectedUser) return;
    updateUser.mutate(
      { id: selectedUser.id, data },
      {
        onSuccess: () => {
          toast.success("Utilisateur mis à jour !");
          setModalAction(null);
          setSelectedUser(null);
        },
        onError: () => toast.error("Erreur lors de la mise à jour"),
      }
    );
  };

  return (
    <div className="overflow-x-auto">
      {/* Modal global */}
      {modalAction && selectedUser && (
        <UserModal
          action={modalAction}
          user={selectedUser}
          onClose={() => {
            setModalAction(null);
            setSelectedUser(null);
          }}
          onSubmit={modalAction === "delete" ? () => handleDelete(selectedUser.id) : handleUpdate}
        />
      )}

      {/* Table */}
      <table className="min-w-full bg-white border border-gray-200">
        <thead className="bg-gray-100">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nom d'utilisateur</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Rôle</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {sortedUsers.map((user: User) => (
            <tr
              key={user.id}
              className="hover:bg-gray-50 cursor-pointer"
              onClick={() => {
                setSelectedUser(user);
                setModalAction("edit");
              }}
            >
              <td className="px-6 py-4 text-sm text-gray-900">{user.id}</td>
              <td className="px-6 py-4 text-sm text-gray-900">{user.username}</td>
              <td className="px-6 py-4 text-sm text-gray-500">{user.email || "-"}</td>
              <td className="px-6 py-4 text-sm text-gray-500">{user.role}</td>
              <td className="px-6 py-4 text-sm font-medium flex gap-4">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedUser(user);
                    setModalAction("delete");
                  }}
                  className="text-red-600 hover:text-red-900"
                >
                  Supprimer
                </button>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedUser(user);
                    setModalAction("changePassword");
                  }}
                  className="text-yellow-600 hover:text-yellow-900"
                >
                  Réinitialiser mot de passe
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
