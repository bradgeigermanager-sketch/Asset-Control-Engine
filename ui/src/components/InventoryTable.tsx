import React, { useEffect, useState } from "react";
import { fetchAssets } from "../services/api";

const InventoryTable: React.FC = () => {
  const [assets, setAssets] = useState<any[]>([]);
  useEffect(() => {
    fetchAssets().then((r) => setAssets(r.items || []));
  }, []);
  return (
    <div>
      <h2>Assets</h2>
      <table style={{width: "100%", borderCollapse: "collapse"}}>
        <thead>
          <tr>
            <th>Tag</th><th>Type</th><th>Hostname</th><th>Owner</th><th>State</th>
          </tr>
        </thead>
        <tbody>
          {assets.map(a => (
            <tr key={a.id}>
              <td>{a.assetTag}</td>
              <td>{a.type}</td>
              <td>{a.hostname}</td>
              <td>{a.owner?.name}</td>
              <td>{a.lifecycleState}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default InventoryTable;
