// src/features/users/components/ForcePasswordChange.tsx
import { useState } from "react";
import { useForcePasswordChange } from "../hooks/useForcePasswordChange";
import toast from "react-hot-toast";

interface Props {
  userId: number;
  onSuccess: () => void; // callback après succès
}

export const ForcePasswordChange = ({ userId, onSuccess }: Props) => {
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [error, setError] = useState("");
  const mutation = useForcePasswordChange();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== password2) {
      setError("Les mots de passe ne correspondent pas");
      return;
    }
    if (password.length < 8) {
      setError("Le mot de passe doit contenir au moins 8 caractères");
      return;
    }

    mutation.mutate(
      { id: userId, password },
      {
        onSuccess: () => {
          toast.success("Mot de passe modifié avec succès !");
          setPassword("");
          setPassword2("");
          onSuccess();
        },
        onError: (err: any) => {
          const msg = err?.response?.data?.detail || "Erreur lors du changement de mot de passe";
          toast.error(msg);
        },
      }
    );
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="max-w-md mx-auto bg-white shadow rounded-lg p-6 space-y-4"
    >
      <h2 className="text-lg font-semibold text-gray-900">
        Changer votre mot de passe
      </h2>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-gray-700">
          Nouveau mot de passe
        </label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="mt-1 block w-full border rounded-md p-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />
      </div>

      <div>
        <label htmlFor="password2" className="block text-sm font-medium text-gray-700">
          Confirmer le mot de passe
        </label>
        <input
          type="password"
          id="password2"
          value={password2}
          onChange={(e) => setPassword2(e.target.value)}
          required
          className="mt-1 block w-full border rounded-md p-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />
        {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
      </div>

      <button
        type="submit"
        disabled={mutation.isPending}
        className="w-full py-2 px-4 rounded-md text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
      >
        {mutation.isPending ? "Enregistrement..." : "Enregistrer"}
      </button>
    </form>
  );
};
