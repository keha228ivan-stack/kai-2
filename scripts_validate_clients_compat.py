#!/usr/bin/env python3
import os
import sys
from pathlib import Path

import requests

BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

REQUIRED = {
    "web": [
        ("post", "/auth/login"),
        ("post", "/manager/assign"),
        ("get", "/manager/employee_courses/{user_id}"),
        ("get", "/manager/employees"),
        ("get", "/library/sync"),
    ],
    "mobile": [
        ("get", "/admin/stats"),
        ("get", "/admin/stats/{department}"),
    ],
    "desktop": [
        ("post", "/auth/register"),
        ("post", "/auth/login"),
        ("get", "/employee/my_courses"),
        ("get", "/employee/my_courses/{course_id}"),
        ("get", "/employee/my_courses/{course_id}/progress"),
        ("patch", "/employee/my_courses/{course_id}/progress"),
        ("get", "/employee/my_courses/{course_id}/test"),
        ("get", "/library/sync"),
    ],
}

CLIENT_ENVS = {
    "web": Path("hrrepozik/.env"),
    "mobile": Path("hrrepozik-modile-2/.env"),
    "desktop": Path("repozik-desktop2/.env"),
}


def read_base_url(path: Path) -> str:
    if not path.exists():
        return ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("API_BASE_URL="):
            return line.split("=", 1)[1].strip()
    return ""


def main() -> int:
    print(f"[info] checking backend compatibility via {BASE_URL}/openapi.json")
    try:
        resp = requests.get(f"{BASE_URL}/openapi.json", timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"[fail] cannot load OpenAPI: {e}")
        return 1

    spec = resp.json()
    paths = spec.get("paths", {})

    ok = True

    for client, reqs in REQUIRED.items():
        print(f"\n[check] {client}")
        env_url = read_base_url(CLIENT_ENVS[client])
        if env_url != "http://127.0.0.1:8000":
            ok = False
            print(f"  [fail] {CLIENT_ENVS[client]} has API_BASE_URL={env_url!r}, expected 'http://127.0.0.1:8000'")
        else:
            print(f"  [ok] base URL from {CLIENT_ENVS[client]} is correct")

        for method, path in reqs:
            exists = path in paths and method in paths[path]
            if not exists:
                ok = False
                print(f"  [fail] missing in backend spec: {method.upper()} {path}")
            else:
                print(f"  [ok] {method.upper()} {path}")

    print("\n[result] " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
