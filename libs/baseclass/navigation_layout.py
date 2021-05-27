import data_base
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty, NumericProperty, ObjectProperty

Builder.load_file('./libs/kv/navigation_layout.kv')


class NavLayoutScreen(Screen):
    name_usr = ObjectProperty(None)
    email_usr = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(NavLayoutScreen, self).__init__(**kwargs)

    def logout(self):
        conn = data_base.conn_db('./assets/data/pcerve_data.db')
        cursor = conn.cursor()
        cursor.execute(f'UPDATE accounts set status = "inactive" WHERE status = "active"')
        conn.commit()
        conn.close()

    def on_leave(self, *args):
        pass
