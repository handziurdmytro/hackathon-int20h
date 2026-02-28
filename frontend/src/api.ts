import axios from 'axios';
import type {Order} from './types';

const API_URL = '';

export const api = {
  uploadCsv: (file: File) => {
    const formData = new FormData();
    formData.append('csv_file', file); // Ключ має бути 'csv_file' як у main.py
    return axios.post(`${API_URL}/orders/import`, formData);
  },

  getOrders: () => axios.get<Order[]>(`${API_URL}/orders`),

  createOrder: (data: { latitude: number; longitude: number; subtotal: number }) => {
    // Створюємо об'єкт, що відповідає Pydantic моделі Order
    const payload = {
      ...data,
    };
    return axios.post(`${API_URL}/orders`, payload);
  },
};