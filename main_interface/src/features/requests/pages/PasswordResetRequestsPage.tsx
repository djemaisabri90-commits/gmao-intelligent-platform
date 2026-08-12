import { ResetCredentialsModal } from "../components/ResetCredentialsModal";
import { usePasswordResetRequests, useProcessPasswordResetRequest } from "../hooks/usePasswordResetRequests";
import { useState } from "react";

interface ResetCredentials {
  id: number;
  username: string;
  temporaryPassword: string;
  activationToken: string;
}

export const PasswordResetRequestsPage = () => {
  const { data: requests, isLoading, error } = usePasswordResetRequests();
  const processRequest = useProcessPasswordResetRequest();

  const [showModal, setShowModal] = useState(false);

  const [credentials, setCredentials] = useState<ResetCredentials>({
    id: 0,
    username: "",
    temporaryPassword: "",
    activationToken: "",
  });



  if (isLoading) {
    return (
      <div className="p-6 text-gray-500 text-lg">
        Chargement des demandes...
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 text-red-600 text-lg">
        Erreur lors du chargement des demandes.
      </div>
    );
  }
  


  return (
    <>
    <ResetCredentialsModal

      isOpen={showModal}
      onClose={() => setShowModal(false)}
      userId={credentials.id}
      username={credentials.username}
      temporaryPassword={credentials.temporaryPassword}
      activationToken={credentials.activationToken}
      title="Fiche de réinitialisation des accès"
      subtitle="Communiquez les nouveaux identifiants à l'employé."
    />
    <div className="max-w-7xl mx-auto px-6 py-8">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">
          Demandes de réinitialisation
        </h1>
        <p className="text-base text-gray-600 mt-2">
          Liste des demandes de mot de passe oublié soumises par les utilisateurs.
        </p>
      </div>

      {/* Tableau */}
      <div className="bg-white border rounded-lg shadow-md overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700 uppercase">ID</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700 uppercase">Utilisateur</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700 uppercase">Date</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700 uppercase">Statut</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700 uppercase">Actions</th>
            </tr>
          </thead>

          <tbody className="divide-y divide-gray-200">
            {requests?.length === 0 && (
              <tr>
                <td colSpan={5} className="text-center py-8 text-gray-500 text-lg">
                  Aucune demande trouvée.
                </td>
              </tr>
            )}

            {requests?.map((request) => (
              <tr key={request.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 text-base text-gray-900">{request.id}</td>
                <td className="px-6 py-4 text-base font-medium text-gray-900">{request.username}</td>
                <td className="px-6 py-4 text-base text-gray-700">
                  {new Date(request.created_at).toLocaleString()}
                </td>
                <td className="px-6 py-4 text-base">
                  {request.status === "pending" && (
                    <span className="px-2 py-1 rounded bg-yellow-100 text-yellow-800 text-sm font-semibold">
                      En attente
                    </span>
                  )}
                  {request.status === "resolved" && (
                    <span className="px-2 py-1 rounded bg-green-100 text-green-800 text-sm font-semibold">
                      Traitée
                    </span>
                  )}
                  {request.status === "rejected" && (
                    <span className="px-2 py-1 rounded bg-red-100 text-red-800 text-sm font-semibold">
                      Rejetée
                    </span>
                  )}
                </td>
                <td className="px-6 py-4">
                  <button
                    disabled={request.status !== "pending"}
                    onClick={() => {
                      processRequest.mutate(request.id, {
                        onSuccess: (data) => {
                          /*alert(
                            `Utilisateur : ${data.username}\n\n` +
                            `Mot de passe : ${data.temporary_password}\n\n` +
                            `Clé : ${data.activation_token}`
                          );*/
                          setCredentials({
                              id: data.id,
                              username: data.username,
                              temporaryPassword: data.temporary_password,
                              activationToken: data.activation_token,
                          });                          
                          setShowModal(true)
                        },
                      });
                    }}
                    className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white px-4 py-2 rounded text-sm font-medium"
                  >
                    Traiter
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  
</>
);
};
