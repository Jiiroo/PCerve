import kivy
import sqlite3
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.config import Config
from kivymd.utils import asynckivy
from kivy.lang.builder import Builder
from kivymd.uix.dialog import MDDialog
from kivy.uix.modalview import ModalView
from time import time, asctime, localtime, sleep
from kivy.core.window import Window
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import ImageLeftWidget, MDList, OneLineIconListItem, TwoLineAvatarListItem
from kivy.properties import ListProperty, StringProperty, ObjectProperty, NumericProperty
from kivymd.uix.card import MDCard


class Login(Screen):
    usr_name = ObjectProperty(None)
    usr_pass = ObjectProperty(None)

    def usr_login(self):
        global log_usr
        temp_username = []
        conn = conn_db('./usr_acc.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        for usernames in rows:
            temp_username.append(usernames[0])
        if self.usr_name.text in temp_username:
            usr_index = temp_username.index(self.usr_name.text)

            if self.usr_pass.text == rows[usr_index][1]:
                log_usr = self.usr_name.text

                self.go_main()
            else:
                pass
                # print('Wrong username or email or password 2')

        else:
            pass
            # print('Wrong username or email or password')
        self.reset_field()

    @staticmethod
    def go_main():
        pass
        # manage.current = 'store'

    def reset_field(self):
        self.usr_name.text = ''
        self.usr_pass.text = ''

    @staticmethod
    def go_signup():
        pass
        # manage.current = 'register'

class RegisterUser(Screen):
    usr_name = ObjectProperty(None)
    usr_pass1 = ObjectProperty(None)
    usr_pass2 = ObjectProperty(None)

    def register(self):
        if self.usr_pass1.text == self.usr_pass2.text:
            conn = conn_db('./usr_acc.db')
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS users(login_cred, password)')
            insert_query = 'INSERT INTO users (login_cred, password) VALUES (?,?)'
            cursor.execute(insert_query, (self.usr_name.text, self.usr_pass1.text,))
            conn.commit()
            conn.close()

            conn = conn_db(f'./assets/data/{self.usr_name.text}.db')
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS users(login_cred, password)')
            insert_query = 'INSERT INTO users (login_cred, password) VALUES (?,?)'
            cursor.execute(insert_query, (self.usr_name.text, self.usr_pass1.text,))
            conn.commit()
            conn.close()

            self.reset_field()
            # manage.current = 'login'
        else:
            self.reset_field()

    def reset_field(self):
        self.usr_name.text = ''
        self.usr_pass1.text = ''
        self.usr_pass2.text = ''

    @staticmethod
    def go_login():
        pass
        # manage.current = 'login'

    @staticmethod
    def go_main():
        pass
        # manage.current = 'store'
        # print('Logged in')


class PersonalInfo(Screen):
    pass

class ForgotPassword(Screen):
    pass

class Profile(Screen):
    pass

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
        reset_data = []
        data_items = []
        conn = conn_db('./assets/data/pcerve_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM directory")
        # cursor.execute("SELECT *, ROW_NUMBER() OVER(ORDER BY id) AS NoId FROM details")
        rows = cursor.fetchall()

        for row in rows:
            reset_data.append(row)
        # data_items = reset_data

        conn.close()

        return reset_data  # data_items

    def on_press(self, instance):
        global store_index
        store_index = instance.index
        # manage.current = 'products'
        self.ids.content.clear_widgets()
        print(store_index)
        # print(instance.index)


class Cart(Screen):
    pass


class Status(Screen):
    pass


class Settings(Screen):
    pass


class About(Screen):
    pass


def conn_db(filename):
    try:
        conn = sqlite3.connect(filename)
    except Error as e:
        pass
        # print(e)
    return conn

class ProductCard(MDCard):
    index = NumericProperty()
    image = StringProperty()
    name = StringProperty()


class Products(Screen):
    def __init__(self, **kwargs):
        super(Products, self).__init__(**kwargs)

    def on_enter(self, *args):
        # Icon for list of stores
        data_items = self.product_direct()

        async def on_enter():
            for info in data_items:
                await asynckivy.sleep(0)
                store_widgets = ProductCard(index=info[0], image=f'./assets/{store_index}/{info[0]}.jpg',
                                            name=f'{info[1]}',
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

    def product_direct(self):
        reset_data = []
        data_items = []
        conn = conn_db(f'./assets/data/pcerve_data.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM store_{store_index}")
        # cursor.execute("SELECT *, ROW_NUMBER() OVER(ORDER BY id) AS NoId FROM products")
        rows = cursor.fetchall()

        for row in rows:
            reset_data.append(row)
        data_items = reset_data

        conn.close()

        return data_items

    def on_press(self, instance):
        global product_index
        product_index = instance.index
        self.ids.content.clear_widgets()
        # self.ids.contents.clear_widgets()
        print(instance.index)

class DetailCard(MDCard):
    image = StringProperty('')
    name = StringProperty('')
    price = NumericProperty(0)
    description = StringProperty('')
    category = StringProperty('')
    brand = StringProperty('')


class ProductDetails(Screen):
    def __init__(self, **kwargs):
        super(ProductDetails, self).__init__(**kwargs)

    def on_enter(self):
        data_items = []
        conn = conn_db(f'./assets/data/pcerve_data.db')
        cursor = conn.cursor()
        select = f"SELECT * FROM store_{store_index} where id = ?"
        print(product_index)
        cursor.execute(select, str(product_index),)
        rows = cursor.fetchone()
        print(rows)
        conn.close()

        for row in rows:
            data_items.append(row)

        async def on_enter():
            await asynckivy.sleep(0)
            details = DetailCard(image=f'./assets/{store_index}/{data_items[0]}.jpg', name=data_items[1])
            self.ids.content.add_widget(details)

        asynckivy.start(on_enter())


class MyApp(MDApp):
    def __init__(self, **kwargs):
        self.title = 'PCerve'
        super().__init__(**kwargs)

    def colors(self, color_code):
        if color_code == 0:
            color_rgba = 0/255, 139/255, 139/255, 1
        elif color_code == 1:
            color_rgba = 0 / 255, 206 / 255, 209 / 255, 1
        elif color_code == 2:
            color_rgba = 18/255, 110/255, 110/255, 1
        return color_rgba

    def build(self):
        kv_run = Builder.load_file("./layout.kv")
        return kv_run

    def show_screen(self, name):
        self.root.current = 'nav_screen'
        self.root.get_screen('nav_screen').ids.manage.current = name
        return True


log_usr = None
store_index = None
product_index = None

if __name__ == "__main__":
    MyApp().run()
