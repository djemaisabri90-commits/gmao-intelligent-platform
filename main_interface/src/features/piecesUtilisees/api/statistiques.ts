// features/piecesUtilisees/api/statistiques.ts

import { apiClient } from "@/api/client";
import type { PieceUtiliseeStatistiques } from "../types/statistiques";

export const getPieceStatistiques = async () => {
  const response = await apiClient.get<PieceUtiliseeStatistiques>(
    "/pieces-utilisees/statistiques/"
  );

  return response.data;
};