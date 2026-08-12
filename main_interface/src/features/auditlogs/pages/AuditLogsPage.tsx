// src/features/auditlogs/pages/AuditLogsPage.tsx

import { useState } from 'react';
import { AuditLogList } from '../components/AuditLogList';
import { AuditLogDetailModal } from '../components/AuditLogDetailModal';
import type { AuditLogWithDetails } from '../types';

export const AuditLogsPage = () => {
  const [selectedLog, setSelectedLog] = useState<AuditLogWithDetails | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleRowClick = (log: AuditLogWithDetails) => {
    setSelectedLog(log);
    setIsModalOpen(true);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Journal d'audit</h1>
      <div className="bg-white shadow-md rounded-lg overflow-hidden">
        <AuditLogList onRowClick={handleRowClick} />
      </div>
      <AuditLogDetailModal
        log={selectedLog}
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />
    </div>
  );
};