//src/features/auth/pages/ResetPassword.tsx

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { apiClient } from "../../../api/client";
import { useAuthStore } from "../../../store/authStore";

export const ResetPasswordPage = () => {
  const [username, setUsername] = useState("");
  const [activationToken, setActivationToken] = useState(""); // 🔑 Nouveau : Stocke le code d'activation

  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();

  useEffect(() => {
    // ✅ Protection : si user est connecté et must_change_password = false → retour login
    if (user && !user.must_change_password) {
      navigate("/login");
    }
  }, [user, navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (password !== confirmPassword) {
      setError("Les mots de passe ne correspondent pas.");
      return;
    }

    setIsLoading(true);
    try {
      if (user) {
        // ✅ Cas connecté → endpoint par ID
        await apiClient.post(`/utilisateurs/${user.id}/change_password/`, {
          activation_token: activationToken,
          password,
        });
      } else {
        // ✅ Cas non connecté → endpoint global
        await apiClient.post(`/utilisateurs/change_password_by_username/`, {
          username,
          activation_token: activationToken,
          password,
        });
      }

      toast.success("Mot de passe changé avec succès. Veuillez vous reconnecter.");

      // Nettoyage complet des tokens de session pour forcer une reconnexion propre
      if (logout) logout();
      localStorage.clear();

      navigate("/login");
    } catch (err: any) {
      // 🛡️ Gestion propre du Throttling (Erreur 429) ou code invalide
      if (err.response?.status === 429) {
        setError("Trop de tentatives infructueuses. Veuillez patienter 1 minute.");
      } else {
        setError(err.response?.data?.error || "Le code d'activation ou les identifiants sont incorrects.");
      }
      //setError(err.response?.data?.error || "Erreur lors de la réinitialisation.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-lg">
        <h2 className="text-center text-xl font-bold mb-2">Réinitialisation sécurisée</h2>
        <p className="text-xs text-gray-500 text-center mb-6">
          Veuillez utiliser le code secret fourni sur votre fiche d'activation.
        </p>
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Si l'utilisateur n'est pas connecté, on lui demande son username */}
          {!user && (
            <div>
            <input
              type="text"
              placeholder="Nom d'utilisateur"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full border p-2 rounded"
              required
            />
            </div>
          )}
          
          {/* 🔑 Champ obligatoire ajouté pour la validation autonome */}
          {/* Saisie obligatoire de la preuve physique (activation_token) */}
          <div>
          <input
            type="text"
            placeholder="Code d'activation unique (Ex: 4a8b-9c2d)"
            value={activationToken}
            onChange={(e) => setActivationToken(e.target.value)}
            className="w-full border p-2 rounded bg-blue-50/50 border-blue-200 focus:border-blue-500"
            required
          />
          </div>

          <input
            type="password"
            placeholder="Nouveau mot de passe"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full border p-2 rounded"
            required
          />
          <div>
          <input
            type="password"
            placeholder="Confirmer le mot de passe"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className="w-full border p-2 rounded"
            required
          />
          </div>
          {error && <p className="text-red-600 text-sm text-center">{error}</p>}
          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:opacity-50"
          >
            {isLoading ? "Vérification..." : "Valider et changer le mot de passe"}
            
          </button>
        </form>
      </div>
    </div>
  );
};
