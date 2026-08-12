// src/features/auditlogs/components/AuditLogList.tsx

import { useAuditLogs } from '../hooks/useAuditLogs';
import type { AuditLogWithDetails } from '../types';

interface AuditLogListProps {
  onRowClick?: (log: AuditLogWithDetails) => void;
}

export const AuditLogList = ({ onRowClick }: AuditLogListProps) => {
  const { data: logs, isLoading, error } = useAuditLogs({ ordering: '-timestamp' }); // ← changer le tri

  if (isLoading) return <div className="p-4 text-gray-500">Chargement...</div>;
  if (error) return <div className="p-4 text-red-500">Erreur : {error.message}</div>;

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full bg-white border border-gray-200">
        <thead className="bg-gray-100">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Utilisateur</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Modèle</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Objet ID</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">IP</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Méthode</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {logs?.map((log) => (
            <tr
              key={log.id}
              className={`hover:bg-gray-50 ${onRowClick ? 'cursor-pointer' : ''}`}
              onClick={() => onRowClick && onRowClick(log)}
            >
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {new Date(log.timestamp).toLocaleString()}  {/* ← utilisation de timestamp */}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {log.user_detail?.username || log.user || '—'}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {log.action}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {log.model}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {log.object_id}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {log.ip_address || '—'}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {log.method || '—'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};