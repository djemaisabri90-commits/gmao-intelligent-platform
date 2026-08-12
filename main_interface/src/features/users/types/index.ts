// src/features/users/types/index.ts

export interface Categorie {
  id: number;
  nom: string;
  // ✅ Typage fort basé sur TYPE_CHOICES du backend
  //nom: "electrique" | "mecanique" | "automation" | "utilitaire";
  description?: string;
}

export interface User {
  id: number;
  username: string;
  email?: string;
  first_name?: string;
  last_name?: string;
  role: "admin" | "technicien" | "expert" | "operateur"; // ✅ typage fort
  telephone?: string;
  is_active?: boolean;
  activation_token: string;
  date_joined?: string;
  temporary_password?: string;

  // ✅ FK vers Categorie
  categorie?: number | null;

  // ✅ détail enrichi exposé par le serializer
  categorie_detail?: Categorie;

  // ✅ champ exposé par le serializer
  must_change_password: boolean;
}
