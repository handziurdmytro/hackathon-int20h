export const SkeletonRow = () => (
  <tr className="orders-table__row">
    <td className="orders-table__cell"><span className="skeleton" style={{ width: '30px', height: '20px' }}></span></td>
    <td className="orders-table__cell"><span className="skeleton" style={{ width: '120px', height: '20px' }}></span></td>
    <td className="orders-table__cell"><span className="skeleton" style={{ width: '60px', height: '20px' }}></span></td>
    <td className="orders-table__cell"><span className="skeleton" style={{ width: '50px', height: '20px' }}></span></td>
    <td className="orders-table__cell"><span className="skeleton" style={{ width: '80px', height: '20px' }}></span></td>
    <td className="orders-table__cell"><span className="skeleton" style={{ width: '70px', height: '20px' }}></span></td>
    <td className="orders-table__cell"><span className="skeleton" style={{ width: '100px', height: '20px' }}></span></td>
  </tr>
);