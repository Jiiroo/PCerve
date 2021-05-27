import sqlite3
import data_base
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.utils import asynckivy
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.modalview import ModalView
from kivy.lang.builder import Builder
from kivy.clock import Clock

Builder.load_file('./libs/kv/login.kv')

class Login(Screen):
    usr_name = ObjectProperty(None)
    usr_pass = ObjectProperty(None)

    def usr_login(self):
        rows = None
        try:
            conn = data_base.conn_db('./assets/data/pcerve_data.db')
            cursor = conn.cursor()
            cursor.execute(f'SELECT password FROM accounts WHERE email = "{self.usr_name.text}"')
            rows = cursor.fetchone()
        except (AttributeError, sqlite3.OperationalError):
            rows = None

        if rows is not None:

            if self.usr_pass.text == rows[0]:
                cursor.execute(f'UPDATE accounts set status = "active" WHERE email = "{self.usr_name.text}"')
                conn.commit()
                self.reset_field()
                return True
            else:
                print('Wrong username or email or password')
        else:
            print('No account')

        self.reset_field()
        conn.close()

    def reset_field(self):
        self.usr_name.text = ''
        self.usr_pass.text = ''

