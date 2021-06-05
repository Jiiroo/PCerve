from libs.baseclass import data_base
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivymd.utils import asynckivy

Builder.load_file('./libs/kv/about_us.kv')

class Content(MDBoxLayout):
    email = StringProperty('')
    quote = StringProperty('')

class AboutUs(Screen):
    def __init__(self, **kwargs):
        super(AboutUs, self).__init__(**kwargs)

    def on_enter(self):
        data_items = []
        conn = data_base.conn_db('./assets/data/pcerve_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM about')
        get_data = cursor.fetchall()

        conn.close()
        for row in get_data:
            data_items.append(row)

        for i in data_items:
            self.ids.box.add_widget(
                MDExpansionPanel(
                    content=Content(email=i[2], quote=i[3]),
                    panel_cls=MDExpansionPanelOneLine(
                        text=i[1],
                    )
                )
            )

    def on_leave(self, *args):
        self.ids.box.clear_widgets()
