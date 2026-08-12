import React, { useState } from "react";
import { apiClient } from "../../../api/client";
import { toast } from "react-toastify";


interface Props {
  isOpen: boolean;
  onClose: () => void;
  userId: number;
  username: string;
  temporaryPassword: string;
  activationToken: string;
  title?: string;
  subtitle?: string;


}

export const ResetCredentialsModal: React.FC<Props> = ({
  isOpen,
  onClose,
  userId,
  username,
  temporaryPassword,
  activationToken,
  title = "Informations d'activation",
  subtitle = "Communiquez ces informations à l'employé.",


}) => {
  if (!isOpen) return null;

  const copyToClipboard = () => {
    navigator.clipboard.writeText(
      `Utilisateur: ${username}
        Mot de passe temporaire: ${temporaryPassword}
        Clé d'activation: ${activationToken}`
    );
  };

  const [isDownloading, setIsDownloading] = useState(false);
  
    const handleDownloadPDF = async () => {
      setIsDownloading(true);
      try {
        // 🎯 IMPORTANT : Forcer responseType à 'blob' pour traiter correctement le flux binaire du PDF
        const response = await apiClient.get(`/utilisateurs/${userId}/export_reset_pdf/`, {
          responseType: "blob",
        });
  
        // Création d'un objet URL à partir du blob binaire reçu du serveur Django
        const blob = new Blob([response.data], { type: "application/pdf" });
        const url = window.URL.createObjectURL(blob);
        
        // Simulation d'un clic sur un lien masqué pour lancer le téléchargement natif du navigateur
        const link = document.createElement("a");
        link.href = url;
        /*link.setAttribute(
          "download",
          `reinitialisation_${username}.pdf`
        );
        */
        link.download = `reinitialisation_${username}.pdf`;
        document.body.appendChild(link);
        link.click();
        
        // Nettoyage de la mémoire du navigateur
        //link.parentNode?.removeChild(link);
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
  
        toast.success("📄 Fiche PDF générée et téléchargée avec succès !");
      } catch (err: any) {
        console.error("Erreur d'export PDF :", err);
        toast.error("Impossible de générer le fichier PDF. Vérifiez qu'il y a des comptes en attente.");
      } finally {
        setIsDownloading(false);
      }
    };
  
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-lg p-6 animate-modal-entrance">

        <div className="mb-4">
          <h2 className="text-xl font-bold text-gray-900">
            {title}
          </h2>

          <p className="text-sm text-gray-500 mt-1">
            {subtitle}
          </p>
        </div>

        <div className="space-y-3">
          <div className="border rounded-lg p-3 bg-gray-50">
            <div className="text-xs text-gray-500">
              ID d'utilisateur
            </div>

            <div className="font-mono font-semibold text-blue-700">
              {userId}
            </div>
          </div>

          <div className="border rounded-lg p-3 bg-gray-50">
            <div className="text-xs text-gray-500">
              Nom d'utilisateur
            </div>

            <div className="font-mono font-semibold text-blue-700">
              {username}
            </div>
          </div>

          <div className="border rounded-lg p-3 bg-gray-50">
            <div className="text-xs text-gray-500">
              Mot de passe temporaire
            </div>

            <div className="font-mono font-semibold text-purple-700">
              {temporaryPassword}
            </div>
          </div>

          <div className="border rounded-lg p-3 bg-gray-50">
            <div className="text-xs text-gray-500">
              Clé d'activation
            </div>

            <div className="font-mono font-semibold text-red-600">
              {activationToken}
            </div>
          </div>

        </div>

        <div className="flex justify-end gap-3 mt-6">
          <button
            onClick={handleDownloadPDF}
            disabled={isDownloading}
            className="w-full flex items-center justify-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2.5 px-4 rounded-lg shadow-sm transition disabled:opacity-50"
          >
            {isDownloading ? (
            <>
            <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            <span>Génération du PDF...</span>
            </>
            ) : (
            <>
            {/* Icône SVG d'une imprimante / document */}
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://w3.org">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
            </svg>
            <span>Imprimer la fiche d'activation</span>
            </>
            )}
          </button>

          <button
            onClick={copyToClipboard}
            className="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-md text-sm"
          >
            Copier
          </button>

          <button
            onClick={onClose}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md text-sm"
          >
            Fermer
          </button>

        </div>

      </div>
    </div>
  );
};