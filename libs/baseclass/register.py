import data_base
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.utils import asynckivy
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.modalview import ModalView
from kivy.lang.builder import Builder
from kivy.clock import Clock

Builder.load_file('./libs/kv/register.kv')

class RegisterUser(Screen):
    usr_name = ObjectProperty(None)
    usr_email = ObjectProperty(None)
    usr_pass1 = ObjectProperty(None)
    usr_pass2 = ObjectProperty(None)

    def register(self):
        if self.usr_pass1.text == self.usr_pass2.text:
            conn = data_base.conn_db('./assets/data/pcerve_data.db')
            cursor = conn.cursor()

            cursor.execute('CREATE TABLE IF NOT EXISTS accounts(id integer unique primary key autoincrement, name, '
                           'email, password, status)')
            insert_query = 'INSERT INTO accounts (name, email, password) VALUES (?,?,?)'
            cursor.execute(insert_query, (self.usr_name.text, self.usr_email.text, self.usr_pass1.text))
            conn.commit()
            conn.close()

            self.reset_field()
            # manage.current = 'login'
            return True
        else:
            self.reset_field()

    def reset_field(self):
        self.usr_name.text = ''
        self.usr_email.text = ''
        self.usr_pass1.text = ''
        self.usr_pass2.text = ''

