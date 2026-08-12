import React from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

interface AlertBannerProps {
  message: string;
}

export const AlertBanner: React.FC<AlertBannerProps> = ({ message }) => {
  const navigate = useNavigate();

  const handleClick = () => {
    toast.info("🔑 Redirection vers la page de réinitialisation du mot de passe...");
    navigate("/reset-password");
  };

  return (
    <div className="bg-yellow-100 border border-yellow-400 text-yellow-800 px-4 py-3 rounded relative mb-4 flex justify-between items-center">
      <div>
        <strong className="font-bold">⚠️ Attention : </strong>
        <span className="block sm:inline">{message}</span>
      </div>
      <button
        onClick={handleClick}
        className="ml-4 bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700"
      >
        Changer maintenant
      </button>
    </div>
  );
};
