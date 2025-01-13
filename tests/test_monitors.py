import unittest
import sqlite3
import os
from PyQt5.QtWidgets import QApplication
from src.monitors import SystemMonitor


class TestSystemMonitor(unittest.TestCase):
    """
    Тестирование класса SystemMonitor
    """
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.monitor = SystemMonitor()

    def test_initial_interval_button(self):
        """
        Проверка начального выбранного интервала
        """
        self.assertEqual(self.monitor.selected_interval_button.text(), '1 сек')
        self.assertEqual(self.monitor.timer.interval(), 1000)

    def test_set_interval(self):
        """
        Проверка установки интервала
        """
        button = self.monitor.interval_buttons[2]  # 3 сек
        self.monitor.set_interval(3, button)
        self.assertEqual(self.monitor.selected_interval_button.text(), '3 сек')
        self.assertEqual(self.monitor.timer.interval(), 3000)

    def test_start_stop_recording(self):
        """
        Проверка начала и остановки записи
        """
        self.monitor.start_recording()
        self.assertTrue(self.monitor.recording)
        self.assertIsNotNone(self.monitor.start_time)
        self.assertFalse(self.monitor.start_button.isVisible())
        self.assertTrue(self.monitor.stop_button.isVisible())

        self.monitor.stop_recording()
        self.assertFalse(self.monitor.recording)
        self.assertTrue(self.monitor.start_button.isVisible())
        self.assertFalse(self.monitor.stop_button.isVisible())

    def test_save_stats(self):
        """
        Проверка сохранения статистики в БД
        """
        if os.path.exists('system_stats.db'):
            os.remove('system_stats.db')
        self.monitor.save_to_db(10, 20, 30, 40, 50, 60, 70)
        conn = sqlite3.connect('system_stats.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS stats
                          (cpu REAL, ram_usage REAL, ram_free REAL, ram_total REAL,
                           disk_usage REAL, disk_free REAL, disk_total REAL, timestamp REAL)''')
        cursor.execute('SELECT * FROM stats')
        records = cursor.fetchall()
        conn.close()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0][1], 10)
        self.assertEqual(records[0][2], 20)
        self.assertEqual(records[0][3], 30)
        self.assertEqual(records[0][4], 40)
        self.assertEqual(records[0][5], 50)
        self.assertEqual(records[0][6], 60)
        self.assertEqual(records[0][7], 70)

    def test_view_records(self):
        """
        Проверка отображения записей
        """
        self.monitor.view_records()
        self.assertTrue(self.monitor.table_window.isVisible())

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()

if __name__ == '__main__':
    unittest.main()