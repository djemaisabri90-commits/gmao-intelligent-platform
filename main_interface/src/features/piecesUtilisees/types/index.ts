// src/features/piecesUtilisees/types/index.ts

export interface PieceUtilisee {
  id: number;
  intervention: number;   // FK vers Intervention
  piece: number;          // FK vers Piece
  piece_nom: string;      // exposé par le serializer
  piece_reference: string;// exposé par le serializer
  quantite: number;
}

// 🔹 Création (pas d'id)
export type PieceUtiliseeCreate = Omit<PieceUtilisee, 'id' | 'piece_nom' | 'piece_reference'>;

// 🔹 Mise à jour (quantité modifiable)
export type PieceUtiliseeUpdate = Partial<Omit<PieceUtilisee, 'id' | 'piece_nom' | 'piece_reference'>>;
