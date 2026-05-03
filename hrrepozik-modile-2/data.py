"""Модуль с тестовыми данными и простым провайдером данных."""

from copy import deepcopy
import json
from pathlib import Path

_USER_STORAGE_PATH = Path(__file__).resolve().parent / "user_data.json"

_DEFAULT_USER = {
    "login": "director",
    "password": "1234",
    "full_name": "Директор Компании",
    "email": "director@company.local",
    "role": "Руководитель",
}


def _load_current_user():
    if not _USER_STORAGE_PATH.exists():
        return deepcopy(_DEFAULT_USER)

    try:
        data = json.loads(_USER_STORAGE_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return deepcopy(_DEFAULT_USER)

    required = {"login", "password", "full_name", "email", "role"}
    if not required.issubset(set(data.keys())):
        return deepcopy(_DEFAULT_USER)
    return data


def _save_current_user(user_data):
    _USER_STORAGE_PATH.write_text(
        json.dumps(user_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


_CURRENT_USER = _load_current_user()

employees = [
    {"id": 1, "name": "Иванов Иван", "department": "Отдел продаж", "course": "Техника продаж", "progress": 45, "test_score": 58, "overdue": True},
    {"id": 2, "name": "Петрова Анна", "department": "Бухгалтерия", "course": "Финансовая отчетность", "progress": 88, "test_score": 91, "overdue": False},
    {"id": 3, "name": "Сидоров Максим", "department": "IT-отдел", "course": "Кибербезопасность", "progress": 72, "test_score": 77, "overdue": False},
    {"id": 4, "name": "Кузнецова Ольга", "department": "Производство", "course": "Охрана труда", "progress": 39, "test_score": 66, "overdue": True},
]

departments = [
    {"name": "Отдел продаж", "employees_count": 12, "average_progress": 64, "average_score": 72, "completed_courses": 18, "overdue_courses": 5, "kpi": 61},
    {"name": "Бухгалтерия", "employees_count": 8, "average_progress": 84, "average_score": 89, "completed_courses": 16, "overdue_courses": 1, "kpi": 87},
    {"name": "IT-отдел", "employees_count": 15, "average_progress": 79, "average_score": 81, "completed_courses": 22, "overdue_courses": 2, "kpi": 78},
    {"name": "Производство", "employees_count": 20, "average_progress": 58, "average_score": 63, "completed_courses": 24, "overdue_courses": 7, "kpi": 56},
]

kpi_metrics = [
    {"name": "Общий KPI обучения", "value": 76},
    {"name": "KPI завершения курсов", "value": 74},
    {"name": "KPI среднего балла тестирования", "value": 80},
    {"name": "KPI соблюдения сроков", "value": 68},
]


course_library = [
    {"id": 1, "title": "Техника продаж", "category": "Продажи", "duration_hours": 8},
    {"id": 2, "title": "Финансовая отчетность", "category": "Финансы", "duration_hours": 10},
    {"id": 3, "title": "Кибербезопасность", "category": "IT", "duration_hours": 6},
    {"id": 4, "title": "Охрана труда", "category": "Производство", "duration_hours": 5},
]

assigned_courses_progress = [
    {"employee_id": 1, "course_id": 1, "deadline": "2026-05-20", "progress": 45},
    {"employee_id": 2, "course_id": 2, "deadline": "2026-05-15", "progress": 88},
    {"employee_id": 3, "course_id": 3, "deadline": "2026-05-25", "progress": 72},
    {"employee_id": 4, "course_id": 4, "deadline": "2026-05-10", "progress": 39},
]

report_templates = {
    "Отчет по выполнению курсов": "За период назначено 42 курса, завершено 31. Средний прогресс обучения — 76%.",
    "Отчет по отделам": "Лучший KPI у Бухгалтерии (87%). Зона роста: Производство (56%) и Отдел продаж (61%).",
    "Отчет по среднему баллу тестирования": "Средний балл тестирования по компании — 72%.",
    "Отчет по просроченным курсам": "Всего просрочено 15 курсов. Наибольшее число просрочек в Производстве.",
}


def get_test_user():
    return deepcopy(_CURRENT_USER)


def register_user(login, password, full_name, email):
    global _CURRENT_USER
    _CURRENT_USER = {
        "login": login,
        "password": password,
        "full_name": full_name,
        "email": email,
        "role": "Руководитель",
    }
    _save_current_user(_CURRENT_USER)
    return deepcopy(_CURRENT_USER)


def get_profile_data():
    return {
        "full_name": _CURRENT_USER["full_name"],
        "email": _CURRENT_USER["email"],
        "role": _CURRENT_USER["role"],
        "login": _CURRENT_USER["login"],
    }


def get_employees(): return deepcopy(employees)

def get_departments(): return deepcopy(departments)

def get_kpi_metrics(): return deepcopy(kpi_metrics)

def get_report_titles(): return list(report_templates.keys())

def get_report_text(title): return report_templates.get(title, "Отчет не найден.")


def get_course_library(): return deepcopy(course_library)

def get_assigned_courses_progress(): return deepcopy(assigned_courses_progress)
