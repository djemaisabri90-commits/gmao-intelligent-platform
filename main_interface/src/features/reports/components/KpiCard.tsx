// src/features/reports/components/KpiCard.tsx

type Props = {
  title: string;
  value: string | number;
  description?: string;
  color?: string;
  icon?: React.ReactNode;
};

export const KpiCard = ({
  title,
  value,
  description,
  color = 'bg-gray-50 text-gray-800',
  icon,
}: Props) => {
  return (
    <div
      className={`rounded-xl p-5 shadow-sm border border-gray-100 hover:shadow-md transition-all duration-200 ${color}`}
    >
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-medium">{title}</h3>
        {icon && <div className="opacity-70">{icon}</div>}
      </div>

      <div className="text-2xl font-bold">{value}</div>

      {description && (
        <p className="text-xs mt-2 opacity-80">{description}</p>
      )}
    </div>
  );
};