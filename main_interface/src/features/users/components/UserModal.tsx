// src/features/users/components/UserModal.tsx
import { UserForm } from "./UserForm";
import { ForcePasswordChange } from "./ForcePasswordChange";
import type { User } from "../types";

interface UserModalProps {
  action: "edit" | "delete" | "changePassword";
  user: User;
  onClose: () => void;
  onSubmit: (data: Partial<User>) => void;
}

export const UserModal = ({ action, user, onClose, onSubmit }: UserModalProps) => {
  return (
    <div className="fixed inset-0 flex items-center justify-center z-50">
      {/* Overlay avec fade */}
      <div
        className="absolute inset-0 bg-black bg-opacity-50 transition-opacity duration-300"
        onClick={onClose}
      />

      {/* Contenu avec animation */}
      <div className="relative bg-white rounded-lg shadow-lg p-6 w-full max-w-lg transform transition-all duration-300 scale-95 opacity-0 animate-modal-enter">
        {action === "edit" && (
          <>
            <h2 className="text-lg font-bold mb-4">Modifier l’utilisateur</h2>
            <UserForm initialData={user} onSubmit={onSubmit} />
          </>
        )}

        {action === "delete" && (
          <>
            <h2 className="text-lg font-bold mb-4">Supprimer l’utilisateur</h2>
            <p>Voulez-vous vraiment supprimer <strong>{user.username}</strong> ?</p>
            <div className="mt-4 flex justify-end gap-2">
              <button
                onClick={onClose}
                className="px-4 py-2 bg-gray-200 rounded-md hover:bg-gray-300"
              >
                Annuler
              </button>
              <button
                onClick={() => onSubmit({ id: user.id })}
                className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
              >
                Supprimer
              </button>
            </div>
          </>
        )}

        {action === "changePassword" && (
          <>
            <h2 className="text-lg font-bold mb-4">Réinitialiser le mot de passe</h2>
            <ForcePasswordChange userId={user.id} onSuccess={onClose} />
          </>
        )}

        {/*<div className="mt-4 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-200 rounded-md hover:bg-gray-300"
          >
            Fermer
          </button>
        </div>
        */}
      </div>
    </div>
  );
};
