import { useState } from "react";
import { UserList } from "../components/UserList";
import { UserForm } from "../components/UserForm";
//import { ForcePasswordChange } from "../components/ForcePasswordChange";
import { ExportActivationPDF } from "../components/ExportActivationPDF"; 
import { useCreateUser } from "../hooks/useUsers";
import type { User } from "../types";
import toast from "react-hot-toast";
import { ResetCredentialsModal } from "@/features/requests/components/ResetCredentialsModal";

export const UsersPage = () => {
  const [showForm, setShowForm] = useState(false);
  //const [forcePasswordUser, setForcePasswordUser] = useState<User | null>(null);
  const createUser = useCreateUser();
  
  // 🎯 État local isolé pour conserver le mot de passe en clair sans écrasement
  const [createdUserInfo, setCreatedUserInfo] = useState<any | null>(null);

  // pdf
  const [showCredentialsModal, setShowCredentialsModal] = useState(false);

  const handleCreate = (data: Partial<User>) => {
    createUser.mutate(data, {
      onSuccess: (response: any) => {
        console.log("RESPONSE =", response);

        toast.success("Utilisateur créé avec succès !");
        setShowForm(false);
        
        // Extraction sécurisée du payload brut de l'utilisateur
        const userData = response?.data ? response.data : response;


        
        setCreatedUserInfo(userData);
        
        /*if (userData.must_change_password) {
          setForcePasswordUser(userData);
        }*/
      },
      onError: () => {
        toast.error("Erreur lors de la création de l'utilisateur");
      },
    });
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      
      {/* 1. Header & Barre d'actions */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6 pb-4 border-b border-gray-100">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Gestion des utilisateurs</h1>
          <p className="text-xs text-gray-500 mt-1">
            Configurez les profils d'usine et gérez les accès hors-ligne.
          </p>
        </div>

        {/* Barre d'outils unifiée */}
        <div className="flex flex-wrap items-center gap-3 w-full md:w-auto">
          <ExportActivationPDF /> 
          <button
            onClick={() => setShowForm(!showForm)}
            className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition text-sm shadow-sm"
          >
            {showForm ? "Annuler" : "Nouvel utilisateur"}
          </button>
        </div>
      </div>

      {/* 🎯 2. Emplacement corrigé : L'affichage Flash se situe sous le header pour ne pas casser le design flexbox */}
      {createdUserInfo && (
      <div className="mb-6 p-5 bg-green-50 border border-green-200 rounded-lg shadow-sm flex justify-center items-center animate-modal-entrance">
  

    <div className="space-y-1">
      <h4 className="text-sm font-semibold text-green-800">
        Compte créé avec succès !
      </h4>

      <p className="text-xs text-green-700">
        Les identifiants temporaires ont été générés.
      </p>

      <div className="mt-3 flex gap-2">

        <button
          onClick={() => setShowCredentialsModal(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded text-xs"
        >
          Voir la fiche d'activation
        </button>

      </div>
    </div>

    <button
      onClick={() => {
        setCreatedUserInfo(null);
        createUser.reset();
      }}
      className="text-xs bg-green-200 hover:bg-green-300 text-green-800 px-2.5 py-1.5 rounded transition font-medium ml-4"
    >
      Masquer
    </button>

  </div>
)}

{createdUserInfo && (
  <ResetCredentialsModal
    isOpen={showCredentialsModal}
    onClose={() => setShowCredentialsModal(false)}

    userId={createdUserInfo.id}

    username={createdUserInfo.username}

    temporaryPassword={
      createdUserInfo.temporary_password || ""
    }

    activationToken={
      createdUserInfo.activation_token || ""
    }
    title="Fiche d'activation initiale"
    subtitle="Remettez cette fiche d'activation au nouvel employé."
  />
)}

      {/* Formulaire de création */}
      {showForm && (
        <div className="mb-8 p-6 border rounded-md bg-gray-50 shadow-sm transition animate-modal-entrance">
          <UserForm onSubmit={handleCreate} isLoading={createUser.isPending} />
        </div>
      )}

      {/* Force password change modal 
      {forcePasswordUser && (
        <div className="mb-8 p-6 border rounded-md bg-white shadow-lg border-yellow-200 animate-modern-alert">
          <ForcePasswordChange
            userId={forcePasswordUser.id}
            onSuccess={() => {
              toast.success("Mot de passe changé avec succès !");
              setForcePasswordUser(null);
            }}
          />
        </div>
      )}
      */}

      {/* Liste globale des utilisateurs de la GMAO */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-100">
        <UserList />
      </div>
    </div>
  );
};
