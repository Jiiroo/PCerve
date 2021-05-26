import data_base
from kivymd.uix.card import MDCard
from kivymd.utils import asynckivy
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy.clock import Clock

Builder.load_file('./libs/kv/reservation_cart.kv')

class ReserveCard(MDCard):
    name = StringProperty('Try')
    image = StringProperty('')
    price = NumericProperty(0)
    count = NumericProperty(0)


class ReservationCart(Screen):
    def __init__(self, **kwargs):
        super(ReservationCart, self).__init__(**kwargs)

    def on_enter(self):
        async def on_enter():

            store_widgets = ReserveCard()
            self.ids.content.add_widget(store_widgets)
            # self.dialog.dismiss()

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