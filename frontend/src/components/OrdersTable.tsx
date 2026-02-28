import type { Order } from "../types";
import { SkeletonRow } from "./SkeletonRow";

interface Props {
  orders: Order[];
  isLoading: boolean;
}

export const OrdersTable = ({ orders, isLoading }: Props) => (
  <div className="table-wrapper">
    <table className="orders-table">
      <thead className="orders-table__header">
        <tr>
          <th className="orders-table__cell">ID</th>
          <th className="orders-table__cell">Coordinates</th>
          <th className="orders-table__cell">Subtotal</th>
          <th className="orders-table__cell">Tax Rate</th>
          <th className="orders-table__cell">Tax Amount</th>
          <th className="orders-table__cell">Total</th>
          <th className="orders-table__cell">Breakdown</th>
        </tr>
      </thead>
      <tbody>
        {isLoading
          ? // Показуємо 5 скелетонів під час завантаження
            [...Array(5)].map((_, i) => <SkeletonRow key={i} />)
          : orders.map((o) => (
              <tr key={o.id} className="orders-table__row">
                <td className="orders-table__cell">{o.id}</td>
                <td className="orders-table__cell">
                  {o.latitude.toFixed(3)}, {o.longitude.toFixed(3)}
                </td>
                <td className="orders-table__cell">${o.subtotal.toFixed(2)}</td>
                <td className="orders-table__cell">
                  {((o.composite_tax_rate ?? 0) * 100).toFixed(2)}%
                </td>
                <td className="orders-table__cell">
                  ${o.tax_amount?.toFixed(2)}
                </td>
                <td className="orders-table__cell">
                  <strong>${o.total_amount?.toFixed(2)}</strong>
                </td>
                <td className="orders-table__cell">
                  <small title={o.breakdown?.jurisdictions.join(", ")}>
                    {o.breakdown?.state_rate} / {o.breakdown?.county_rate} /
                    {o.breakdown?.city_rate} / {o.breakdown?.special_rates}
                  </small>
                </td>
              </tr>
            ))}
      </tbody>
    </table>
  </div>
);
