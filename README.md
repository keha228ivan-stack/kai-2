# Локальная HR-система (web + mobile + desktop)

## Архитектура
- `hrrepozik` (web, менеджеры): назначение курсов, обзор по курсам без персонального прогресса.
- `hrrepozik-modile-2` (mobile, администраторы): только агрегированная статистика (`/admin/stats`, `/admin/stats/{department}`).
- `repozik-desktop2` (desktop, сотрудники): регистрация, мои курсы, прогресс, тест после завершения.
- `backend/app` — единый локальный API + SQLite (`hr_local.db`) для синхронизации между всеми клиентами.

## Проверка требований
1. Сущности `User`, `Course`, `Lesson`, `Progress`, `Test`, `CourseAssignment` связаны через FK/relationship.
2. Сотрудник получает только `my_courses`, тест — только при `status=completed`.
3. Менеджер может назначать курс (`/manager/assign`) и видеть только количество назначений (`/manager/employee_courses/{user_id}`).
4. Администратор получает только агрегаты по системе и отделам.
5. Назначение курса создаётся только в `course_assignments` со статусом `in-progress` (это «Курсы в процессе», а не библиотека).
6. Библиотека курсов синхронизируется через `/library/sync` для web/desktop; mobile endpoint не использует.

## Запуск локально
```bash
pip install -r requirements.txt
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`

## Примечания по синхронизации
- При регистрации сотрудника запись сразу попадает в общую БД SQLite и видна web/mobile клиентам согласно ролям.
- Для near real-time можно добавить SSE/WebSocket слой поверх текущего REST API.
