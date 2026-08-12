//src/features/components/RecentLogsTable.tsx
import { useRecentLogs } from '../hooks/useReports';

import { useEffect } from "react";

interface RecentLogsTableProps {
  enableStreaming?: boolean; // ✅ nouvelle prop optionnelle
}

export const RecentLogsTable = ({ enableStreaming }: RecentLogsTableProps) => {
  const { data: logs, isLoading } = useRecentLogs(10);

  useEffect(() => {
    if (enableStreaming) {
      // Ici tu pourrais brancher un WebSocket ou SSE pour actualiser les logs
      console.log("Streaming activé pour les journaux récents");
    }
  }, [enableStreaming]);

  if (isLoading) return <div className="text-gray-500">Chargement...</div>;
  if (!logs?.length) return <div className="text-gray-500">Aucun log récent.</div>;

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <h3 className="text-lg font-medium text-gray-900 p-6 pb-0">Dernières actions</h3>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Utilisateur</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Action</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Bon de travail</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {logs.map((log) => (
              <tr key={log.id}>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {new Date(log.date_action).toLocaleString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {log.user_detail?.username || `#${log.user}`}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{log.action}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  WO#{log.workorder}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};