
import psutil
import sqlite3
import time
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtWidgets import QHBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QTimer

class SystemMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.recording = False
        self.start_time = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)
        self.initUI()
        

    def initUI(self):
        self.layout = QVBoxLayout()

        self.interval_layout = QHBoxLayout()
        self.interval_buttons = []
        self.selected_interval_button = None
        for i in range(1, 6):
            button = QPushButton(f'{i} сек', self)
            button.clicked.connect(lambda _, interval=i,
                                   btn=button: self.set_interval(interval, btn))
            self.interval_layout.addWidget(button)
            self.interval_buttons.append(button)

        self.layout.addLayout(self.interval_layout)

        self.set_interval(1, self.interval_buttons[0])

        self.cpu_label = QLabel('ЦП: 0%', self)
        self.ram_label = QLabel('ОЗУ: 0%', self)
        self.disk_label = QLabel('ПЗУ: 0%', self)
        self.timer_label = QLabel('Время записи 00:00', self)

        self.start_button = QPushButton('Начать запись', self)
        self.start_button.clicked.connect(self.start_recording)

        self.stop_button = QPushButton('Остановить запись', self)
        self.stop_button.clicked.connect(self.stop_recording)
        self.stop_button.hide()

        self.view_button = QPushButton('Просмотр записей', self)
        self.view_button.clicked.connect(self.view_records)

        self.layout.addWidget(self.cpu_label)
        self.layout.addWidget(self.ram_label)
        self.layout.addWidget(self.disk_label)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.stop_button)
        self.layout.addWidget(self.timer_label)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.view_button)

        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)
        self.setWindowTitle('Уровень загруженности:')
        self.show()

        self.timer.start(1000)
    
    def set_interval(self, interval, button):
        self.timer.setInterval(interval * 1000)
        if self.selected_interval_button:
            self.selected_interval_button.setStyleSheet("")
        self.selected_interval_button = button
        self.selected_interval_button.setStyleSheet("background-color: lightblue")

    def view_records(self):
        conn = sqlite3.connect('system_stats.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM stats')
        records = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        conn.close()

        table = QTableWidget()
        table.setRowCount(len(records))
        table.setColumnCount(len(column_names))
        table.setHorizontalHeaderLabels(column_names)

        for row_idx, row_data in enumerate(records):
            for col_idx, col_data in enumerate(row_data):
                table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        table.resizeColumnsToContents()
        table.resizeRowsToContents()

        self.table_window = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(table)
        self.table_window.setLayout(layout)
        self.table_window.setWindowTitle('Записи в базе данных')
        self.table_window.show()

    def update_stats(self):
        cpu_usage = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        ram_usage = ram.percent
        ram_free = ram.available / (1024 ** 3)  # в ГБ
        ram_total = ram.total / (1024 ** 3)  # в ГБ

        disk_usage = disk.percent
        disk_free = disk.free / (1024 ** 3)  # в ГБ
        disk_total = disk.total / (1024 ** 3)  # в ГБ

        self.cpu_label.setText(f'ЦП: {cpu_usage}%')
        self.ram_label.setText(f'ОЗУ: {ram_usage}% (Свободно:: {ram_free:.2f} GB, Всего: {ram_total:.2f} GB)')
        self.disk_label.setText(f'ПЗУ: {disk_usage}% (Свободно: {disk_free:.2f} GB, Всего: {disk_total:.2f} GB)')

        if self.recording:
            elapsed_time = int(time.time() - self.start_time)
            minutes, seconds = divmod(elapsed_time, 60)
            self.timer_label.setText(f'Время записи: {minutes:02d}:{seconds:02d}')
            self.save_to_db(cpu_usage, ram_usage, disk_usage, ram_free, ram_total, disk_free, disk_total)

    def start_recording(self):
        self.recording = True
        self.start_time = time.time()
        self.start_button.hide()
        self.stop_button.show()
        self.init_db()

    def stop_recording(self):
        self.recording = False
        self.start_button.show()
        self.stop_button.hide()
        self.timer_label.setText(f'Время записи 00:00')

    def init_db(self):
        self.conn = sqlite3.connect('system_stats.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS stats (
                            timestamp TEXT,
                            cpu_usage REAL,
                            ram_usage REAL,
                            ram_free REAL,
                            ram_total REAL,
                            disk_usage REAL,
                            disk_free REAL,
                            disk_total REAL)''')
        self.conn.commit()

    def save_to_db(self, cpu_usage, ram_usage, ram_free, ram_total, disk_usage, disk_free, disk_total):
        conn = sqlite3.connect('system_stats.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS stats (
                            timestamp TEXT,
                            cpu_usage REAL,
                            ram_usage REAL,
                            ram_free REAL,
                            ram_total REAL,
                            disk_usage REAL,
                            disk_free REAL,
                            disk_total REAL)''')
        cursor.execute('''INSERT INTO stats (timestamp, cpu_usage, ram_usage, ram_free, ram_total, disk_usage, disk_free, disk_total)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                    (time.strftime('%Y-%m-%d %H:%M:%S'), cpu_usage, ram_usage, ram_free, ram_total, disk_usage, disk_free, disk_total))
        conn.commit()
        conn.close()

    def closeEvent(self, event):
        if self.recording:
            self.conn.close()
        event.accept()
