import { useStockAlerts } from '../hooks/useReports';

export const StockAlertsTable = () => {
  const { data: alerts, isLoading } = useStockAlerts();

  if (isLoading) return <div className="text-gray-500">Chargement...</div>;
  if (!alerts?.length) return <div className="text-gray-500">Aucune alerte stock.</div>;

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <h3 className="text-lg font-medium text-gray-900 p-6 pb-0">Alertes stock</h3>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Référence</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nom</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Quantité</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Seuil</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {alerts.map((piece) => (
              <tr key={piece.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{piece.reference}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{piece.nom}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-red-600 font-semibold">{piece.quantite}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{piece.seuil_alerte}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};