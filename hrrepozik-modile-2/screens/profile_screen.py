from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from data import get_profile_data

KV = """
<ProfileScreen>:
    name: "profile"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 0.93, 0.94, 0.96, 1

        MDTopAppBar:
            title: "Профиль"
            md_bg_color: 1, 1, 1, 1
            specific_text_color: 0.08, 0.12, 0.22, 1

        MDBoxLayout:
            orientation: "vertical"
            padding: "16dp"
            spacing: "10dp"

            MDCard:
                orientation: "vertical"
                padding: "14dp"
                radius: [16,16,16,16]

                MDLabel:
                    id: full_name
                    text: ""
                    bold: True
                MDLabel:
                    id: email
                    text: ""
                MDLabel:
                    id: role
                    text: ""
                MDLabel:
                    id: login
                    text: ""
"""
Builder.load_string(KV)


class ProfileScreen(Screen):
    def on_pre_enter(self, *args):
        data = get_profile_data()
        self.ids.full_name.text = f"ФИО: {data['full_name']}"
        self.ids.email.text = f"Email: {data['email']}"
        self.ids.role.text = f"Роль: {data['role']}"
        self.ids.login.text = f"Логин: {data['login']}"
