// src/features/reports/components/AnimatedKpiCard.tsx

import { motion } from "framer-motion";

interface AnimatedKpiCardProps {
  title: string;
  value: string | number;
  description?: string;
  color?: string;
}

export const AnimatedKpiCard = ({
  title,
  value,
  description,
  color = "bg-gray-100 text-gray-800",
}: AnimatedKpiCardProps) => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className={`rounded-lg shadow p-6 ${color}`}
    >
      <h3 className="text-lg font-bold">{title}</h3>
      <motion.p
        key={value} // permet de relancer l’animation à chaque changement
        initial={{ y: -10, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.4 }}
        className="text-2xl font-extrabold"
      >
        {value}
      </motion.p>
      {description && (
        <p className="text-sm text-gray-600 dark:text-gray-400">{description}</p>
      )}
    </motion.div>
  );
};
