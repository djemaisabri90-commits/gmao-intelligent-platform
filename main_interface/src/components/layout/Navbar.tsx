import { useState, useRef, useEffect, useMemo } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuthStore } from "../../store/authStore";
import { logout } from "../../features/auth/api/authApi";
import { NotificationMenu } from "./NotificationMenu";

export const Navbar = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
  const userMenuRef = useRef<HTMLDivElement>(null);
  const { user, logout: clearUser } = useAuthStore();
  const navigate = useNavigate();

  // Liens regroupés par catégories (sans "Tableau de bord")
  const navigation = useMemo(() => {
    const role = user?.role;

    const operations = [
      { name: "Signalements", href: "/signalements", icon: "⚠️" },
      { name: "Bons de travail", href: "/workorders", icon: "📝" },
      { name: "Interventions", href: "/interventions", icon: "🔧" },
      
    ];

    const administration = [
      { name: "Machines", href: "/machines", icon: "🏭" },
      { name: "Pièces", href: "/pieces", icon: "⚙️" },
      { name: "prédictive", href: "/predictive", icon: "🔧" },
      { name: "Logs", href: "/logs", icon: "📜" },
      { name: "Audit", href: "/auditlogs", icon: "🔍" },
      { name: "Utilisateurs", href: "/utilisateurs", icon: "👥" },
      { name: "Demande", href: "/password-reset-requests", icon: "👥" },

    ];

    const signale = [
      {name: "Signalements", href: "/signalements", icon: "⚠️" }
    ]

    const methode = [
      { name: "Machines", href: "/machines", icon: "🏭" },
      { name: "Pièces", href: "/pieces", icon: "⚙️" },
      { name: "prédictive", href: "/predictive", icon: "🔧" },
      { name: "Logs", href: "/logs", icon: "📜" },
    ]
    
    if (role === "admin") return [...operations, ...administration];
    if (role === "expert") return [...operations, ...methode];
    if (role === "technicien") return [...operations];
    if (role === "operateur") return [...signale];
    return [];
  }, [user?.role]);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (userMenuRef.current && !userMenuRef.current.contains(event.target as Node)) {
        setIsUserMenuOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleLogout = () => {
    logout();
    clearUser();
    navigate("/login");
  };

  return (
    <nav className="w-full bg-white shadow-md z-50">
      <div className="container mx-auto px-8">
        <div className="flex justify-between items-center h-20">
          {/* Logo → redirection vers dashboard */}
          <Link to="/reports" className="flex items-center space-x-3">
            <img
              src="/src/assets/logoDash.png"
              alt="Logo GMAO Délice Groupe"
              className="h-20"
            />
          </Link>

          {/* Desktop navigation */}
          <div className="hidden md:flex space-x-1">
            {navigation.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                className="flex items-center text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
              >
                <span className="mr-2">{item.icon}</span>
                {item.name}
              </Link>
            ))}
          </div>

          {/* Desktop user menu */}
          <div className="hidden md:flex items-center space-x-4">
            <NotificationMenu />
            {user ? (
              <div className="relative" ref={userMenuRef}>
                <button
                  onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                  className="flex items-center space-x-2 focus:outline-none"
                >
                  <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white">
                    {user.first_name?.charAt(0) || user.username?.charAt(0) || "U"}
                  </div>
                  <span className="text-sm font-medium text-gray-700">
                    {user.first_name || user.username}
                  </span>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                {isUserMenuOpen && (
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-10 border border-gray-100 animate-fade-in">
                    <Link to="/profile" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                      Profil
                    </Link>
                    <Link to="/settings" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                      Paramètres
                    </Link>
                    <button
                      onClick={handleLogout}
                      className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    >
                      Déconnexion
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <Link
                to="/login"
                className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium"
              >
                Connexion
              </Link>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-700 hover:text-blue-600 focus:outline-none"
            >
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                {isMobileMenuOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile drawer */}
        {isMobileMenuOpen && (
          <div className="fixed inset-0 bg-black bg-opacity-30 z-40">
            <div className="fixed top-0 left-0 w-64 h-full bg-white shadow-lg p-6 z-50">
              <button
                onClick={() => setIsMobileMenuOpen(false)}
                className="mb-6 text-gray-700 hover:text-blue-600"
              >
                ✖ Fermer
              </button>
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  to={item.href}
                  className="flex items-center px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  <span className="mr-2">{item.icon}</span>
                  {item.name}
                </Link>
              ))}
              <div className="mt-6 border-t border-gray-200 pt-4">
                <NotificationMenu />
              </div>
              {user ? (
                <button
                  onClick={() => {
                    handleLogout();
                    setIsMobileMenuOpen(false);
                  }}
                  className="mt-4 block w-full text-left px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50"
                >
                  Déconnexion
                </button>
              ) : (
                <Link
                  to="/login"
                  className="mt-4 block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  Connexion
                </Link>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};
