import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const api = {
  uploadCsv: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return axios.post(`${API_URL}/orders/import`, formData);
  },

  getOrders: (page: number = 1) => 
    axios.get(`${API_URL}/orders?page=${page}`),

  createOrder: (data: { lat: number; lon: number; subtotal: number }) =>
    axios.post(`${API_URL}/orders`, data),
};