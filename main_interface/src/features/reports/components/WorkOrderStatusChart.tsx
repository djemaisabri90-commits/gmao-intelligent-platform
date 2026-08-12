// src/features/reports/components/WorkOrderStatusChart.tsx

import { useWorkOrderStats } from '../hooks/useReports';
import {
  PieChart,
  Pie,
  ResponsiveContainer,
  Legend,
  Tooltip,
  Sector,
} from 'recharts';

const COLORS = ['#F59E0B', '#8B5CF6', '#3B82F6', '#10B981'];

// ✅ Tooltip custom (sans casser formatter)
const CustomTooltip = ({ active, payload }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white border border-gray-200 shadow-lg rounded-lg p-3">
        <p className="text-sm font-semibold text-gray-800 mb-2">
          Détail
        </p>

        {payload.map((entry: any, index: number) => (
          <div key={index} className="flex items-center gap-2 text-xs">
            <div
              className="w-2 h-2 rounded-full"
              style={{ backgroundColor: entry.payload.fill || entry.color }} // ✅ Utilise la couleur exacte de la part
            />
            <span className="text-gray-600">{entry.name} :</span>
            <span className="font-medium text-gray-900">
              {entry.value} bon(s)
            </span>
          </div>
        ))}
      </div>
    );
  }

  return null;
};

export const WorkOrderStatusChart = () => {
  const { data: stats, isLoading } = useWorkOrderStats();

  if (isLoading) {
    return <div className="text-gray-500">Chargement...</div>;
  }

  if (!stats?.by_etat) return null;

  // ✅ Mapping backend avec injection de la couleur 'fill' pour la légende
  const data = Object.entries(stats.by_etat).map(([name, value], index) => ({
    name:
      name === 'en_attente'
        ? 'En attente'
        : name === 'valide'
        ? 'Validé'
        : name === 'en_cours'
        ? 'En cours'
        : name === 'clos'
        ? 'Clos'
        : name,
    value,
    fill: COLORS[index % COLORS.length] // 👈 ✅ Recharts lit cette propriété pour colorer la légende !
  }));

  if (data.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6 text-center text-gray-500">
        Aucune donnée disponible
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6 hover:shadow-md transition-all duration-300">
      
      {/* Header */}
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-900">
          Répartition par état
        </h3>
        <p className="text-sm text-gray-500">
          Distribution des ordres de travail
        </p>
      </div>

      <ResponsiveContainer width={350} height={300}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            outerRadius={90} // 👈 légèrement augmenté
            dataKey="value"
            label={({ name, percent = 0 }) =>
              `${name} ${(percent * 100).toFixed(0)}%`
            }
            shape={(props) => (
              <Sector
                {...props}
                fill={COLORS[props.index % COLORS.length]}
              />
            )}
          />

          {/* ✅ Tooltip amélioré */}
          <Tooltip content={<CustomTooltip />} />

          {/* ✅ Legend avec icônes "circle" synchronisées sur COLORS */}
          <Legend
            verticalAlign="bottom"
            height={36}
            iconType="circle"
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};
