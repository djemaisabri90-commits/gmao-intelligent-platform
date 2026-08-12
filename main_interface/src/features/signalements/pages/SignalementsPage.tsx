import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { SignalementList } from "../components/SignalementList";
import { SignalementForm } from "../components/SignalementForm";
import { useCreateSignalement } from "../hooks/useSignalements";
import type { Signalement } from "../types";
import toast, { Toaster } from "react-hot-toast";
import { useAuthStore } from "@/store/authStore";

export const SignalementsPage = () => {
  const [showForm, setShowForm] = useState(false);
  const createSignalement = useCreateSignalement();

  const navigate = useNavigate();

  const { user } = useAuthStore();
  const { logout } = useAuthStore();

  const isOperateur = user?.role === "operateur";

  const canViewList = [
    "admin",
    "expert",
    "technicien",
  ].includes(user?.role || "");

  const handleCreate = (data: Partial<Signalement>) => {
    createSignalement.mutate(data, {
      onSuccess: () => {
        setShowForm(false);
        toast.success("Signalement créé avec succès !");
        // Auto logout opérateur
      if (user?.role === "operateur") {
        setTimeout(() => {
          logout();
          navigate("/login");
        }, 1500);
      }

      },
      onError: () => {
        toast.error("Erreur lors de la création du signalement.");
      },
    });
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <Toaster position="top-right" />

      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">
          Signalements
        </h1>

        {/* Bouton visible seulement pour non-opérateur */}
        {!isOperateur && (
          <button
            onClick={() => setShowForm(!showForm)}
            className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md"
          >
            {showForm ? "Annuler" : "Créer un signalement"}
          </button>
        )}
      </div>

      {/* Formulaire opérateur : toujours visible */}
      {isOperateur && (
        <div className="mb-8 p-4 border rounded-md bg-gray-50">
          <SignalementForm
            onSubmit={handleCreate}
            isLoading={createSignalement.isPending}
          />
        </div>
      )}

      {/* Formulaire autres rôles */}
      {!isOperateur && showForm && (
        <div className="mb-8 p-4 border rounded-md bg-gray-50">
          <SignalementForm
            onSubmit={handleCreate}
            isLoading={createSignalement.isPending}
          />
        </div>
      )}

      {/* Liste visible seulement pour rôles autorisés */}
      {canViewList && <SignalementList />}
    </div>
  );
};