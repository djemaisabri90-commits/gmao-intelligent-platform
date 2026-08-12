import { useState } from 'react';
import { apiClient } from '@/api/client';

export const ForgotPasswordPage = () => {
  const [username, setUsername] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    setLoading(true);

    try {
      await apiClient.post('/utilisateurs/request_password_reset/', {
        username,
      });

      setMessage("Votre demande a été transmise à l’administrateur.");
      setUsername('');
    } catch (err) {
      setMessage("Erreur lors de l'envoi de la demande.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-lg">

        <h2 className="text-center text-xl font-bold mb-4">
          Mot de passe oublié
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">

          <input
            type="text"
            placeholder="Nom d'utilisateur"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full border p-2 rounded"
            required
          />

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
          >
            {loading ? "Envoi..." : "Envoyer la demande"}
          </button>

        </form>

        {message && (
          <p className="mt-4 text-green-600 text-center">
            {message}
          </p>
        )}

      </div>
    </div>
  );
};