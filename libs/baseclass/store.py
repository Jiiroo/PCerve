from libs.baseclass import data_base
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivymd.utils import asynckivy
from kivy.clock import Clock

Builder.load_file('./libs/kv/store.kv')

class Card(MDCard):
    index = NumericProperty()
    icon = StringProperty()
    title = StringProperty()


class Store(Screen):
    def __init__(self, **kwargs):
        super(Store, self).__init__(**kwargs)

    def on_enter(self, *args):

        # Icon for list of stores
        data_items = self.store_direct()

        async def on_enter():
            for info in data_items:
                await asynckivy.sleep(0)
                store_widgets = Card(index=info[0], icon=f'./assets/{info[0]}/icon.png',
                                     title=f'{info[1]}',
                                     on_release=self.on_press)
                self.ids.content.add_widget(store_widgets)

        asynckivy.start(on_enter())

    def refresh_callback(self, *args):
        '''A method that updates the state of your application
        while the spinner remains on the screen.'''

        def refresh_callback(interval):
            self.ids.content.clear_widgets()

            if self.x == 0:
                self.x, self.y = 0, 0
            else:
                self.x, self.y = 0, 0
            self.on_enter()
            self.ids.refresh_layout.refresh_done()

        Clock.schedule_once(refresh_callback, 1)

    def store_direct(self):
        data_items = []
        conn = data_base.conn_db('./assets/data/pcerve_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM directory")
        # cursor.execute("SELECT *, ROW_NUMBER() OVER(ORDER BY id) AS NoId FROM details")
        rows = cursor.fetchall()

        for row in rows:
            data_items.append(row)
        # data_items = reset_data

        conn.close()

        return data_items  # data_items

    def on_press(self, instance):
        get = MDApp.get_running_app()
        get.store_index = instance.index

    def on_leave(self, *args):
        self.ids.content.clear_widgets()

