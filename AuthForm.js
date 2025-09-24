import React, { useState } from "react";
import API from "./api";

export default function AuthForm({onLogin}){
  const [user, setUser] = useState({username:"admin", password:"adminpass", full_name:"Administrator"});

  const login = async () => {
    const res = await fetch(`/api/token`, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(user)});
    const j = await res.json();
    if(j.access_token){ onLogin(j.access_token); }
    else alert("Login error");
  };
  const register = async () => {
    const res = await fetch(`/api/register`, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(user)});
    const j = await res.json();
    if(j.access_token){ onLogin(j.access_token); }
    else alert("Register error");
  };

  return (
    <div className="auth">
      <input value={user.username} onChange={e=>setUser({...user, username:e.target.value})} placeholder="username" />
      <input value={user.password} onChange={e=>setUser({...user, password:e.target.value})} placeholder="password" type="password" />
      <button onClick={login}>Login</button>
      <button onClick={register}>Register</button>
    </div>
  );
}
