"use client";

import { useMemo, useState } from "react";
import { apiFetch, API_BASE_URL, loginManager } from "../lib/api";

export default function Page() {
  const [email, setEmail] = useState("mgr@example.com");
  const [password, setPassword] = useState("123456");
  const [token, setToken] = useState("");
  const [employees, setEmployees] = useState([]);
  const [employeeId, setEmployeeId] = useState("");
  const [courseId, setCourseId] = useState("1");
  const [assignInfo, setAssignInfo] = useState("");
  const [error, setError] = useState("");

  const authHeaders = useMemo(() => ({ Authorization: `Bearer ${token}` }), [token]);

  async function onLogin(e) {
    e.preventDefault();
    setError("");
    try {
      const data = await loginManager(email, password);
      setToken(data.access_token);
    } catch (e2) {
      setError(String(e2.message || e2));
    }
  }

  async function loadEmployees() {
    setError("");
    try {
      const data = await apiFetch("/manager/employees", { headers: authHeaders });
      setEmployees(data);
      if (data[0]) setEmployeeId(String(data[0].id));
    } catch (e2) {
      setError(String(e2.message || e2));
    }
  }

  async function assignCourse(e) {
    e.preventDefault();
    setError("");
    setAssignInfo("");
    try {
      const data = await apiFetch("/manager/assign", {
        method: "POST",
        headers: authHeaders,
        body: JSON.stringify({ user_id: Number(employeeId), course_id: Number(courseId) }),
      });
      setAssignInfo(JSON.stringify(data));
    } catch (e2) {
      setError(String(e2.message || e2));
    }
  }

  return (
    <main className="container">
      <h1>HR Manager Web</h1>
      <p>API: {API_BASE_URL}</p>

      <section className="card">
        <h3>1) Manager login</h3>
        <form className="row" onSubmit={onLogin}>
          <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="email" />
          <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" placeholder="password" />
          <button type="submit">Login</button>
        </form>
        {token ? <p className="ok">Logged in</p> : null}
      </section>

      <section className="card">
        <h3>2) Employees</h3>
        <button onClick={loadEmployees} disabled={!token}>Load employees</button>
        <ul>
          {employees.map((u) => (
            <li key={u.id}>{u.id}: {u.name} ({u.email})</li>
          ))}
        </ul>
      </section>

      <section className="card">
        <h3>3) Assign course</h3>
        <form className="row" onSubmit={assignCourse}>
          <input value={employeeId} onChange={(e) => setEmployeeId(e.target.value)} placeholder="employee id" />
          <input value={courseId} onChange={(e) => setCourseId(e.target.value)} placeholder="course id" />
          <button type="submit" disabled={!token}>Assign</button>
        </form>
        {assignInfo ? <p className="ok">{assignInfo}</p> : null}
      </section>

      {error ? <p className="error">{error}</p> : null}
    </main>
  );
}
