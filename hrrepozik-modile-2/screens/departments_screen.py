from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from data import get_departments
from utils import get_kpi_color

KV = """
<DepartmentsScreen>:
    name: "departments"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 0.93, 0.94, 0.96, 1

        MDTopAppBar:
            title: "Отделы"
            md_bg_color: 1, 1, 1, 1
            specific_text_color: 0.08, 0.12, 0.22, 1

        ScrollView:
            MDBoxLayout:
                id: deps_box
                orientation: "vertical"
                adaptive_height: True
                spacing: "10dp"
                padding: "12dp"
"""
Builder.load_string(KV)


class DepartmentsScreen(Screen):
    def on_pre_enter(self, *args):
        """Рендерит аналитику по всем отделам."""
        self.ids.deps_box.clear_widgets()
        for dep in get_departments():
            color = get_kpi_color(dep["kpi"])
            card = MDCard(
                orientation="vertical",
                padding="12dp",
                size_hint_y=None,
                height="180dp",
                radius=[16, 16, 16, 16],
                md_bg_color=(0.97, 0.97, 0.97, 1),
            )
            card.add_widget(MDLabel(text=f"{dep['name']} (KPI: {dep['kpi']}%)", bold=True, text_color=color))
            card.add_widget(MDLabel(text=f"Сотрудников: {dep['employees_count']}"))
            card.add_widget(MDLabel(text=f"Средний прогресс: {dep['average_progress']}%"))
            card.add_widget(MDLabel(text=f"Средний балл: {dep['average_score']}%"))
            card.add_widget(MDLabel(text=f"Завершено курсов: {dep['completed_courses']}"))
            card.add_widget(MDLabel(text=f"Просрочено курсов: {dep['overdue_courses']}"))
            self.ids.deps_box.add_widget(card)
