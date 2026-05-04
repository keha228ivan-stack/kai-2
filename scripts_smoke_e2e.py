#!/usr/bin/env python3
import os
import sys
import requests

BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
TIMEOUT = 10


def req(method: str, path: str, **kwargs):
    r = requests.request(method, f"{BASE_URL}{path}", timeout=TIMEOUT, **kwargs)
    return r


def ensure_user(name, email, password, role, department):
    r = req("POST", "/auth/register", json={
        "name": name,
        "email": email,
        "password": password,
        "role": role,
        "department": department,
    })
    if r.status_code not in (200, 400):
        raise RuntimeError(f"register {email} failed: {r.status_code} {r.text}")


def login(email, password):
    r = req("POST", "/auth/login", data={"username": email, "password": password})
    if r.status_code != 200:
        raise RuntimeError(f"login {email} failed: {r.status_code} {r.text}")
    return r.json()["access_token"]


def auth(token):
    return {"Authorization": f"Bearer {token}"}


def main():
    print(f"[info] using API_BASE_URL={BASE_URL}")

    # 1) users
    ensure_user("Emp One", "emp@example.com", "123456", "employee", "sales")
    ensure_user("Mgr One", "mgr@example.com", "123456", "manager", "sales")
    ensure_user("Admin One", "admin@example.com", "123456", "admin", "hq")

    emp_t = login("emp@example.com", "123456")
    mgr_t = login("mgr@example.com", "123456")
    adm_t = login("admin@example.com", "123456")

    # 2) manager sees employees
    r = req("GET", "/manager/employees", headers=auth(mgr_t))
    if r.status_code != 200:
        raise RuntimeError(f"manager/employees failed: {r.status_code} {r.text}")
    employees = r.json()
    emp = next((u for u in employees if u["email"] == "emp@example.com"), None)
    if not emp:
        raise RuntimeError("employee not visible for manager")

    # 3) assign seeded course #1
    r = req("POST", "/manager/assign", headers=auth(mgr_t), json={"user_id": emp["id"], "course_id": 1})
    if r.status_code != 200:
        raise RuntimeError(f"manager/assign failed: {r.status_code} {r.text}")

    # 4) employee sees course and updates progress
    r = req("GET", "/employee/my_courses", headers=auth(emp_t))
    if r.status_code != 200:
        raise RuntimeError(f"employee/my_courses failed: {r.status_code} {r.text}")
    if not isinstance(r.json(), list):
        raise RuntimeError("employee/my_courses returned non-list")

    r = req("PATCH", "/employee/my_courses/1/progress", headers=auth(emp_t), json={"completion_percentage": 100})
    if r.status_code != 200:
        raise RuntimeError(f"progress update failed: {r.status_code} {r.text}")

    r = req("GET", "/employee/my_courses/1/test", headers=auth(emp_t))
    if r.status_code != 200:
        raise RuntimeError(f"employee test fetch failed: {r.status_code} {r.text}")

    # 5) admin stats
    r = req("GET", "/admin/stats", headers=auth(adm_t))
    if r.status_code != 200:
        raise RuntimeError(f"admin stats failed: {r.status_code} {r.text}")

    print("[ok] end-to-end flow is healthy")
    print("[ok] manager -> employee visibility works")
    print("[ok] assignment -> progress -> test flow works")
    print("[ok] admin stats available")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[fail] {e}")
        sys.exit(1)
