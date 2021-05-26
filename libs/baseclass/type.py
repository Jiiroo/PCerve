import data_base
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivymd.utils import asynckivy
from kivy.clock import Clock

Builder.load_file('./libs/kv/type.kv')

class TypesCard(MDCard):
    name = StringProperty()

class ProductTypes(Screen):
    def __init__(self, **kwargs):
        super(ProductTypes, self).__init__(**kwargs)
        self.get = get = MDApp.get_running_app()

    def on_enter(self, *args):
        data_items = []
        conn = data_base.conn_db(f'./assets/data/pcerve_data.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT category FROM store_{self.get.store_index}")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        print(rows)
        for row in rows:
            if row not in data_items:
                data_items.append(row)

        async def on_enter():

            for info in data_items:
                await asynckivy.sleep(0)
                store_widgets = TypesCard(name=f'{info[0]}', on_release=self.on_press)
                self.ids.content.add_widget(store_widgets)
            # self.dialog.dismiss()

        asynckivy.start(on_enter())
        # self.dialog.dismiss()

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

    def on_press(self, instance):
        self.get.product_type = str(instance.name)

    def on_leave(self, *args):
        self.ids.content.clear_widgets()