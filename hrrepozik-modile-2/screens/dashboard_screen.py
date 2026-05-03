from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from data import get_departments, get_employees
from utils import calculate_dashboard_stats

KV = """
<DashboardScreen>:
    name: "dashboard"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 0.93, 0.94, 0.96, 1

        MDTopAppBar:
            title: "Главная"
            md_bg_color: 1, 1, 1, 1
            specific_text_color: 0.08, 0.12, 0.22, 1

        ScrollView:
            MDBoxLayout:
                id: cards_box
                orientation: "vertical"
                adaptive_height: True
                spacing: "10dp"
                padding: "12dp"
"""
Builder.load_string(KV)


class DashboardScreen(Screen):
    def on_pre_enter(self, *args):
        """Заполняет карточки сводных метрик перед входом на экран."""
        self.ids.cards_box.clear_widgets()
        stats = calculate_dashboard_stats(get_employees(), get_departments())

        for title, item in stats.items():
            card = MDCard(
                orientation="vertical",
                padding="12dp",
                size_hint_y=None,
                height="120dp",
                radius=[16, 16, 16, 16],
            )
            card.add_widget(MDLabel(text=title, bold=True))
            card.add_widget(MDLabel(text=str(item["value"]), theme_text_color="Primary", font_style="H6"))
            card.add_widget(MDLabel(text=item["description"], theme_text_color="Secondary"))
            self.ids.cards_box.add_widget(card)
