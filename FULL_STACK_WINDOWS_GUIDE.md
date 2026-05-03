# Полная инструкция запуска (Windows): backend + web + mobile + desktop

## 1) Подготовка
Открой **PowerShell** в корне проекта (`C:\projects\kai 2`).

Проверь инструменты:
```powershell
python --version
pip --version
git --version
```

## 2) Запуск backend

### 2.1 Виртуальное окружение
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2.2 Установка зависимостей
```powershell
pip install -r requirements.txt
```

### 2.3 Старт FastAPI
```powershell
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Проверка:
- `http://127.0.0.1:8000` → должен вернуться JSON `{"status":"ok",...}`
- `http://127.0.0.1:8000/docs` → Swagger

> Backend держим открытым в отдельном окне PowerShell.

## 3) Где прописан адрес backend в клиентах

По умолчанию уже установлено в каждом клиенте:
- `hrrepozik/.env`
- `hrrepozik-modile-2/.env`
- `repozik-desktop2/.env`

Содержимое:
```env
API_BASE_URL=http://127.0.0.1:8000
```

## 4) Запуск WEB клиента (менеджер)

Окно PowerShell №2:
```powershell
cd .\hrrepozik
```

Дальше выбирай команды под твой стек:

### Если React/Vite
```powershell
npm install
npm run dev
```

### Если Next.js
```powershell
npm install
npm run dev
```

После запуска открой локальный URL, который покажет консоль (обычно `http://localhost:5173` или `http://localhost:3000`).

Логинься менеджером и используй:
- `POST /auth/login`
- `POST /manager/assign`
- `GET /manager/employee_courses/{user_id}`

## 5) Запуск MOBILE клиента (админ)

Окно PowerShell №3:
```powershell
cd .\hrrepozik-modile-2
```

### Если React Native + Expo
```powershell
npm install
npm run start
```

### Если Flutter
```powershell
flutter pub get
flutter run
```

Используй только админ-ручки:
- `GET /admin/stats`
- `GET /admin/stats/{department}`

## 6) Запуск DESKTOP клиента (сотрудник)

Окно PowerShell №4:
```powershell
cd .\repozik-desktop2
```

### Если Electron
```powershell
npm install
npm run desktop
```
или
```powershell
npm run start
```

Используй employee-ручки:
- `POST /auth/register`
- `POST /auth/login`
- `GET /employee/my_courses`
- `GET /employee/my_courses/{course_id}`
- `GET /employee/my_courses/{course_id}/progress`
- `PATCH /employee/my_courses/{course_id}/progress`
- `GET /employee/my_courses/{course_id}/test`

## 7) Как проверить, что все связано

1. В desktop зарегистрируй сотрудника.
2. В web (менеджер) назначь курс сотруднику.
3. В desktop обнови список — курс должен быть в "в процессе".
4. В mobile (админ) проверь рост агрегированной статистики, но без персональных деталей.

## 8) Частые проблемы

### 404 на `/`
Исправлено: backend теперь отдает `{"status":"ok"}` на корне.

### 401 Unauthorized
Проверь Bearer токен и роль пользователя.

### Не открывается клиент
- проверь `npm install` выполнен;
- проверь версию Node/Python/Flutter;
- проверь `.env` с `API_BASE_URL=http://127.0.0.1:8000`.

### Error: Can't resolve `tailwindcss` in `C:\projects\kai 2`
Это значит, что web-клиент запускается не из папки `hrrepozik` **или** не установлены зависимости именно в `hrrepozik`.

Исправление:
```powershell
cd C:\projects\kai 2\hrrepozik
npm install
npm install -D tailwindcss postcss autoprefixer
npm run dev
```

Важно: не запускай `npm run dev` из `C:\projects\kai 2` (корень mono-репозитория).
