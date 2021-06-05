from libs.baseclass import data_base
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivymd.utils import asynckivy

Builder.load_file('./libs/kv/app_settings.kv')

class BlankCard(MDCard):
    name = StringProperty('')
    email = StringProperty('')
    password = StringProperty('')

class AppSettings(Screen):
    def __init__(self, **kwargs):
        super(AppSettings, self).__init__(**kwargs)

    def on_enter(self):
        conn = data_base.conn_db('./assets/data/pcerve_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM accounts WHERE status = "active"')
        get_data = cursor.fetchone()

        conn.close()

        async def on_enter():
            await asynckivy.sleep(0)
            self.ids.content.add_widget(BlankCard(name=get_data[1], email=get_data[2], password='*' * len(get_data[3])))

        asynckivy.start(on_enter())

    def on_leave(self, *args):
        self.ids.content.clear_widgets()
