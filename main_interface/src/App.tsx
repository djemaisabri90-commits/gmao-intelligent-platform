// src/App.tsx
import { useEffect } from 'react';
import { RouterProvider } from 'react-router-dom';
//import { RouterProvider, useNavigate } from 'react-router-dom';

import { router } from './routes';
import { useAuthStore } from './store/authStore';
import { fetchCurrentUser } from './features/auth/api/authApi'; // à créer
import { getRefreshToken } from './api/auth';
//import { Toaster } from 'react-hot-toast';
import { ToastContainer, toast } from "react-toastify";
//import { NotificationListener } from "./components/layout/NotificationListener";
import "react-toastify/dist/ReactToastify.css";
function App() {
  const { accessToken, user, setAuth } = useAuthStore();
  //const navigate = useNavigate();

  // Restauration de la session après un rafraîchissement
  useEffect(() => {
    const restoreSession = async () => {
      if (accessToken && getRefreshToken() && !user) {
        try {
          const userData = await fetchCurrentUser(); // endpoint /api/me/
          setAuth(accessToken, getRefreshToken() || '', userData);
        } catch (error) {
          // Token invalide, on déconnecte
          useAuthStore.getState().logout();
          toast.error("Votre session a expiré. Veuillez vous reconnecter.");
          //navigate("/login?expired=true"); // ✅ redirection automatique avec paramètre
        }
      }
    };
    restoreSession();
  }, [accessToken, user, setAuth]);

  return (
    <>
    <ToastContainer position="top-right" autoClose={3000}/>

    {/*<Toaster position="top-right" />*/}
    {/*<NotificationListener />  écoute globale */}
    <RouterProvider router={router} />
    </>
  );
}

export default App;

/*

// src/App.tsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import PiecesPage from './features/pieces/pages/PiecesPage';
import InterventionDetail from './features/interventions/pages/InterventionDetail';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        /* Page de gestion des pièces */
        //<Route path="/pieces" element={<PiecesPage />} />

        //{/* Page détail intervention avec pièces utilisées */}
        //<Route
          //path="/interventions/:id"
          //element={<InterventionDetailWrapper />}
       /// />
      //</Routes>
   // </Router>
 // );
//};

// Wrapper pour récupérer l'id depuis l'URL
/*import { useParams } from 'react-router-dom';

const InterventionDetailWrapper: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const interventionId = Number(id);

  return <InterventionDetail interventionId={interventionId} />;
};

export default App;
*/

