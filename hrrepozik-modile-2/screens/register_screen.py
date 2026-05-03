from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from data import register_user

KV = """
<RegisterScreen>:
    name: "register"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 0.93, 0.94, 0.96, 1
        padding: "24dp"
        spacing: "12dp"

        MDLabel:
            text: "Регистрация руководителя"
            halign: "center"
            font_style: "H5"

        MDTextField:
            id: full_name
            hint_text: "ФИО"
        MDTextField:
            id: email
            hint_text: "Email"
        MDTextField:
            id: login
            hint_text: "Логин"
        MDTextField:
            id: password
            hint_text: "Пароль"
            password: True

        MDRaisedButton:
            text: "Зарегистрироваться"
            on_release: root.do_register(full_name.text, email.text, login.text, password.text)

        MDTextButton:
            text: "Назад ко входу"
            on_release: app.switch_screen("login")

        MDLabel:
            id: msg
            text: ""
            halign: "center"
"""
Builder.load_string(KV)


class RegisterScreen(Screen):
    def do_register(self, full_name, email, login, password):
        if not all([full_name, email, login, password]):
            self.ids.msg.text = "Заполните все поля"
            return
        register_user(login, password, full_name, email)
        self.ids.msg.text = "Пользователь создан. Войдите с новыми данными"
