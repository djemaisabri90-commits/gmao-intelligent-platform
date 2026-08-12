// src/components/layout/NotificationMenu.tsx
import { Fragment, useState } from "react";
import { Menu, Transition } from "@headlessui/react";
import { BellIcon } from "@heroicons/react/24/outline";
import { useNotifications, useMarkNotificationRead } from "../../features/notifications/hooks/useNotifications";
import { useNavigate } from "react-router-dom";
import { apiClient } from "@/api/client";
import { useQueryClient } from "@tanstack/react-query";

export const NotificationMenu = () => {
  const [currentPage, setCurrentPage] = useState(1); // ✅ gestion pagination
  const { data } = useNotifications(currentPage);
  const notifications = data?.results ?? [];
  const totalCount = data?.count ?? 0;
  const markRead = useMarkNotificationRead();
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const markAllRead = async () => {
    await apiClient.post("/notifications/mark_all_read/");
    queryClient.invalidateQueries({ queryKey: ["notifications"] });
  };

  const unreadCount = notifications.filter(n => !n.is_read).length;

  const hasNextPage = Boolean(data?.next);
  const hasPrevPage = Boolean(data?.previous);

  return (
    <Menu as="div" className="relative ml-3">
      <Menu.Button className="relative p-2 rounded-full text-gray-700 hover:text-blue-600 focus:outline-none">
        <BellIcon className="h-6 w-4" />
        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full px-1">
            {unreadCount}
          </span>
        )}
      </Menu.Button>
      <Transition
        as={Fragment}
        enter="transition ease-out duration-100"
        enterFrom="transform opacity-0 scale-95"
        enterTo="transform opacity-100 scale-100"
        leave="transition ease-in duration-75"
        leaveFrom="transform opacity-100 scale-100"
        leaveTo="transform opacity-0 scale-95"
      >
        <Menu.Items className="absolute right-0 mt-2 w-80 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-10">
          <div className="py-1 max-h-96 overflow-y-auto">
            {notifications.length ? (
              notifications.map((n) => (
                <Menu.Item key={n.id}>
                  {({ active }) => (
                    <div
                      onClick={() => {
                        markRead.mutate(n.id);
                        if (n.url) navigate(n.url);
                      }}
                      className={`cursor-pointer px-4 py-2 text-sm ${
                        active ? "bg-gray-100" : ""
                      } ${n.is_read ? "text-gray-500" : "text-gray-700 font-medium"}`}
                    >
                      {n.message}
                      <div className="text-xs text-gray-400">
                        {new Date(n.created_at).toLocaleString()}
                      </div>
                    </div>
                  )}
                </Menu.Item>
              ))
            ) : (
              <div className="px-4 py-2 text-sm text-gray-500">Aucune notification</div>
            )}
          </div>

          {/* ✅ Bouton "Tout marquer comme lu" */}
          {notifications.length > 0 && (
            <div className="border-t border-gray-200">
              <button
                onClick={markAllRead}
                className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                Tout marquer comme lu
              </button>
            </div>
          )}

          {/* ✅ Pagination */}
          <div className="flex justify-between items-center px-4 py-2 border-t border-gray-200 text-sm">
            <button
              disabled={!hasPrevPage}
              onClick={() => setCurrentPage((p) => Math.max(p - 1, 1))}
              className={`px-2 py-1 rounded ${
                hasPrevPage ? "text-blue-600 hover:bg-gray-100" : "text-gray-400 cursor-not-allowed"
              }`}
            >
              Précédent
            </button>
            <span className="text-gray-500">
              Page {currentPage} / {Math.ceil(totalCount / 10)}
            </span>
            <button
              disabled={!hasNextPage}
              onClick={() => setCurrentPage((p) => p + 1)}
              className={`px-2 py-1 rounded ${
                hasNextPage ? "text-blue-600 hover:bg-gray-100" : "text-gray-400 cursor-not-allowed"
              }`}
            >
              Suivant
            </button>
          </div>
        </Menu.Items>
      </Transition>
    </Menu>
  );
};
