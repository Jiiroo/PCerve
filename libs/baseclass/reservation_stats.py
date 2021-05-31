import data_base
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.utils import asynckivy
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelThreeLine
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy.clock import Clock

Builder.load_file('./libs/kv/reservation_stats.kv')

class StatsCard(MDCard):
    index = NumericProperty()
    store_id = NumericProperty()
    product_id = NumericProperty()
    count = NumericProperty(0)
    name = StringProperty('')
    price = StringProperty()
    stocks = NumericProperty()
    date = StringProperty()

    def cancel_item(self):
        conn = data_base.conn_db('./assets/data/pcerve_data.db')
        cursor = conn.cursor()
        print(self.index)
        cursor.execute(f'DELETE from confirmed_reserve where id = {self.index}')
        conn.commit()
        conn.close()
        self.parent.remove_widget(self)

class ReservationStatus(Screen):
    def __init__(self, **kwargs):
        super(ReservationStatus, self).__init__(**kwargs)
        self.get = get = MDApp.get_running_app()

    def on_enter(self, *args):
        data_items = []
        dates = []
        conn = data_base.conn_db('./assets/data/pcerve_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id from accounts WHERE status = "active"')
        usr_id = cursor.fetchone()
        cursor.execute('CREATE TABLE IF NOT EXISTS confirmed_reserve(id integer unique primary key autoincrement, '
                       'usr_id, store_id, product_id, count, products, price, date)')
        cursor.execute(f'SELECT * from confirmed_reserve WHERE usr_id = {usr_id[0]}')
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            data_items.append(row)
        for date in data_items:
            if date not in date:
                dates.append(date)

        async def on_enter():
            price = 0
            conn2 = data_base.conn_db('./assets/data/pcerve_data.db')
            cursor2 = conn2.cursor()

            for info in data_items:
                await asynckivy.sleep(0)
                cursor2.execute(f'SELECT stocks FROM store_{info[2]} where id = {info[3]}')
                pick = cursor2.fetchone()
                print(info[2])
                price += (float(info[6].replace(',', '')) * info[4])

                store_widgets = StatsCard(store_id=info[2], product_id=info[3],
                                          count=info[4], name=info[5], price=info[6],
                                          index=info[0], stocks=pick[0], date=info[7],)

                self.ids.content.add_widget(store_widgets)
            # self.dialog.dismiss()
            print('{:,}'.format(price))
            self.total = '{:,}'.format(price)
            conn2.close()

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

    def cancel_all(self):
        conn = data_base.conn_db('./assets/data/pcerve_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id from accounts WHERE status = "active"')
        uid = cursor.fetchone()

        cursor.execute(f'DELETE from confirmed_reserve WHERE usr_id = {uid[0]}')
        conn.commit()
        conn.close()
        self.ids.content.clear_widgets()

    def on_leave(self, *args):
        self.ids.content.clear_widgets()
