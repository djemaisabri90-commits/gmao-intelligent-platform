// src/features/users/components/UserForm.tsx
import { useState } from "react";
import type { User } from "../types";
import { useCategories } from "../hooks/useCategories";

interface UserFormProps {
  initialData?: Partial<User>;
  onSubmit: (data: Partial<User>) => void;
  isLoading?: boolean;
}

export const UserForm = ({
  initialData = {},
  onSubmit,
  isLoading = false,
}: UserFormProps) => {
  const { data: categories, isLoading: catLoading, error } = useCategories();

  const [formData, setFormData] = useState({
    username: initialData.username || "",
    email: initialData.email || "",
    first_name: initialData.first_name || "",
    last_name: initialData.last_name || "",
    role: initialData.role || "",
    telephone: initialData.telephone || "",
    categorie: initialData.categorie || "",
    is_active: initialData.is_active !== undefined ? initialData.is_active : true,
    password: "",
    password2: "",
  });

  //const [passwordError, setPasswordError] = useState("");
  const [categorieError, setCategorieError] = useState("");

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value, type } = e.target;
    if (type === "checkbox") {
      const checked = (e.target as HTMLInputElement).checked;
      setFormData((prev) => ({ ...prev, [name]: checked }));
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
    //if (name === "password" || name === "password2") setPasswordError("");
    if (name === "categorie") setCategorieError("");
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!initialData.id && formData.password !== formData.password2) {
      //setPasswordError("Les mots de passe ne correspondent pas");
      return;
    }
    // ✅ Validation dynamique : catégorie obligatoire si rôle = technicien
    if (formData.role === "technicien" && !formData.categorie) {
      setCategorieError("La catégorie est obligatoire pour un technicien");
      return;
    }
    const data: Partial<User> = {
      username: formData.username,
      email: formData.email || undefined,
      first_name: formData.first_name || undefined,
      last_name: formData.last_name || undefined,
      role: formData.role ? (formData.role as User["role"]) : undefined,
      telephone: formData.telephone || undefined,
      categorie: formData.categorie ? Number(formData.categorie) : undefined,
      is_active: formData.is_active,
    };
    if (!initialData.id && formData.password) {
      (data as any).password = formData.password;
    }
    onSubmit(data);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* username + email */}
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label htmlFor="username" className="block text-sm font-medium text-gray-700">
            Nom d'utilisateur *
          </label>
          <input
            type="text"
            name="username"
            id="username"
            required
            value={formData.username}
            onChange={handleChange}
            className="mt-1 block w-full border rounded-md shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
        </div>
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700">
            Email
          </label>
          <input
            type="email"
            name="email"
            id="email"
            value={formData.email}
            onChange={handleChange}
            className="mt-1 block w-full border rounded-md shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
        </div>
      </div>

      {/* prénom + nom */}
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label htmlFor="first_name" className="block text-sm font-medium text-gray-700">
            Prénom
          </label>
          <input
            type="text"
            name="first_name"
            id="first_name"
            value={formData.first_name}
            onChange={handleChange}
            className="mt-1 block w-full border rounded-md shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
        </div>
        <div>
          <label htmlFor="last_name" className="block text-sm font-medium text-gray-700">
            Nom
          </label>
          <input
            type="text"
            name="last_name"
            id="last_name"
            value={formData.last_name}
            onChange={handleChange}
            className="mt-1 block w-full border rounded-md shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
        </div>
      </div>

      {/* téléphone */}
      <div>
        <label htmlFor="telephone" className="block text-sm font-medium text-gray-700">
          Téléphone
        </label>
        <input
          type="text"
          name="telephone"
          id="telephone"
          value={formData.telephone}
          onChange={handleChange}
          className="mt-1 block w-full border rounded-md shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />
      </div>

      {/* rôle */}
      <div>
        <label htmlFor="role" className="block text-sm font-medium text-gray-700">
          Rôle
        </label>
        <select
          name="role"
          id="role"
          value={formData.role}
          onChange={handleChange}
          className="mt-1 block w-full border rounded-md shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        >
          <option value="">Sélectionnez un rôle</option>
          <option value="admin">Admin</option>
          <option value="expert">Expert</option>
          <option value="technicien">Technicien</option>
          <option value="operateur">Opérateur</option>
        </select>
      </div>

      {/* catégorie */}
      <div>
        <label htmlFor="categorie" className="block text-sm font-medium text-gray-700">
          Catégorie
        </label>
        {catLoading ? (
          <p className="text-gray-500 text-sm">Chargement des catégories...</p>
        ) : error ? (
          <p className="text-red-500 text-sm">Erreur de chargement des catégories</p>
        ) : (
          <select
            name="categorie"
            id="categorie"
            value={formData.categorie}
            onChange={handleChange}
            disabled={formData.role !== "technicien"} // ✅ UX : désactivé si pas technicien
            className={`mt-1 block w-full border rounded-md shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm
              ${formData.role !== "technicien" ? "bg-gray-100 cursor-not-allowed" : ""
              }`}
          >
            <option value="">
              {formData.role === "technicien"
                ? "Sélectionnez une catégorie"
                : "Seuls les techniciens peuvent avoir une catégorie"}
            </option>
            {categories?.map((cat) => (
              <option key={cat.id} value={cat.id}>
                {cat.nom}
              </option>
            ))}
          </select>
        )}
        {categorieError && <p className="mt-1 text-sm text-red-600">{categorieError}</p>}
      </div>

      {/* actif */}
      <div className="flex items-center">
        <input
          type="checkbox"
          name="is_active"
          id="is_active"
          checked={formData.is_active}
          onChange={handleChange}
          className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
        />
        <label htmlFor="is_active" className="ml-2 block text-sm text-gray-900">
          Actif
        </label>
      </div>

      {/* mot de passe uniquement en création 
      {!initialData?.id && (
        <>
        <div>
        <div className="flex justify-between items-center">
          <label htmlFor="password" className="block text-sm font-medium text-gray-700">
          Mot de passe
          </label>
          <span className="text-xs text-gray-400 font-normal">Optionnel</span>
        </div>
        <input
          type="password"
          name="password"
          id="password"
          value={formData.password || ""}
          onChange={handleChange}
          placeholder="Laisser vide pour une génération automatique"
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 text-gray-800 placeholder-gray-400 focus:ring-blue-500 focus:border-blue-500 sm:text-sm outline-none transition-all"
          />
          <p className="mt-1 text-xs text-gray-400">
          Si laissé vide, la GMAO générera un mot de passe temporaire unique et sécurisé.
          </p>
          </div>

          <div>
          <label htmlFor="password2" className="block text-sm font-medium text-gray-700">
            Confirmer le mot de passe
          </label>
          <input
            type="password"
            name="password2"
            id="password2"
            value={formData.password2 || ""}
            onChange={handleChange}
            placeholder="Confirmez le mot de passe si saisi"
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 text-gray-800 placeholder-gray-400 focus:ring-blue-500 focus:border-blue-500 sm:text-sm outline-none transition-all"
          />
          {passwordError && (
            <p className="mt-1 text-sm text-red-600 font-medium animate-pulse">
              {passwordError}
            </p>
          )}
          </div>
          </>
      )} */}

        

      <button
        type="submit"
        disabled={isLoading}
        className="w-full flex justify-center py-2 px-4 rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
      >
        {isLoading ? "Enregistrement..." : "Enregistrer"}
      </button>
    </form>
  );
};