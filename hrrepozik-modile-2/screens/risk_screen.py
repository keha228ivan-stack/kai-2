from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from data import get_employees
from utils import get_risk_employees

KV = """
<RiskScreen>:
    name: "risk"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 0.93, 0.94, 0.96, 1

        MDTopAppBar:
            title: "Зона риска"
            md_bg_color: 1, 1, 1, 1
            specific_text_color: 0.08, 0.12, 0.22, 1

        ScrollView:
            MDBoxLayout:
                id: risk_box
                orientation: "vertical"
                adaptive_height: True
                spacing: "10dp"
                padding: "12dp"
"""
Builder.load_string(KV)


class RiskScreen(Screen):
    def on_pre_enter(self, *args):
        """Формирует список сотрудников, требующих внимания."""
        self.ids.risk_box.clear_widgets()
        for employee in get_risk_employees(get_employees()):
            card = MDCard(orientation="vertical", padding="12dp", size_hint_y=None, height="170dp", radius=[16] * 4)
            card.add_widget(MDLabel(text=employee["name"], bold=True))
            card.add_widget(MDLabel(text=f"Отдел: {employee['department']}"))
            card.add_widget(MDLabel(text=f"Курс: {employee['course']}"))
            card.add_widget(MDLabel(text=f"Прогресс: {employee['progress']}% | Балл: {employee['test_score']}%"))
            card.add_widget(MDLabel(text=f"Причина: {employee['risk_reason']}", theme_text_color="Error"))
            self.ids.risk_box.add_widget(card)
