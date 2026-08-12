// src/features/predictive/components/MachineMap.tsx
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import type { LatLngExpression } from "leaflet"; 
import type { MachineFeatures } from "../types";

const getMarkerIcon = (risk: number) => {
  return L.icon({
    iconUrl:
      risk === 1
        ? "/icons/marker-red.png"   // ⚠️ risque élevé
        : "/icons/marker-green.png", // ✅ normal
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
  });
};

interface Props {
  machines: MachineFeatures[];
}

export const MachineMap = ({ machines }: Props) => {
  const center: LatLngExpression = [36.8188, 10.1658]; // Tunis

  return (
    <MapContainer center={center} zoom={12} className="h-96 w-full rounded-lg shadow-md">
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {machines.map(m =>
        m.latitude && m.longitude ? (
          <Marker
            key={m.machine_id}
            position={[m.latitude, m.longitude]}
            icon={getMarkerIcon(m.target)}
          >
            <Popup>
              <strong>Machine {m.machine_id}</strong><br />
              Interventions: {m.total_interventions}<br />
              Risque: {m.target === 1 ? "⚠️ Critique" : "✅ Normal"}
            </Popup>
          </Marker>
        ) : null
      )}
    </MapContainer>
  );
};
