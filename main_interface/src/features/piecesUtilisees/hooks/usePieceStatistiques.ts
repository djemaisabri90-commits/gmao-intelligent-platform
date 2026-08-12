// features/piecesUtilisees/hooks/usePieceStatistiques.ts

import { useQuery } from "@tanstack/react-query";
import { getPieceStatistiques } from "../api/statistiques";

export const usePieceStatistiques = () => {
  return useQuery({
    queryKey: ["piece-statistiques"],
    queryFn: getPieceStatistiques,
  });
};