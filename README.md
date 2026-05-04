# Локальная HR-система (web + mobile + desktop)

## Архитектура
- `hrrepozik` (web, менеджеры): назначение курсов, обзор по курсам без персонального прогресса.
- `hrrepozik-modile-2` (mobile, администраторы): только агрегированная статистика (`/admin/stats`, `/admin/stats/{department}`).
- `repozik-desktop2` (desktop, сотрудники): регистрация, мои курсы, прогресс, тест после завершения.
- `backend/app` — единый локальный API + SQLite (`hr_local.db`) для синхронизации между всеми клиентами.

## Проверка требований
1. Сущности `User`, `Course`, `Lesson`, `Progress`, `Test`, `CourseAssignment` связаны через FK/relationship.
2. Сотрудник получает только `my_courses`, тест — только при `status=completed`.
3. Менеджер может назначать курс (`/manager/assign`) и видеть только количество назначений (`/manager/employee_courses/{user_id}`), без прогресса каждого сотрудника.
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

## Частая ошибка web-клиента (`tailwindcss`)
Если видишь ошибку:
`Error: Can't resolve 'tailwindcss' in 'C:\projects\kai 2'`

Сделай так (Windows PowerShell):
```powershell
cd "C:\projects\kai 2\hrrepozik"
npm install
npm install -D tailwindcss postcss autoprefixer
npm run dev
```

Важно:
- не запускай `npm run dev` из `C:\projects\kai 2`;
- запускать нужно из папки `hrrepozik`, где лежит `package.json` web-клиента.


### Если ошибка остаётся даже внутри `hrrepozik`
Для Next.js 16 + Turbopack в монорепозитории резолв `tailwindcss` иногда идёт от корня (`C:\\projects\\kai 2`).
Поэтому установи shared dev-зависимости в корне проекта:
```powershell
cd "C:\\projects\\kai 2"
npm install
```
После этого снова:
```powershell
cd "C:\\projects\\kai 2\\hrrepozik"
npm run dev
```


## Рекомендуемый единый стек (для учебного демо)
Чтобы не путаться, используем один понятный стек:
- **Backend**: FastAPI + SQLite (`backend/app`).
- **Frontend**: Next.js 16 (`hrrepozik`).

Mobile/desktop клиенты оставляем опциональными. Для защиты проекта преподавателю достаточно связки backend + web, где видно авторизацию, назначение курсов и данные из БД.

### Быстрый запуск (2 терминала)
Терминал #1 (backend):
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Терминал #2 (web):
```bash
cd hrrepozik
npm install
npm run dev
```

Web: `http://localhost:3000`
API: `http://127.0.0.1:8000`
