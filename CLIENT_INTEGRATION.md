# Client ↔ Backend integration contract (single stack)

Этот репозиторий сейчас содержит backend и конфиги клиентов (`.env`), но **не содержит исходный код UI клиентов** (`hrrepozik`, `hrrepozik-modile-2`, `repozik-desktop2`).

Поэтому в рамках этого репозитория фиксируется единый API-контракт и автоматическая проверка совместимости клиентов с backend.

## Единый base URL
Во всех клиентах:
- `API_BASE_URL=http://127.0.0.1:8000`

Файлы:
- `hrrepozik/.env`
- `hrrepozik-modile-2/.env`
- `repozik-desktop2/.env`

## Роли и endpoints

### Web (`hrrepozik`, manager)
- `POST /auth/login`
- `POST /manager/assign`
- `GET /manager/employees`
- `GET /manager/employee_courses/{user_id}`
- `GET /library/sync`

### Mobile (`hrrepozik-modile-2`, admin)
- `GET /admin/stats`
- `GET /admin/stats/{department}`

### Desktop (`repozik-desktop2`, employee)
- `POST /auth/register`
- `POST /auth/login`
- `GET /employee/my_courses`
- `GET /employee/my_courses/{course_id}`
- `GET /employee/my_courses/{course_id}/progress`
- `PATCH /employee/my_courses/{course_id}/progress`
- `GET /employee/my_courses/{course_id}/test`
- `GET /library/sync`

## Проверка совместимости (автоматически)
1. Запусти backend:
```bash
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```
2. Прогони проверку контракта:
```bash
python scripts_validate_clients_compat.py
```

Скрипт проверит:
- что backend действительно публикует нужные endpoints в `openapi.json`;
- что `.env` клиентов указывают на правильный `API_BASE_URL`;
- что контракт web/mobile/desktop не расходится с backend API.

## Полный smoke поток
```bash
python scripts_smoke_e2e.py
```
Проверяет рабочую бизнес-цепочку: register/login/assign/progress/test/admin stats.
