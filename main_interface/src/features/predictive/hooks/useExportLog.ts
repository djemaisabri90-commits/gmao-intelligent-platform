// src/features/predictive/hooks/useExportLog.ts
import { exportLog } from "../api/predictiveApi";
import { useMutation } from "@tanstack/react-query";
import { toast } from "react-toastify";
/*
type ExportFormat = "csv" | "json";

const triggerDownload = (data: any, version: number, format: ExportFormat) => {
  const mimeType = format === "csv" ? "text/csv" : "application/json";

  // ✅ Corriger JSON → stringifier avant de créer le Blob
  const content = format === "json" ? JSON.stringify(data, null, 2) : data;

  const blob = new Blob([content], { type: mimeType });
  const url = window.URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;
  link.download = `log_v${version}.${format}`;
  link.click();

  window.URL.revokeObjectURL(url); // nettoyage mémoire
};

export const useExportLog = () => {
  return useMutation({
    mutationFn: async ({ version, format }: { version: number; format: ExportFormat }) =>
      exportLog(version, format), // backend renvoie Blob ou JSON
    onSuccess: (data, variables) => {
      triggerDownload(data, variables.version, variables.format);
      toast.success(`✅ Log v${variables.version} exporté en ${variables.format.toUpperCase()}`);
    },
    onError: (error: unknown) => {
      const message = error instanceof Error ? error.message : "Erreur inconnue";
      toast.error(`❌ Erreur export: ${message}`);
    },
  });
};
*/

type ExportFormat = "csv" | "json" | "xlsx";

const triggerDownload = (data: any, version: number, format: ExportFormat) => {
  let mimeType: string;
  let content: BlobPart;

  switch (format) {
    case "csv":
      mimeType = "text/csv";
      content = data;
      break;
    case "json":
      mimeType = "application/json";
      content = JSON.stringify(data, null, 2); // ✅ stringifier JSON
      break;
    case "xlsx":
      mimeType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
      content = data; // ✅ backend doit renvoyer un Blob
      break;
    default:
      throw new Error("Format non supporté");
  }

  const blob = new Blob([content], { type: mimeType });
  const url = window.URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;
  link.download = `log_v${version}.${format}`;
  link.click();

  window.URL.revokeObjectURL(url); // nettoyage mémoire
};

export const useExportLog = () => {
  return useMutation({
    mutationFn: async ({ version, format }: { version: number; format: ExportFormat }) =>
      exportLog(version, format), // backend renvoie Blob ou JSON
    onSuccess: (data, variables) => {
      triggerDownload(data, variables.version, variables.format);
      toast.success(`✅ Log v${variables.version} exporté en ${variables.format.toUpperCase()}`);
    },
    onError: (error: unknown) => {
      const message = error instanceof Error ? error.message : "Erreur inconnue";
      toast.error(`❌ Erreur export: ${message}`);
    },
  });
};
