"""Утилиты для расчета метрик HR-аналитики."""


def calculate_average_progress(employees):
    """Возвращает средний процент прохождения обучения."""
    if not employees:
        return 0
    return round(sum(item["progress"] for item in employees) / len(employees), 1)


def calculate_average_score(employees):
    """Возвращает средний балл тестирования."""
    if not employees:
        return 0
    return round(sum(item["test_score"] for item in employees) / len(employees), 1)


def get_risk_employees(employees):
    """Возвращает сотрудников в зоне риска с расшифровкой причин."""
    risk_list = []
    for employee in employees:
        reasons = []
        if employee["progress"] < 50:
            reasons.append("Низкий прогресс обучения")
        if employee["overdue"]:
            reasons.append("Просрочен курс")
        if employee["test_score"] < 60:
            reasons.append("Низкий средний балл")

        if reasons:
            item = dict(employee)
            item["risk_reason"] = ", ".join(reasons)
            risk_list.append(item)
    return risk_list


def get_kpi_status(value):
    """Возвращает статус KPI по процентному значению."""
    if value >= 80:
        return "Хорошо"
    if value >= 60:
        return "Требует внимания"
    return "Критично"


def get_kpi_color(value):
    """Возвращает цвет KPI в формате RGBA для Kivy."""
    if value >= 80:
        return (0.2, 0.7, 0.3, 1)  # зеленый
    if value >= 60:
        return (0.95, 0.75, 0.2, 1)  # желтый
    return (0.85, 0.25, 0.25, 1)  # красный


def calculate_dashboard_stats(employees, departments):
    """Возвращает агрегированные показатели для Dashboard."""
    total_employees = len(employees)
    assigned_courses = len(employees)
    completed_courses = sum(1 for item in employees if item["progress"] >= 100)
    if completed_courses == 0:
        # Для реалистичного прототипа учитываем завершенные по отделам, если в сотрудниках нет 100%.
        completed_courses = sum(dep["completed_courses"] for dep in departments)

    overdue_courses = sum(1 for item in employees if item["overdue"])
    risk_employees = len(get_risk_employees(employees))

    return {
        "Всего сотрудников": {
            "value": total_employees,
            "description": "Общее количество сотрудников в системе обучения",
        },
        "Назначено курсов": {
            "value": assigned_courses,
            "description": "Количество назначений обучающих курсов",
        },
        "Завершено курсов": {
            "value": completed_courses,
            "description": "Количество курсов, завершенных сотрудниками",
        },
        "Средний процент прохождения": {
            "value": f"{calculate_average_progress(employees)}%",
            "description": "Средний процент прохождения назначенных курсов",
        },
        "Средний балл тестирования": {
            "value": f"{calculate_average_score(employees)}%",
            "description": "Средний результат по тестированию сотрудников",
        },
        "Количество просроченных курсов": {
            "value": overdue_courses,
            "description": "Число курсов, завершение которых просрочено",
        },
        "Количество сотрудников в зоне риска": {
            "value": risk_employees,
            "description": "Сотрудники с низким прогрессом/оценкой или просрочками",
        },
    }
