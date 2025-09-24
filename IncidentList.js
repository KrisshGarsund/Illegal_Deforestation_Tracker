import React from "react";

export default function IncidentList({incidents}){
  return (
    <div className="incident-list">
      <h2>Detected Incidents</h2>
      {incidents.length === 0 ? <p>No incidents</p> : (
        <ul>{incidents.map(i => (
          <li key={i.case_id}>
            <strong>{i.case_id}</strong><br/>
            Severity: {i.severity} — Centroid: {i.centroid[0].toFixed(3)}, {i.centroid[1].toFixed(3)}
          </li>
        ))}</ul>
      )}
    </div>
  );
}
