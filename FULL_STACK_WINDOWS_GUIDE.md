# Windows Full Stack: backend + web + mobile + desktop (один backend)

Ниже только практические команды без альтернативных стеков.

## 0) Что установить
```powershell
python --version
node --version
npm --version
```

## 1) Backend (Терминал #1)
```powershell
cd "C:\projects\kai 2"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn backend.app.main:app --reload --host 126.0.0.1 --port 8000
```

Проверка backend:
- `http://126.0.0.1:8000`
- `http://126.0.0.1:8000/docs`

## 2) Прописать один API URL для всех клиентов
Файлы уже должны содержать:
- `hrrepozik/.env`
- `hrrepozik-modile-2/.env`
- `repozik-desktop2/.env`

Значение в каждом:
```env
API_BASE_URL=http://126.0.0.1:8000
```

## 3) Web клиент (manager) — Терминал #2
```powershell
cd "C:\projects\kai 2\hrrepozik"
npm install
cd "C:\projects\kai 2\hrrepozik"
npm run dev
```

Если увидишь `Can't resolve 'tailwindcss'` (как в твоем логе), проблема в неверном Turbopack root.

В `hrrepozik/next.config.ts` (или `next.config.js`) добавь:
```ts
import path from "node:path";

const nextConfig = {
  turbopack: {
    root: path.resolve(__dirname),
  },
};

export default nextConfig;
```

После этого:
```powershell
cd "C:\projects\kai 2\hrrepozik"
npm install
npm run dev
```

## 4) Mobile клиент (admin) — Терминал #3
```powershell
cd "C:\projects\kai 2\hrrepozik-modile-2"
npm install
npm run start
```

## 5) Desktop клиент (employee) — Терминал #4
```powershell
cd "C:\projects\kai 2\repozik-desktop2"
npm install
npm run desktop
```

## 6) Что проверить в UI, чтобы увидеть что всё связано
1. **Desktop (employee):** зайти сотрудником и открыть `my courses`.
2. **Web (manager):** назначить курс этому сотруднику.
3. **Desktop (employee):** обновить список — курс должен появиться.
4. **Desktop (employee):** выставить прогресс 100%.
5. **Web/Manager или API:** убедиться, что назначение есть.
6. **Mobile (admin):** открыть `stats` и увидеть агрегированную статистику.

Если этот сценарий проходит — все 3 клиента работают с одним backend и общей БД.
