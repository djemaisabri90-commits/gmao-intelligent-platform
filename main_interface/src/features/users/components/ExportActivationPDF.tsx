import React, { useState } from "react";
import { toast } from "react-toastify";
import { apiClient } from "../../../api/client";

export const ExportActivationPDF: React.FC = () => {
  const [isDownloading, setIsDownloading] = useState(false);

  const handleDownloadPDF = async () => {
    setIsDownloading(true);
    try {
      // 🎯 IMPORTANT : Forcer responseType à 'blob' pour traiter correctement le flux binaire du PDF
      const response = await apiClient.get("/utilisateurs/export_activation_pdf/", {
        responseType: "blob",
      });

      // Création d'un objet URL à partir du blob binaire reçu du serveur Django
      const blob = new Blob([response.data], { type: "application/pdf" });
      const url = window.URL.createObjectURL(blob);
      
      // Simulation d'un clic sur un lien masqué pour lancer le téléchargement natif du navigateur
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `fiches_activation_gmao_${new Date().toISOString().split('T')[0]}.pdf`);
      document.body.appendChild(link);
      link.click();
      
      // Nettoyage de la mémoire du navigateur
      link.parentNode?.removeChild(link);
      window.URL.revokeObjectURL(url);

      toast.success("📄 Fiches PDF générées et téléchargées avec succès !");
    } catch (err: any) {
      console.error("Erreur d'export PDF :", err);
      toast.error("Impossible de générer le fichier PDF. Vérifiez qu'il y a des comptes en attente.");
    } finally {
      setIsDownloading(false);
    }
  };

  return (
    <div className="backdrop-blur-xl bg-white border border-gray-100 rounded-xl p-6 shadow-sm max-w-sm">
      <h3 className="text-lg font-bold text-gray-800 mb-2">Imprimerie des Identifiants</h3>
      <p className="text-xs text-gray-500 mb-4">
        Génère un catalogue de fiches individuelles avec lignes de pointillés pour découpe manuelle (Distribution d'usine sans email).
      </p>
      
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
            <span>Imprimer les fiches d'activation</span>
          </>
        )}
      </button>
    </div>
  );
};
