import kivy
import sqlite3
from kivymd.app import MDApp
from kivy.clock import Clock
from kivymd.utils import asynckivy
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty, StringProperty, ObjectProperty, NumericProperty
from libs.baseclass import store, type, products, product_details, reservation_cart

class Manage(ScreenManager):
    pass


manage = Manage()


class MyApp(MDApp):
    product_type = StringProperty()
    log_usr = StringProperty()
    store_index = NumericProperty()
    product_index = NumericProperty()

    def __init__(self, **kwargs):
        self.title = 'PCerve'
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.on_key)

    def colors(self, color_code):
        if color_code == 0:
            color_rgba = 0/255, 139/255, 139/255, 1
        elif color_code == 1:
            color_rgba = 0 / 255, 206 / 255, 209 / 255, 1
        elif color_code == 2:
            color_rgba = 18/255, 110/255, 110/255, 1
        return color_rgba

    def build(self):
        kv_run = Builder.load_file("main.kv")
        return kv_run

    def show_screen(self, name):
        self.root.current = 'nav_screen'
        self.root.get_screen('nav_screen').ids.manage.current = name
        return True

    def on_key(self, window, key, *args):
        if key == 27:  # the esc key
            if self.root.get_screen('nav_screen').ids.manage.current == 'store':
                previous = 'store'
            elif self.root.get_screen('nav_screen').ids.manage.current == 'product_type':
                previous = 'store'
            elif self.root.get_screen('nav_screen').ids.manage.current == 'products':
                previous = 'product_type'
            elif self.root.get_screen('nav_screen').ids.manage.current == 'details':
                previous = 'products'
            else:
                previous = False
            if previous:
                self.root.get_screen('nav_screen').ids.manage.current = previous
            return True


if __name__ == "__main__":
    MyApp().run()
