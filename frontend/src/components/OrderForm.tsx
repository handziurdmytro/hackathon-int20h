import { useState } from "react";
import { api } from "../api";
import "../styles/OrderForm.scss";

interface Props {
  onOrderCreated: () => void;
}

export const OrderForm = ({ onOrderCreated }: Props) => {
  const [formData, setFormData] = useState({
    latitude: 0,
    longitude: 0,
    subtotal: 0,
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.createOrder({
        lat: formData.latitude,
        lon: formData.longitude,
        subtotal: formData.subtotal,
      });
      onOrderCreated();
      alert("Order created!");
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="card order-form">
      <h3 className="order-form__title">Manual Creation</h3>
      <div className="order-form__grid">
        <div className="form-group">
          <label className="form-group__label">Latitude</label>
          <input
            type="number"
            step="any"
            required
            className="form-group__input"
            onChange={(e) =>
              setFormData({ ...formData, latitude: parseFloat(e.target.value) })
            }
            title="Enter GPS latitude within New York State"
          />
        </div>
        <div className="form-group">
          <label className="form-group__label">Longitude</label>
          <input
            type="number"
            step="any"
            required
            className="form-group__input"
            onChange={(e) =>
              setFormData({
                ...formData,
                longitude: parseFloat(e.target.value),
              })
            }
            title="Enter GPS longitude within New York State"
          />
        </div>
        <div className="form-group">
          <label className="form-group__label">Subtotal ($)</label>
          <input
            type="number"
            step="0.01"
            required
            className="form-group__input"
            onChange={(e) =>
              setFormData({ ...formData, subtotal: parseFloat(e.target.value) })
            }
            title="Price of wellness package before tax"
          />
        </div>
      </div>
      <button
        type="submit"
        className="btn order-form__submit"
        title="Click to calculate tax and save order"
      >
        Calculate & Save
      </button>
    </form>
  );
};
