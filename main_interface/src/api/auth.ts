//src/api/auth.ts
//export des constantes pour une meilleure maintenabilité
export const TOKEN_KEY = '<access_token>';
export const REFRESH_KEY = 'refresh_token';

export const getAccessToken = () => localStorage.getItem(TOKEN_KEY);
export const getRefreshToken = () => localStorage.getItem(REFRESH_KEY);
export const setTokens = (access: string, refresh: string) => {
  localStorage.setItem(TOKEN_KEY, access);
  localStorage.setItem(REFRESH_KEY, refresh);
};
export const clearTokens = () => {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(REFRESH_KEY);
};

/**
 * exporter les clés:
 * ce qui peut être utile si je dois les utiliser ailleurs,
 * par exemple dans un intercepteur Axios:
 * pour lire le refresh token.
 * Mais le code actuel fonctionne parfaitement.
 */