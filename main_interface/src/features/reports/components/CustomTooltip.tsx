// src/features/reports/components/CustomTooltip.tsx

import type { TooltipProps } from 'recharts';

// ✅ Type corrigé
type CustomTooltipProps = TooltipProps<number, string> & {
  payload?: Array<{
    name?: string;
    value?: number;
    color?: string;
  }>;
  label?: string;
};

export const CustomTooltip = ({
  active,
  payload,
  label,
}: CustomTooltipProps) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white border border-gray-200 shadow-lg rounded-lg p-3">
        {label && (
          <p className="text-sm font-semibold text-gray-800 mb-1">
            {label}
          </p>
        )}

        {payload.map((entry, index: number) => (
          <div key={index} className="flex items-center gap-2 text-xs">
            <div
              className="w-2 h-2 rounded-full"
              style={{ backgroundColor: entry.color }}
            />
            <span className="text-gray-600">{entry.name} :</span>
            <span className="font-medium text-gray-900">
              {entry.value}
            </span>
          </div>
        ))}
      </div>
    );
  }

  return null;
};