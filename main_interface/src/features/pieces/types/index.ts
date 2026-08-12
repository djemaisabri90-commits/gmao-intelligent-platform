// src/features/pieces/types/index.ts

export interface Piece {
  id: number;
  nom: string;
  reference: string;
  stock_disponible: number;
  fournisseur: string;
  prix_unitaire: string;
}

// 🔹 Type pour la création (pas d'id)
export type PieceCreate = Omit<Piece, 'id'>;

// 🔹 Type pour la mise à jour (tous les champs optionnels)
export type PieceUpdate = Partial<Omit<Piece, 'id'>>;
