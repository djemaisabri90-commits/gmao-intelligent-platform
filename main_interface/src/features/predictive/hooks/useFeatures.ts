// src/features/predictive/hooks/useFeature.ts
import { featureData } from "../api/predictiveApi";
import type { MachineFeatures} from "../types";
import { useQuery } from "@tanstack/react-query";

export const useFeature = () => {
  return useQuery<MachineFeatures[]>({
    queryKey: ["featuresDataset"],
    queryFn: featureData,
  });
 
};
