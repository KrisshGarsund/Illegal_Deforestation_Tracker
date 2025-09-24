import React, { useEffect, useRef } from "react";

export default function MapDashboard({incidents}){
  const ref = useRef(null);
  useEffect(()=>{
    if(!window.google || !ref.current) return;
    const map = new window.google.maps.Map(ref.current, {
      center: {lat: 20.5, lng: 78.9},
      zoom: 5
    });
    // draw incidents
    incidents.forEach(inc => {
      const [lat, lng] = inc.centroid || [inc.lat, inc.lng];
      const marker = new window.google.maps.Marker({
        position: {lat, lng},
        map,
        title: `${inc.case_id || "Case"} — Severity ${inc.severity}`
      });
      const inf = new window.google.maps.InfoWindow({
        content: `<div><strong>${inc.case_id || "Case"}</strong><br/>Severity: ${inc.severity}<br/>Score: ${inc.score || "-"}</div>`
      });
      marker.addListener("click", ()=>inf.open(map, marker));
    });
  }, [incidents]);

  return <div ref={ref} style={{height: "600px", width: "100%", borderRadius: 6, boxShadow: "0 1px 6px rgba(0,0,0,0.1)"}} />;
}
