import { useState, useEffect, useCallback } from "react";
import { api } from "./api";
import type { Order } from "./types";
import { OrdersTable } from "./components/OrdersTable";
import { OrderForm } from "./components/OrderForm";

function App() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchOrders = useCallback(async () => {
    setIsLoading(true);
    try {
      const { data } = await api.getOrders();
      if (data) setOrders(data);
    } catch (err) {
      console.error(err);
    } finally {
      setTimeout(() => setIsLoading(false), 500); 
    }
  }, []);

  useEffect(() => {
    fetchOrders();
  }, [fetchOrders]);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    try {
      await api.uploadCsv(file);
      fetchOrders();
    } catch {
      alert("Upload failed");
    }
  };

  return (
    <div className="container">
      <header className="app-header">
        <h1 className="app-header__title">BetterMe Tax Dashboard</h1>
        <div className="app-header__actions">
          <input
            type="file"
            onChange={handleFileUpload}
            accept=".csv"
            id="csv-upload"
            style={{ display: "none" }}
          />
          <label
            htmlFor="csv-upload"
            className="btn"
            title="Upload a CSV file with orders to process taxes automatically"
          >
            Import CSV
          </label>
        </div>
      </header>

      <OrderForm onOrderCreated={() => void fetchOrders()} />

      <section className="card">
        <h3 className="card__title">Processed Orders List</h3>
        <OrdersTable orders={orders} isLoading={isLoading} />
      </section>
    </div>
  );
}

export default App;
