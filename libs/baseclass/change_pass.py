from libs.baseclass import data_base
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy.clock import Clock

Builder.load_file('./libs/kv/change_pass.kv')

class ChangePass(Screen):
    old_pass = ObjectProperty()
    new_pass = ObjectProperty()
    confirm = ObjectProperty()

    def __init__(self, **kwargs):
        super(ChangePass, self).__init__(**kwargs)

    def change(self, *args):
        if self.new_pass.text == self.confirm.text:

            conn = data_base.conn_db('./assets/data/pcerve_data.db')
            cursor = conn.cursor()
            cursor.execute('SELECT password FROM accounts WHERE status = "active"')
            get_data = cursor.fetchone()

            if get_data[0] == self.old_pass.text:
                cursor.execute(f'UPDATE accounts SET password = "{self.new_pass.text}" WHERE status = "active"')
            conn.commit()
            conn.close()

            self.old_pass.text = ''
            self.new_pass.text = ''
            self.confirm.text = ''


