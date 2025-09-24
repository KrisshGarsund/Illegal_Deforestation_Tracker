// Use relative /api paths so when backend serves frontend both are on same origin.
const API = "/api";

export async function post(path, body, token){
  const headers = {"Content-Type":"application/json"};
  if(token) headers["Authorization"] = `Bearer ${token}`;
  const res = await fetch(`${API}${path}`, {method:"POST", headers, body: JSON.stringify(body)});
  return res.json();
}

export async function get(path, token){
  const headers = {};
  if(token) headers["Authorization"] = `Bearer ${token}`;
  const res = await fetch(`${API}${path}`, {headers});
  return res.json();
}
export default API;
