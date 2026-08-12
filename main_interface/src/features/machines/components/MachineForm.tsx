// src/features/machines/components/MachineForm.tsx
import { useState } from "react";
import type { Machine } from "../types";

interface MachineFormProps {
  initialData?: Partial<Machine>;
  onCreate?: (data: Omit<Machine, "id" | "etat">) => void;
  onUpdate?: (data: Partial<Machine>) => void;
  isLoading?: boolean;
  isEdit?: boolean;
}

export const MachineForm = ({
  initialData = {},
  onCreate,
  onUpdate,
  isLoading = false,
  isEdit = false,
}: MachineFormProps) => {
  const [formData, setFormData] = useState({
    nom: initialData.nom || "",
    description: initialData.description || "",
    localisation: initialData.localisation || "",
    type: initialData.type || "",
    date_installation: initialData.date_installation || "",
    etat: initialData.etat || "SERVICE",
  });

  const [error, setError] = useState<string | null>(null);

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
    >
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Validation frontend
    if (!formData.nom.trim()) {
      setError("Le nom de la machine est obligatoire.");
      return;
    }

    if (formData.date_installation) {
      const today = new Date();
      const selectedDate = new Date(formData.date_installation);
      if (selectedDate > today) {
        setError("La date d'installation ne peut pas être dans le futur.");
        return;
      }
    }

    setError(null);

    if (isEdit && onUpdate) {
      onUpdate(formData);
    } else if (!isEdit && onCreate) {
      const { nom, description, localisation, type, date_installation } =
        formData;
      onCreate({ nom, description, localisation, type, date_installation });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && <div className="text-red-600 text-sm font-medium">{error}</div>}

      {/* Nom */}
      <div>
        <label htmlFor="nom" className="block text-sm font-medium text-gray-700">
          Nom *
        </label>
        <input
          type="text"
          name="nom"
          id="nom"
          required
          value={formData.nom}
          onChange={handleChange}
          className="mt-1 block w-full border rounded-md shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />
      </div>

      {/* Description */}
      <div>
        <label
          htmlFor="description"
          className="block text-sm font-medium text-gray-700"
        >
          Description
        </label>
        <textarea
          name="description"
          id="description"
          rows={3}
          value={formData.description}
          onChange={handleChange}
          className="mt-1 block w-full border rounded-md shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />
      </div>

      {/* Localisation */}
      <div>
        <label
          htmlFor="localisation"
          className="block text-sm font-medium text-gray-700"
        >
          Localisation
        </label>
        <input
          type="text"
          name="localisation"
          id="localisation"
          value={formData.localisation}
          onChange={handleChange}
          className="mt-1 block w-full border rounded-md shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />
      </div>

      {/* Type */}
      <div>
        <label
          htmlFor="type"
          className="block text-sm font-medium text-gray-700"
        >
          Type
        </label>
        <input
          type="text"
          name="type"
          id="type"
          value={formData.type}
          onChange={handleChange}
          className="mt-1 block w-full border rounded-md shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />
      </div>

      {/* Date d'installation */}
      <div>
        <label
          htmlFor="date_installation"
          className="block text-sm font-medium text-gray-700"
        >
          Date d'installation
        </label>
        <input
          type="date"
          name="date_installation"
          id="date_installation"
          value={formData.date_installation}
          onChange={handleChange}
          className="mt-1 block w-full border rounded-md shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />
      </div>

      {/* État (uniquement en édition) */}
      {isEdit && (
        <div>
          <label
            htmlFor="etat"
            className="block text-sm font-medium text-gray-700"
          >
            État
          </label>
          <select
            name="etat"
            id="etat"
            value={formData.etat}
            onChange={handleChange}
            className="mt-1 block w-full border rounded-md shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          >
            <option value="SERVICE">En service</option>
            <option value="PANNE">En panne</option>
            <option value="MAINTENANCE">En maintenance</option>
            <option value="INCONNU">Inconnu</option>
          </select>
        </div>
      )}

      {/* Bouton */}
      <div>
        <button
          type="submit"
          disabled={isLoading}
          className="w-full py-2 px-4 rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
        >
          {isLoading ? "Enregistrement..." : "Enregistrer"}
        </button>
      </div>
    </form>
  );
};
