import React from "react";
import InventoryTable from "./components/InventoryTable";

const App: React.FC = () => {
  return (
    <div>
      <header style={{padding: "1rem", borderBottom: "1px solid #ddd"}}>
        <h1>Asset Control Engine</h1>
      </header>
      <main style={{padding: "1rem"}}>
        <InventoryTable />
      </main>
    </div>
  );
};

export default App;
