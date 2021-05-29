import data_base
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.utils import asynckivy
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy.clock import Clock

class ReservationStatus(Screen):
    def __init__(self, **kwargs):
        super(ReservationStatus, self).__init__(**kwargs)
        self.get = get = MDApp.get_running_app()

    def on_enter(self, *args):
        pass