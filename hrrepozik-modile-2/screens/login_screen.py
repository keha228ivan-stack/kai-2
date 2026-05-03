from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from data import get_test_user

KV = """
<LoginScreen>:
    name: "login"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 0.93, 0.94, 0.96, 1
        padding: "24dp"
        spacing: "16dp"

        MDLabel:
            text: "HR Analytics"
            halign: "center"
            font_style: "H4"

        MDLabel:
            text: "Вход для руководителя"
            halign: "center"

        Widget:
            size_hint_y: None
            height: "24dp"

        MDTextField:
            id: login_input
            hint_text: "Логин"
            helper_text: "Введите логин"
            helper_text_mode: "on_focus"

        MDTextField:
            id: password_input
            hint_text: "Пароль"
            password: True
            helper_text: "Введите пароль"
            helper_text_mode: "on_focus"

        MDRaisedButton:
            text: "Войти"
            pos_hint: {"center_x": 0.5}
            on_release: root.do_login(login_input.text, password_input.text)

        MDTextButton:
            text: "Нет аккаунта? Регистрация"
            pos_hint: {"center_x": 0.5}
            on_release: app.switch_screen("register")

        MDLabel:
            id: error_label
            text: ""
            theme_text_color: "Error"
            halign: "center"
"""

Builder.load_string(KV)


class LoginScreen(Screen):
    """Экран авторизации руководителя."""

    def do_login(self, login, password):
        """Проверяет логин/пароль и переводит на Dashboard."""
        user = get_test_user()
        if login == user["login"] and password == user["password"]:
            self.ids.error_label.text = ""
            self.manager.current = "dashboard"
        else:
            self.ids.error_label.text = "Неверный логин или пароль"
