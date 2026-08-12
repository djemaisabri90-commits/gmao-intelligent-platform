// layouts/MainLayout.tsx
import { Outlet } from 'react-router-dom';
import { Navbar } from '@/components/layout/Navbar';
//import { Sidebar } from '@/components/layout/Sidebar';
import { useAuthStore } from "../store/authStore";
import { AlertBanner } from '@/features/auth/components/AlertBanner';

export const MainLayout = () => {
  const { user } = useAuthStore();
  
  // 🛡️ Si l'utilisateur doit changer de mot de passe, on applique le rideau de fer UI
  if (user && user.must_change_password) {
    return (
      <div className="relative min-h-screen w-screen bg-gray-900/40 backdrop-blur-sm flex items-center justify-center p-4">
        {/* Floutage d'arrière-plan de l'usine pour bloquer l'accès visuel aux machines */}
        <div className="absolute inset-0 bg-cover bg-center filter blur-md opacity-20" style={{ backgroundImage: "url('src/assets/logoApp.png')" }} />
        
        <div className="relative z-50 max-w-lg w-full bg-white rounded-xl shadow-2xl p-2 Convertible animate-modern-alert">
          <AlertBanner message="Pour des raisons de sécurité en entreprise, vous devez obligatoirement modifier votre mot de passe temporaire initial avant de pouvoir accéder aux fonctionnalités de la GMAO." />
        </div>
      </div>
    );
  }

  // Cas nominal : l'utilisateur a déjà configuré son mot de passe, il accède normalement au reste de l'application
  return (
    <div className="flex h-screen bg-gray-100 overflow-hidden">
      {/* Votre barre latérale de navigation (Sidebar) de GMAO ici */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Votre barre supérieure (Header/Navbar) ici */}
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50 p-6">
          <Navbar />
          <Outlet /> {/* Affiche la page demandée (Dashboard, Ordres de travail, etc.) */}
        </main>
      </div>
    </div>
  );
};










  
  
  
  
  
  
  
  /*
  return (
    <div className="min-h-screen bg-gray-100">
      {/* ✅ Bannière persistante 
      
      
      {user && user.must_change_password && user.role !== "admin" && (
        <AlertBanner message="Vous devez changer votre mot de passe avant d'accéder pleinement au tableau de bord." />
      )}

      <Navbar />
      
      <main className="container mx-auto px-4 py-8">
        <Outlet />
      </main>
    </div>
  );
  */
