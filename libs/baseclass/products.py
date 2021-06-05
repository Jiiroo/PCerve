from libs.baseclass import data_base
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.utils import asynckivy
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy.clock import Clock

Builder.load_file('./libs/kv/products.kv')

class ProductCard(MDCard):
    index = NumericProperty()
    image = StringProperty()
    name = StringProperty()

class Products(Screen):
    dialog = None

    def __init__(self, **kwargs):
        super(Products, self).__init__(**kwargs)
        self.get = MDApp.get_running_app()

    def on_enter(self, *args):
        # Icon for list of stores
        data_items = []
        conn = data_base.conn_db(f'./assets/data/pcerve_data.db')
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM store_{self.get.store_index} WHERE category = "{self.get.product_type}"')
        # cursor.execute("SELECT *, ROW_NUMBER() OVER(ORDER BY id) AS NoId FROM products")
        rows = cursor.fetchall()
        for row in rows:
            data_items.append(row)

        conn.close()

        async def on_enter():

            for info in data_items:
                await asynckivy.sleep(0)
                store_widgets = ProductCard(index=info[0], image=f'./assets/{self.get.store_index}/{info[0]}.jpg',
                                            name=f'{info[1]}',
                                            on_release=self.on_press)
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
        self.get.product_index = instance.index

    def on_leave(self, *args):
        self.ids.content.clear_widgets()