import React, { useState, useEffect } from "react";
import MapDashboard from "./MapDashboard.js";
import IncidentList from "./IncidentList.js";
import Assistant from "./Assistant.js";
import AuthForm from "./AuthForm.js";
import { get } from "./api.js";

export default function App(){
  const [token, setToken] = useState("");
  const [incidents, setIncidents] = useState([]);

  useEffect(() => {
    if(!token) return;
    (async () => {
      const inc = await get("/incidents", token).catch(_=>[]);
      setIncidents(inc || []);
    })();
  }, [token]);

  return (
    <div className="page">
      <header className="header">
        <h1>Illegal Deforestation Tracker</h1>
        <AuthForm onLogin={t=>setToken(t)} />
      </header>

      <main className="main-grid">
        <section className="map-section">
          <MapDashboard incidents={incidents} />
        </section>
        <aside className="sidebar">
          <IncidentList incidents={incidents} />
          <Assistant token={token} />
        </aside>
      </main>

      <footer className="footer">Prototype — replace synthetic data with real NDVI for publication.</footer>
    </div>
  );
}
