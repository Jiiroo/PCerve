import data_base
import datetime
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.utils import asynckivy
from kivy.properties import StringProperty, NumericProperty
from kivymd.uix.picker import MDDatePicker
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder


Builder.load_file('./libs/kv/reservation_cart.kv')

class ReserveCard(MDCard):
    index = NumericProperty()
    store_id = NumericProperty()
    product_id = NumericProperty()
    count = NumericProperty(0)
    name = StringProperty('')
    price = StringProperty()
    stocks = NumericProperty()

    def update(self):
        conn = data_base.conn_db('./assets/data/pcerve_data.db')
        cursor = conn.cursor()
        cursor.execute(f'UPDATE reservations set count = {self.count} WHERE id = {self.index}')
        conn.commit()
        conn.close()

    def delete_item(self):
        conn = data_base.conn_db('./assets/data/pcerve_data.db')
        cursor = conn.cursor()
        cursor.execute(f'DELETE from reservations where id = {self.index}')
        conn.commit()
        conn.close()
        self.parent.remove_widget(self)

class ReservationCart(Screen):
    total = StringProperty()

    def __init__(self, **kwargs):
        super(ReservationCart, self).__init__(**kwargs)
        self.get = get = MDApp.get_running_app()

    def on_enter(self, *args):
        data_items = []
        conn = data_base.conn_db('./assets/data/pcerve_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id from accounts WHERE status = "active"')
        usr_id = cursor.fetchone()

        cursor.execute('CREATE TABLE IF NOT EXISTS reservations(id integer unique primary key autoincrement, usr_id, '
                       'store_id, product_id, count, products, price)')

        cursor.execute(f'SELECT * from reservations WHERE usr_id = {usr_id[0]}')
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            data_items.append(row)

        async def on_enter():
            price = 0
            conn2 = data_base.conn_db('./assets/data/pcerve_data.db')
            cursor2 = conn2.cursor()

            for info in data_items:
                await asynckivy.sleep(0)
                cursor2.execute(f'SELECT stocks FROM store_{info[2]} where id = {info[3]}')
                pick = cursor2.fetchone()

                price += (float(info[6].replace(',', ''))*info[4])
                store_widgets = ReserveCard(store_id=info[2], product_id=info[3], count=info[4], name=info[5],
                                            price=info[6], index=info[0], stocks=pick[0])
                self.ids.content.add_widget(store_widgets)
            # self.dialog.dismiss()
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

    def delete_all(self):
        conn = data_base.conn_db('./assets/data/pcerve_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id from accounts WHERE status = "active"')
        uid = cursor.fetchone()

        cursor.execute(f'DELETE from reservations WHERE usr_id = {uid[0]}')
        conn.commit()
        conn.close()
        self.ids.content.clear_widgets()

    def date_pick(self):
        date_dialog = MDDatePicker(min_date=datetime.date.today(),
                                   max_date=datetime.datetime.strptime("2025:05:30", '%Y:%m:%d').date(), )
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        data_items = []
        conn = data_base.conn_db('./assets/data/pcerve_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id from accounts WHERE status = "active"')
        uid = cursor.fetchone()

        cursor.execute(f'SELECT * FROM reservations WHERE usr_id = {uid[0]}')
        rows = cursor.fetchall()

        cursor.execute('CREATE TABLE IF NOT EXISTS confirmed_reserve(id integer unique primary key autoincrement, '
                       'usr_id, store_id, product_id, count, products, price, date)')
        for row in rows:
            insert_data = 'INSERT INTO confirmed_reserve (usr_id, store_id, product_id, count, products, price, date) '\
                          'VALUES (?,?,?,?,?,?,?)'
            cursor.execute(insert_data, (row[1], row[2], row[3], row[4], row[5], row[6], value))
            conn.commit()
        conn.close()
        self.delete_all()
        self.ids.content.clear_widgets()

    def on_cancel(self, instance, value):
        instance.dismiss()

    def on_leave(self, *args):
        self.ids.content.clear_widgets()
