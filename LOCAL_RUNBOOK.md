# LOCAL RUNBOOK: backend + all clients

Ниже — пошаговая инструкция, как локально поднять backend и подключить 3 клиента к одному API.

---

## 0.1) Рекомендуемый формат для учебного показа
Чтобы не распыляться по разным стекам, поднимай сначала **только backend + web (`hrrepozik`)**. Этого достаточно, чтобы показать рабочую интеграцию с БД, авторизацию и бизнес-логику. Mobile/desktop подключай как дополнительный бонус.

## 0) Что должно быть установлено

```bash
python3 --version
pip --version
git --version
```

Рекомендуется Python 3.10+.

---

## 1) Клонирование и переход в проект

```bash
git clone <YOUR_REPO_URL> kai-2
cd kai-2
```

---

## 2) Поднять backend (FastAPI + SQLite)

### 2.1 Создать виртуальное окружение

Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2.2 Установить зависимости

```bash
pip install -r requirements.txt
```

### 2.3 Запустить backend

```bash
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Проверка:
- API root: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`

> ВАЖНО: backend должен работать в отдельном терминале постоянно.

---

## 3) Проверить backend вручную (быстрый smoke test)

Открой второй терминал (backend не выключать):

### 3.1 Регистрация пользователей (employee/manager/admin)

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Emp One","email":"emp@example.com","password":"123456","role":"employee","department":"sales"}'

curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Mgr One","email":"mgr@example.com","password":"123456","role":"manager","department":"sales"}'

curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Admin One","email":"admin@example.com","password":"123456","role":"admin","department":"hq"}'
```

### 3.2 Получить JWT токены

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=emp@example.com&password=123456"

curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=mgr@example.com&password=123456"

curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=123456"
```

Скопируй `access_token` каждого пользователя.

---

## 4) Подключение клиентов к backend

Все клиенты должны использовать один base URL:

```text
http://127.0.0.1:8000
```

### 4.1 Web клиент `hrrepozik` (роль manager)

1. Открой проект web-клиента.
2. Найди конфиг API (обычно `.env`, `config.ts`, `axios.ts`, `api.ts`).
3. Установи:

```env
API_BASE_URL=http://127.0.0.1:8000
```

4. Используй manager endpoints:
- `POST /auth/login`
- `POST /manager/assign`
- `GET /manager/employee_courses/{user_id}`
- `GET /library/sync`

### 4.2 Mobile клиент `hrrepozik-modile-2` (роль admin)

1. Открой проект mobile-клиента.
2. Найди API base URL (обычно `constants.ts`, `env`, `build config`).
3. Установи:

```text
http://127.0.0.1:8000
```

4. Используй только admin endpoints:
- `GET /admin/stats`
- `GET /admin/stats/{department}`

> Mobile не должен показывать детальные данные по конкретным сотрудникам.

### 4.3 Desktop клиент `repozik-desktop2` (роль employee)

1. Открой проект desktop-клиента.
2. Найди файл, где задан API URL.
3. Установи:

```text
http://127.0.0.1:8000
```

4. Используй employee endpoints:
- `POST /auth/register`
- `POST /auth/login`
- `GET /employee/my_courses`
- `GET /employee/my_courses/{course_id}`
- `GET /employee/my_courses/{course_id}/progress`
- `PATCH /employee/my_courses/{course_id}/progress`
- `GET /employee/my_courses/{course_id}/test`
- `GET /library/sync`

---

## 5) Порядок запуска всех приложений

1. Терминал #1: backend
```bash
source .venv/bin/activate
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

2. Терминал #2: web client
```bash
cd hrrepozik
# далее команда запуска вашего web-проекта, например:
# npm install
# npm run dev
```

3. Терминал #3: mobile client
```bash
cd hrrepozik-modile-2
# далее команда запуска вашего mobile-проекта, например:
# npm install
# npm run start
```

4. Терминал #4: desktop client
```bash
cd repozik-desktop2
# далее команда запуска вашего desktop-проекта, например:
# npm install
# npm run desktop
```

---

## 6) Проверка, что клиенты реально связаны с backend

- В desktop зарегистрируй сотрудника → в backend БД появится пользователь.
- В web под manager назначь курс сотруднику → в desktop у сотрудника курс появится в «в процессе».
- В mobile под admin проверь, что видна агрегированная статистика, а не карточка каждого пользователя.

---

## 7) Частые проблемы

### Порт занят
```bash
lsof -i :8000
# завершить процесс и перезапустить backend
```

### Неправильный base URL
Проверь, что в каждом клиенте стоит именно:
```text
http://127.0.0.1:8000
```

#### Ошибка `Can't resolve 'tailwindcss' in 'C:\projects\kai 2'`
Причина: web запускается из корня репозитория, а не из `hrrepozik`, либо в `hrrepozik` не установлены npm-зависимости.

Исправление:
```bash
cd hrrepozik
npm install
npm install -D tailwindcss postcss autoprefixer
npm run dev
```

Нельзя запускать `npm run dev` из корня `kai-2`.

Если ошибка остаётся даже при запуске из `hrrepozik`, зафиксируй корень Turbopack в `hrrepozik/next.config.ts` (или `next.config.js`):
```ts
import path from "node:path";

const nextConfig = {
  turbopack: {
    root: path.resolve(__dirname),
  },
};

export default nextConfig;
```
После этого перезапусти `npm run dev` в `hrrepozik`.

### 401 Unauthorized
- Проверь, что передаёшь JWT в заголовке:
```text
Authorization: Bearer <token>
```
- Проверь, что логинишься пользователем правильной роли.

---

## 8) Полезные ссылки

- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`
