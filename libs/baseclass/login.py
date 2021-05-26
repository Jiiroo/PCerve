import data_base
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.utils import asynckivy
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.modalview import ModalView
from kivy.lang.builder import Builder
from kivy.clock import Clock

Builder.load_file('./libs/kv/login.kv')

class Login(Screen):
    usr_name = ObjectProperty(None)
    usr_pass = ObjectProperty(None)

    def usr_login(self):
        temp_username = []
        conn = data_base.conn_db('./usr_acc.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        for usernames in rows:
            temp_username.append(usernames[0])
        if self.usr_name.text in temp_username:
            usr_index = temp_username.index(self.usr_name.text)

            if self.usr_pass.text == rows[usr_index][1]:
                log_usr = self.usr_name.text

                self.go_main()
            else:
                pass
                # print('Wrong username or email or password 2')

        else:
            pass
            # print('Wrong username or email or password')
        self.reset_field()

    @staticmethod
    def go_main():
        pass
        # manage.current = 'store'

    def reset_field(self):
        self.usr_name.text = ''
        self.usr_pass.text = ''

    @staticmethod
    def go_signup():
        pass
        # manage.current = 'register'

    def on_leave(self):
        pass