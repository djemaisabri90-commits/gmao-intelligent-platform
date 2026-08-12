//src/features/auth/pages/LoginPage.tsx

import { useState, useEffect } from 'react';
import { useNavigate, Link, useLocation } from 'react-router-dom';
import { useAuthStore } from '../../../store/authStore';
import { login } from '../api/authApi';
import { toast } from "react-toastify";

export const LoginPage = () => {
  const [step, setStep] = useState(1); // ✅ MFA step
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const { setAuth } = useAuthStore();

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    if (params.get("expired")) {
      setError("Votre session a expiré, merci de vous reconnecter.");
    }
  }, [location.search]);

  const handleNext = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (step === 1) {
      if (!username) {
        setError("Veuillez saisir votre identifiant.");
        return;
      }
      setStep(2);
      return;
    }

    if (step === 2) {
      setIsLoading(true);
      try {
        const response = await login(username, password);
        setAuth(response.access, response.refresh, response.user);
        /*if (response.user.must_change_password) {
          navigate('/reset-password');
        } else {
          navigate('/');
        }*/

        toast.success(
          `Bienvenue de nouveau, ${response.user.first_name || response.user.username} !`
        );

        if (response.user.must_change_password) {
          navigate('/reset-password');
        }

        navigate('/');
      } catch (err: any) {
        if (err.response?.data?.detail) {
          setError(err.response.data.detail);
        } else if (err.message) {
          setError(err.message);
        } else {
          setError('Identifiants incorrects');
        }
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
  <div className="relative h-screen w-screen flex items-center justify-center overflow-hidden">

    {/* 🌍 FULLSCREEN BACKGROUND */}
    <div
      className="fixed inset-0 bg-cover bg-center"
      style={{
        backgroundImage: "url('src/assets/logoApp.png')",
      }}
    />

    {/* 🌑 OVERLAY */}
    <div className="fixed inset-0 bg-gradient-to-br from-black/80 via-black/60 to-black/80" />

    {/* ✨ floating shapes */}
    <div className="absolute w-72 h-72 bg-blue-500/20 rounded-full blur-3xl top-10 left-10 animate-pulse" />
    <div className="absolute w-72 h-72 bg-purple-500/20 rounded-full blur-3xl bottom-10 right-10 animate-pulse" />

    {/* MAIN CONTENT */}
    <div className="relative z-10 w-full max-w-md space-y-6">

      {/* LOGO */}
      <div className="flex justify-center">
        <img
          src="src/assets/logo.png"
          alt="Logo entreprise"
          className="w-20 drop-shadow-lg"
        />
      </div>

      {/* TITLE */}
      <h2 className="text-center text-3xl font-bold text-white tracking-wide">
        Connexion
      </h2>

      {/* FORM */}
      <div className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-2xl shadow-2xl p-6">

        <form className="space-y-5" onSubmit={handleNext}>

          {/* STEP 1 */}
          {step === 1 && (
            <input
              id="username"
              name="username"
              type="text"
              autoComplete="username"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Nom d'utilisateur"
              className="w-full px-4 py-3 rounded-md bg-white/90 focus:bg-white border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          )}

          {/* STEP 2 */}
          {step === 2 && (
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="current-password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Mot de passe"
              className="w-full px-4 py-3 rounded-md bg-white/90 focus:bg-white border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          )}

          {/* ERROR */}
          {error && (
            <div className="text-red-300 text-sm text-center animate-pulse">
              {error}
            </div>
          )}

          {/* BUTTON */}
          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3 rounded-md bg-blue-600 hover:bg-blue-700 text-white font-medium transition"
          >
            {isLoading
              ? "Connexion..."
              : step === 1
              ? "Suivant"
              : "Se connecter"}
          </button>

        </form>
      </div>

      {/* FOOTER */}
      <p className="text-center text-sm text-white/70">
        <Link to="/password-reset-request" className="hover:text-white">
          Mot de passe oublié ?
        </Link>
      </p>

    </div>
  </div>
);
};
