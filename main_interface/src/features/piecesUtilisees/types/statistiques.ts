// features/piecesUtilisees/types/statistiques.ts

export interface PieceUtiliseeStatistiques {
  pieces_consommees: number;
  cout_total_pieces: number;

  cout_moyen_intervention: number;

  intervention_plus_couteuse?: {
    intervention_id: number;
    cout_total: number;
  };

  intervention_moins_couteuse?: {
    intervention_id: number;
    cout_total: number;
  };

  cout_par_intervention: {
    intervention_id: number;
    cout_total: number;
  }[];
}