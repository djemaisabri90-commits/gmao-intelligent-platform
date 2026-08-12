// src/components/layout/NotificationListener.tsx
import { useEffect } from "react";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import { useAuthStore } from "../../store/authStore";

export const NotificationListener = () => {
  const { user } = useAuthStore();
  const navigate = useNavigate();

  useEffect(() => {
    if (!user) return; // pas de socket si non connecté

    const socket = new WebSocket("ws://localhost:8000/ws/notifications/");

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      toast.info(
        <div>
          <p>{data.text} ({data.categorie})</p>
          <button
            onClick={() => navigate(data.url)}
            className="mt-2 px-2 py-1 bg-blue-600 text-white rounded"
          >
            Voir le bon
          </button>
        </div>,
        { autoClose: 8000 }
      );


      //toast.success(data.text);  ✅ afficher notification
    };

    return () => socket.close();
  }, [user, navigate]);

  return null; // pas d'UI, juste la logique
};
