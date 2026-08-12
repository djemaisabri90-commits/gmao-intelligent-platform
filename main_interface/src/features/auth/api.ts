import api from "@/api/axios";

export const login = async (data: { username: string; password: string }) => {
  const res = await api.post("login/", data);
  return res.data;
};