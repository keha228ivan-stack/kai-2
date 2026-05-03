from kivy.lang import Builder
from kivymd.app import MDApp

from screens.dashboard_screen import DashboardScreen
from screens.departments_screen import DepartmentsScreen
from screens.kpi_screen import KpiScreen
from screens.login_screen import LoginScreen
from screens.profile_screen import ProfileScreen
from screens.register_screen import RegisterScreen
from screens.reports_screen import ReportsScreen

KV = """
#:import dp kivy.metrics.dp

MDScreen:
    md_bg_color: 0.93, 0.94, 0.96, 1
    MDBoxLayout:
        orientation: "vertical"

        ScreenManager:
            id: screen_manager

        MDBoxLayout:
            id: nav_bar
            size_hint_y: None
            height: dp(66)
            spacing: "6dp"
            padding: "8dp"
            md_bg_color: 1, 1, 1, 1

            MDRectangleFlatButton:
                text: "Главная"
                on_release: app.switch_screen("dashboard")
            MDRectangleFlatButton:
                text: "Отделы"
                on_release: app.switch_screen("departments")
            MDRectangleFlatButton:
                text: "KPI"
                on_release: app.switch_screen("kpi")
            MDRectangleFlatButton:
                text: "Отчеты"
                on_release: app.switch_screen("reports")
            MDRectangleFlatButton:
                text: "Профиль"
                on_release: app.switch_screen("profile")
            MDRaisedButton:
                text: "Выход"
                md_bg_color: 0.14, 0.38, 0.92, 1
                on_release: app.logout()
"""


class HrMobileApp(MDApp):
    def build(self):
        self.title = "HR Analytics Mobile"
        self.theme_cls.primary_palette = "Blue"
        root = Builder.load_string(KV)
        self.sm = root.ids.screen_manager

        self.sm.add_widget(LoginScreen())
        self.sm.add_widget(RegisterScreen())
        self.sm.add_widget(DashboardScreen())
        self.sm.add_widget(DepartmentsScreen())
        self.sm.add_widget(KpiScreen())
        self.sm.add_widget(ReportsScreen())
        self.sm.add_widget(ProfileScreen())

        self.sm.current = "login"
        root.ids.nav_bar.disabled = True
        root.ids.nav_bar.opacity = 0
        self.root_widget = root
        return root

    def switch_screen(self, name):
        self.sm.current = name

    def on_start(self):
        self.sm.bind(current=self.on_screen_changed)

    def on_screen_changed(self, _, current):
        is_auth = current in {"login", "register"}
        self.root_widget.ids.nav_bar.disabled = is_auth
        self.root_widget.ids.nav_bar.opacity = 0 if is_auth else 1

    def logout(self):
        self.sm.current = "login"


if __name__ == "__main__":
    HrMobileApp().run()
