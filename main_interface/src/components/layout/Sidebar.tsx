// src/components/Sidebar.tsx
import { Link, useNavigate } from "react-router-dom";
import { useAuthStore } from "../../store/authStore";
import { NotificationMenu } from "./NotificationMenu";

export const Sidebar = () => {
  const { user, logout: clearUser } = useAuthStore();
  const navigate = useNavigate();

  const navigation = [
    { name: "Tableau de bord", href: "/reports", icon: "📊" },
    { name: "Signalements", href: "/signalements", icon: "⚠️" },
    { name: "Bons de travail", href: "/workorders", icon: "📝" },
    { name: "Interventions", href: "/interventions", icon: "🔧" },
    { name: "Machines", href: "/machines", icon: "🏭" },
    { name: "Pièces", href: "/pieces", icon: "⚙️" },
    { name: "Prédictive", href: "/predictive", icon: "🔮" },
    { name: "Logs", href: "/logs", icon: "📜" },
    { name: "Audit", href: "/auditlogs", icon: "🔍" },
    { name: "Utilisateurs", href: "/utilisateurs", icon: "👥" },
  ];

  const handleLogout = () => {
    clearUser();
    navigate("/login");
  };

  return (
    <aside className="fixed top-0 left-0 h-screen w-64 bg-gradient-to-b from-blue-50 to-blue-100 shadow-lg flex flex-col justify-between z-50">
      {/* Logo */}
      <div>
        <div className="flex items-center justify-center h-20 border-b">
          <img src="/src/assets/logoApp.png" alt="Logo" className="h-12" />
        </div>

        {/* Navigation */}
        <nav className="mt-6 space-y-2 px-4">
          {navigation.map((item) => (
            <Link
              key={item.name}
              to={item.href}
              className="flex items-center px-3 py-2 rounded-md text-gray-700 hover:bg-blue-200 hover:text-blue-800 transition-colors"
            >
              <span className="mr-2">{item.icon}</span>
              {item.name}
            </Link>
          ))}
        </nav>
      </div>

      {/* Bas de sidebar */}
      <div className="border-t px-4 py-4">
        <NotificationMenu />
        {user ? (
          <button
            onClick={handleLogout}
            className="mt-4 w-full px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-red-100 hover:text-red-600 transition-colors"
          >
            Déconnexion
          </button>
        ) : (
          <Link
            to="/login"
            className="mt-4 block px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-blue-200 hover:text-blue-800"
          >
            Connexion
          </Link>
        )}
      </div>
    </aside>
  );
};
