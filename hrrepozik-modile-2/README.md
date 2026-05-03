# HR Analytics Mobile (Kivy)

Мобильный прототип аналитического клиента HR-системы для руководства компании.

## Что реализовано

- Авторизация руководителя (тестовый пользователь).
- Dashboard с ключевыми показателями обучения.
- Аналитика по отделам с цветовой индикацией KPI.
- Экран KPI со статусами и progress bar.
- Экран сотрудников в зоне риска.
- Экран текстовых отчетов.
- Нижняя навигация по разделам + выход.

## Тестовые данные для входа

- `login`: `director`
- `password`: `1234`

## Структура проекта

```text
main.py
data.py
utils.py
screens/
  login_screen.py
  dashboard_screen.py
  departments_screen.py
  kpi_screen.py
  risk_screen.py
  reports_screen.py
```

## Установка зависимостей

```bash
pip install kivy kivymd
```

## Запуск

```bash
python main.py
```

## Идея для дальнейшего развития

Слой `data.py` уже организован как провайдер данных через функции (`get_employees`, `get_departments` и т.д.).
Поэтому при подключении backend/API можно заменить только внутреннюю реализацию провайдера, без изменения экранов.
