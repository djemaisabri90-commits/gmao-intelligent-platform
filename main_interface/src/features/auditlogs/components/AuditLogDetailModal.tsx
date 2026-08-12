// src/features/auditlogs/components/AuditLogDetailModal.tsx

import { Dialog, Transition } from '@headlessui/react';
import { Fragment } from 'react';
import type { AuditLogWithDetails } from '../types';

interface AuditLogDetailModalProps {
  log: AuditLogWithDetails | null;
  isOpen: boolean;
  onClose: () => void;
}

export const AuditLogDetailModal = ({ log, isOpen, onClose }: AuditLogDetailModalProps) => {
  if (!log) return null;

  return (
    <Transition appear show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-10" onClose={onClose}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black bg-opacity-25" />
        </Transition.Child>

        <div className="fixed inset-0 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4 text-center">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 scale-95"
              enterTo="opacity-100 scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <Dialog.Panel className="w-full max-w-2xl transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                <Dialog.Title as="h3" className="text-lg font-medium leading-6 text-gray-900">
                  Détail de l'audit
                </Dialog.Title>
                <div className="mt-4 space-y-3">
                  <p><strong>Date :</strong> {new Date(log.timestamp).toLocaleString()}</p>
                  <p><strong>Utilisateur :</strong> {log.user_detail?.username || log.user || '—'}</p>
                  <p><strong>Action :</strong> {log.action}</p>
                  <p><strong>Modèle :</strong> {log.model}</p>
                  <p><strong>Objet ID :</strong> {log.object_id}</p>
                  <p><strong>Endpoint :</strong> {log.endpoint || '—'}</p>
                  <p><strong>Méthode :</strong> {log.method || '—'}</p>
                  <p><strong>IP :</strong> {log.ip_address || '—'}</p>
                  <p><strong>User-Agent :</strong> {log.user_agent || '—'}</p>
                  {log.changements && (
                    <div>
                      <strong>Changements :</strong>
                      <pre className="mt-1 p-2 bg-gray-100 rounded text-sm overflow-auto">
                        {(() => {
                          try {
                            return JSON.stringify(
            typeof log.changements === "string"
              ? JSON.parse(log.changements)
              : log.changements,
            null,
            2
          );
                          } catch {
                            return String(log.changements);
                          }
                        })()}
                      </pre>
                    </div>
                  )}
                </div>
                <div className="mt-6">
                  <button
                    type="button"
                    className="inline-flex justify-center rounded-md border border-transparent bg-blue-100 px-4 py-2 text-sm font-medium text-blue-900 hover:bg-blue-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                    onClick={onClose}
                  >
                    Fermer
                  </button>
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition>
  );
};