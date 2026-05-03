# Client -> Local Backend Integration (default config in client code)

Цель: клиенты должны быть привязаны к локальному backend по умолчанию.

Base URL по умолчанию в коде каждого клиента:
- `http://127.0.0.1:8000`

## Web (`hrrepozik`, manager role)
В коде web-клиента должен быть дефолт:
- `API_BASE_URL = "http://127.0.0.1:8000"`

Используемые endpoints:
- `POST /auth/login`
- `POST /manager/assign`
- `GET /manager/employee_courses/{user_id}`
- `GET /library/sync`

## Mobile (`hrrepozik-modile-2`, admin role)
В коде mobile-клиента должен быть дефолт:
- `API_BASE_URL = "http://127.0.0.1:8000"`

Используемые endpoints:
- `GET /admin/stats`
- `GET /admin/stats/{department}`

## Desktop (`repozik-desktop2`, employee role)
В коде desktop-клиента должен быть дефолт:
- `API_BASE_URL = "http://127.0.0.1:8000"`

Используемые endpoints:
- `POST /auth/register`
- `POST /auth/login`
- `GET /employee/my_courses`
- `GET /employee/my_courses/{course_id}`
- `GET /employee/my_courses/{course_id}/progress`
- `PATCH /employee/my_courses/{course_id}/progress`
- `GET /employee/my_courses/{course_id}/test`
- `GET /library/sync`


## Current repo defaults
- `hrrepozik/.env`
- `hrrepozik-modile-2/.env`
- `repozik-desktop2/.env`

Each already contains `API_BASE_URL=http://127.0.0.1:8000`.
