from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar

from data import get_kpi_metrics
from utils import get_kpi_color, get_kpi_status

KV = """
<KpiScreen>:
    name: "kpi"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 0.93, 0.94, 0.96, 1

        MDTopAppBar:
            title: "KPI"
            md_bg_color: 1, 1, 1, 1
            specific_text_color: 0.08, 0.12, 0.22, 1

        ScrollView:
            MDBoxLayout:
                id: kpi_box
                orientation: "vertical"
                adaptive_height: True
                spacing: "10dp"
                padding: "12dp"
"""
Builder.load_string(KV)


class KpiScreen(Screen):
    def on_pre_enter(self, *args):
        """Показывает KPI, статус и прогресс-бар."""
        self.ids.kpi_box.clear_widgets()
        for metric in get_kpi_metrics():
            value = metric["value"]
            status = get_kpi_status(value)
            color = get_kpi_color(value)

            card = MDCard(orientation="vertical", padding="12dp", size_hint_y=None, height="150dp", radius=[16] * 4)
            card.add_widget(MDLabel(text=f"{metric['name']}: {value}%", bold=True))
            bar = MDProgressBar(value=value)
            bar.color = color
            card.add_widget(bar)
            card.add_widget(MDLabel(text=f"Статус: {status}", text_color=color))
            self.ids.kpi_box.add_widget(card)
