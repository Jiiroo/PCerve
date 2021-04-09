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
from kivymd.uix.list import MDList, OneLineIconListItem, TwoLineAvatarListItem, OneLineListItem, ILeftBodyTouch, ImageLeftWidget
from kivy.properties import ListProperty, StringProperty, ObjectProperty, NumericProperty


class Login(Screen):
    usr_name = ObjectProperty(None)
    usr_pass = ObjectProperty(None)
    
    def usr_login(self):
        conn = conn_db('usr_acc.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        if self.usr_name.text in rows[0]:
            usr_index = rows[0].index(self.usr_name.text)
            print(usr_index)
        else:
            print('Wrong username or email or password')
        if self.usr_pass.text == rows[1][usr_index]:
            print('matched')
            self.go_main(self.usr_name.text)
            self.reset_field()
        else:
            print('Wrong username or email or password 2')
            
    def reset_field(self):
        self.usr_name.text = ''
        self.usr_pass.text = ''

    @staticmethod
    def go_signup():
        manage.current = 'register'

    @staticmethod
    def go_main(info):
        print('Logged in')

    
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
            self.reset_field()
            self.go_login()

    def reset_field(self):
        self.usr_name.text = ''
        self.usr_pass1.text = ''
        self.usr_pass2.text = ''
        
    @staticmethod
    def go_login():
        manage.current = 'login'
    
def conn_db(filename):
    try:
        conn = sqlite3.connect(filename)
    except Error as e:
        print(e)
    return conn
    
class ForgotPassword(Screen):
    pass



class MainMenu(Screen):
    def navigation_draw(self):
        pass

class ContentDrawer(Screen):
    pass


class Store(Screen):
    pass

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
                      MainMenu(name='main')]
    
        for navigate in navigating:
            manage.add_widget(navigate)
        manage.current = 'main'

class Manager(ScreenManager):
    pass


manage = Manager()

if __name__ == "__main__":
    
    MyApp().run()
