import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000",
  timeout: 12000,
});

export const fetchProducts = async (limit = 20) => {
  const { data } = await api.get(`/products?limit=${limit}`);
  return Array.isArray(data) ? data : [];
};

export const fetchSimilar = async (productId) => {
  const { data } = await api.get(`/similar/${encodeURIComponent(productId)}`);
  // Ensure we never echo the same product back as “similar”
  return (Array.isArray(data) ? data : []).filter(p => p.PRODUCT_ID !== productId);
};

export default api;
