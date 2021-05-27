import data_base
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.utils import asynckivy
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.modalview import ModalView
from kivy.lang.builder import Builder
from kivy.clock import Clock

Builder.load_file('./libs/kv/profile.kv')

class Profile(Screen):
    pass
