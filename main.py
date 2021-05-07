import kivy
import sqlite3
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.config import Config
from kivymd.utils import asynckivy
from kivy.lang.builder import Builder
from kivymd.uix.dialog import MDDialog
from kivy.uix.modalview import ModalView
from time import time, asctime, localtime
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
        conn = conn_db('usr_acc.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        for usernames in rows:
            temp_username.append(usernames[0])
        if self.usr_name.text in temp_username:
            usr_index = temp_username.index(self.usr_name.text)
            print(usr_index)
            if self.usr_pass.text == rows[usr_index][1]:
                print('matched')
                # write_data = open('current_user.txt', 'w')
                # write_data.write(self.usr_name.text)
                # write_data.close()

                log_usr = self.usr_name.text

                self.go_main()
            else:
                print('Wrong username or email or password 2')

        else:
            print('Wrong username or email or password')
        self.reset_field()

    @staticmethod
    def go_main():
        manage.current = 'store'

    def reset_field(self):
        self.usr_name.text = ''
        self.usr_pass.text = ''

    @staticmethod
    def go_signup():
        manage.current = 'register'

class RegisterUser(Screen):
    usr_name = ObjectProperty(None)
    usr_pass1 = ObjectProperty(None)
    usr_pass2 = ObjectProperty(None)

    def register(self):
        if self.usr_pass1.text == self.usr_pass2.text:
            conn = conn_db('usr_acc.db')
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS users(login_cred, password)')
            insert_query = 'INSERT INTO users (login_cred, password) VALUES (?,?)'
            cursor.execute(insert_query, (self.usr_name.text, self.usr_pass1.text,))
            conn.commit()
            cursor.close()

            conn = conn_db(f'assets/data/{self.usr_name.text}.db')
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS users(login_cred, password)')
            insert_query = 'INSERT INTO users (login_cred, password) VALUES (?,?)'
            cursor.execute(insert_query, (self.usr_name.text, self.usr_pass1.text,))
            conn.commit()
            cursor.close()

            self.reset_field()
            manage.current = 'login'
        else:
            self.reset_field()

    def reset_field(self):
        self.usr_name.text = ''
        self.usr_pass1.text = ''
        self.usr_pass2.text = ''

    @staticmethod
    def go_login():
        manage.current = 'login'

    @staticmethod
    def go_main():
        manage.current = 'store'
        print('Logged in')


class PersonalInfo(Screen):
    pass

class ForgotPassword(Screen):
    pass


class NavDrawer(Screen):
    @staticmethod
    def go_profile():
        manage.current = 'profile'

    @staticmethod
    def go_store():
        pass

    @staticmethod
    def go_cart():
        print('cart')
        # manage.current = 'cart'

    @staticmethod
    def go_status():
        pass

    @staticmethod
    def go_settings():
        pass

    @staticmethod
    def go_about():
        pass

    @staticmethod
    def out():
        manage.current = 'login'


class Profile(Screen):
    @staticmethod
    def go_back():
        manage.current = 'store'

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
        print(log_usr)
        async def on_enter():
            for info in data_items:
                await asynckivy.sleep(0)
                store_widgets = Card(index=info[4], icon=f'assets/{info[2]}/icon.png',
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
            self.tick = 0

        Clock.schedule_once(refresh_callback, 1)

    def store_direct(self):
        reset_data = []
        data_items = []
        conn = conn_db('store_direct.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM details")
        cursor.execute("SELECT *, ROW_NUMBER() OVER(ORDER BY id) AS NoId FROM details")
        rows = cursor.fetchall()

        for row in rows:
            reset_data.append(row)
        data_items = reset_data

        cursor.close()
        print(rows)
        return data_items

    def on_press(self, instance):
        global store_index
        store_index = instance.index
        print(instance.index)
        

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
        print(e)
    return conn


class ProductDetails(Screen):
    pass


class MyApp(MDApp):
    def __init__(self, **kwargs):
        self.title = 'PCerve'
        super().__init__(**kwargs)

    def build(self):
        Builder.load_file("layout.kv")

        return manage

    def on_start(self):
        navigating = [RegisterUser(name='register'),
                      Login(name='login'),
                      Store(name='store'),
                      Profile(name='profile')]

        for navigate in navigating:
            manage.add_widget(navigate)
        manage.current = 'register'


class Manager(ScreenManager):
    pass


log_usr = None
store_index = None
manage = Manager()

if __name__ == "__main__":
    MyApp().run()
