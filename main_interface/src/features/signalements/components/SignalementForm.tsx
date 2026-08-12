// src/features/signalements/components/SignalementForm.tsx

import { useState } from "react";
import { useMachines } from "../../machines/hooks/useMachines";
import type { Signalement } from "../types";
import { SignalementStatus } from "../types"; // import enum-like object

interface SignalementFormProps {
  initialData?: Partial<Signalement>;
  onSubmit: (data: Partial<Signalement>) => void;
  isLoading?: boolean;
}

type SignalementFormData = {
  machine: number | "";
  description: string;
  source: Signalement["source"];
  statut: Signalement["statut"];
};

export const SignalementForm = ({
  initialData = {},
  onSubmit,
  isLoading = false,
}: SignalementFormProps) => {
  const { data: machines } = useMachines();

  const [formData, setFormData] = useState<SignalementFormData>({
    machine: initialData.machine ?? "",
    description: initialData.description ?? "",
    source: initialData.source ?? "manuel",
    //statut: initialData.statut ?? SignalementStatus.nouveau,
    statut: SignalementStatus.nouveau,

  });

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
    const data: Partial<Signalement> = {
      machine: formData.machine === "" ? undefined : Number(formData.machine),
      description: formData.description,
      source: formData.source,
      statut: formData.statut,
    };
    onSubmit(data);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Machine */}
      <div>
        <label
          htmlFor="machine"
          className="block text-sm font-medium text-gray-700"
        >
          Machine *
        </label>
        <select
          name="machine"
          id="machine"
          required
          value={formData.machine}
          onChange={handleChange}
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        >
          <option value="">Sélectionnez une machine</option>
          {machines?.map((machine) => (
            <option key={machine.id} value={machine.id}>
              {machine.nom}
            </option>
          ))}
        </select>
      </div>

      {/* Description */}
      <div>
        <label
          htmlFor="description"
          className="block text-sm font-medium text-gray-700"
        >
          Description *
        </label>
        <textarea
          name="description"
          id="description"
          rows={3}
          required
          value={formData.description}
          onChange={handleChange}
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />
      </div>

      {/* Source */}
      <div>
        <label
          htmlFor="source"
          className="block text-sm font-medium text-gray-700"
        >
          Source
        </label>
        {/*<select
          name="source"
          id="source"
          value={formData.source}
          onChange={handleChange}
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        >
          <option value="manuel">Humain</option>
          <option value="preventif">Préventif</option>
          <option value="iot">IoT</option>
        </select>*/}
        <input
          type="text"
          value="Humain"
          disabled
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 bg-gray-100 text-gray-700 sm:text-sm"
        />
        {/* valeur cachée réellement envoyée */}
        <input type="hidden" name="source" value="manuel" />
      </div>

      {/* Statut */}
      {/*<div>
        <label
          htmlFor="statut"
          className="block text-sm font-medium text-gray-700"
        >
          Statut
        </label>
        {/*<select
          name="statut"
          id="statut"
          value={formData.statut}
          onChange={handleChange}
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        >
          <option value={SignalementStatus.nouveau}>Nouveau</option>
          <option value={SignalementStatus.en_cours}>En cours</option>
          <option value={SignalementStatus.traite}>Traité</option>
          <option value={SignalementStatus.clos}>Clos</option>
        </select>
        </div>*/}
        <input
          type="hidden"
          name="statut"
          value={SignalementStatus.nouveau}
        />

      {/* Submit */}
      <button
        type="submit"
        disabled={isLoading}
        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
      >
        {isLoading ? "Enregistrement..." : "Enregistrer"}
      </button>
    </form>
  );
};
