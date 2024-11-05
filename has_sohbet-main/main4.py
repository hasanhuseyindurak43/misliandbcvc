import sys
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtCore import QThreadPool, QRunnable, pyqtSlot
import backend.veri_listele
import icon_rc  # Resource dosyasını import edin
import os
from datetime import datetime, timedelta
from backend import *
import mysql.connector
from functools import partial

conn = mysql.connector.connect(
    host="localhost",        # MySQL sunucusu
    user="barron4335",    # MySQL kullanıcı adı
    password="1968Hram",# MySQL şifresi
    database="has_kazanc" # Bağlanmak istediğiniz veritabanı
)
cursor = conn.cursor()

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        uic.loadUi('uis/loginpanel.ui', self)

        self.failed_attempts = 0
        self.lockout_time = None

        # Timer for ikiframe
        self.iki_timer = QtCore.QTimer(self)
        self.iki_timer.timeout.connect(self.iki_move_frame)
        self.iki_x_pos = -204
        self.iki_timer.start(3)

    def iki_move_frame(self):
        if self.iki_x_pos < 80:
            self.iki_x_pos += 1  # Movement in positive direction
            self.ikiframe.setGeometry(QtCore.QRect(130, self.iki_x_pos, 301, 191))
        else:
            self.iki_timer.stop()

    def logincontrol(self):
        username = self.kad.text()
        password = self.kparola.text()

        # Eğer kullanıcı kilitlenmişse, şifre yanlış girme sayısının ve kilitlenme süresinin kontrolü
        if self.lockout_time and datetime.now() < self.lockout_time:
            remaining_time = (self.lockout_time - datetime.now()).total_seconds()
            minutes, seconds = divmod(int(remaining_time), 60)
            QtWidgets.QMessageBox.warning(self, 'Kilitli Hesap', f'Çok fazla deneme yaptınız. Lütfen {minutes} dakika {seconds} saniye sonra tekrar deneyin.')
            return

        # Giriş bilgileri doğruysa dashboard'u aç
        check_user = backend.veri_listele.CheckUser(username, password)
        if check_user.verify_user():  # Örnek doğrulama
            check_statu = backend.veri_listele.CheckUserStatu(username)
            if check_statu.verify_user() == 'aktif':
                QtWidgets.QMessageBox.warning(self, 'Uyarı', f'Kullanıcı {username} zaten giriş yapmıştır.!')

            elif check_statu.verify_user() == 'pasif':
                user_data = backend.veri_listele.CheckUserDetay(username)
                user_data = user_data.verify_user()
                self.load = LoadWindow(user_data[0][0],user_data[0][1])
                self.load.show()
                self.close()
        else:
            self.failed_attempts += 1
            if self.failed_attempts >= 5:
                self.lockout_time = datetime.now() + timedelta(minutes=10)
                self.failed_attempts = 0  # Hata sayacını sıfırla
                QtWidgets.QMessageBox.warning(self, 'Hatalı Giriş', '5 kez yanlış şifre girdiniz. Lütfen 10 dakika bekleyin.')
            else:
                QtWidgets.QMessageBox.warning(self, 'Hatalı Giriş', 'Kullanıcı adı veya parola yanlış!')

# class ChromeScrapyDriverWorker(QRunnable):
#     def __init__(self, mac_adet):
#         super().__init__()
#         self.mac_adet = mac_adet
#
#     @pyqtSlot()
#     def run(self):
#         try:
#             if self.mac_adet is not None:
#                 scrapy.mac_analiz.Application(self.mac_adet)
#         except Exception as e:
#             print(f"Bir hata oluştu: {e}")
#         finally:
#             print("Scrapy driver işçi işlevi tamamlandı.")

class LoadWindow(QtWidgets.QMainWindow):
    def __init__(self, user_id, username):
        super(LoadWindow, self).__init__()
        uic.loadUi('uis/load.ui', self)

        self.user_id = user_id
        self.username = username
        userupdate = backend.veri_guncelle.UserUpdate(self.username)
        userupdate.verify_user()

        # 2 dakika (120000 ms) sonra işlemi başlat
        QtCore.QTimer.singleShot(110, self.start_progress)

        # Başlangıç değerleri
        self.counter = -1
        self.max_value = 100

        self.thread_pool = QThreadPool()

    def start_progress(self):
        # Timer oluştur
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)  # Her 100ms'de bir güncelle

    def update_progress(self):
        if self.counter < self.max_value:

            # Sayacı arttır
            self.counter += 1

            # QLCDNumber'ı güncelle
            self.number.display(self.counter)

            # QProgressBar'ı güncelle
            self.progressBar.setValue(self.counter)

            # self.check_scrapy_driver_version(mac_adet)

            if self.counter == 100:
                self.dashboard = DashboardWindow(user_id=self.user_id, username=self.username)
                self.dashboard.show()
                self.close()

        else:
            # Eğer 100'e ulaştıysa timer'ı durdur
            self.timer.stop()

    # def check_scrapy_driver_version(self, mac_adet):
    #     print("Scrapy driver worker başlatılıyor...")
    #     worker = ChromeScrapyDriverWorker(mac_adet)
    #     self.thread_pool.start(worker)
    #     print("Scrapy driver worker başlatıldı.")

class DashboardWindow(QtWidgets.QMainWindow):
    def __init__(self, user_id, username):
        super(DashboardWindow, self).__init__()
        uic.loadUi('uis/dashboard.ui', self)

        self.user_id = user_id
        self.username = username

        self.anasayfa.clicked.connect(self.anasayfa_function)
        self.ayarlar.clicked.connect(self.ayarlar_function)
        self.gruplar.clicked.connect(self.gruplar_function)
        self.mesajlar.clicked.connect(self.mesajlar_function)

        self.widgets = []

        # QLabel nesnelerini saklamak için bir liste oluştur# Başlangıçta UpdateThread'i başlatın
        self.update_thread = UpdateThread(self)
        self.update_thread.update_signal.connect(self.update_labels)
        self.update_thread.start()

        # QLabel nesnelerini saklamak için bir liste oluştur# Başlangıçta UpdateThread'i başlatın
        self.update_thread1 = UpdateThread(self)
        self.update_thread1.update_signal.connect(self.load_friend_requests)
        self.update_thread1.start()

        # QLabel nesnelerini saklamak için bir liste oluştur# Başlangıçta UpdateThread'i başlatın
        self.update_thread2 = UpdateThread(self)
        self.update_thread2.update_signal.connect(self.load_friends)
        self.update_thread2.start()

        # Timer for ikiframe
        self.iki_timer = QtCore.QTimer(self)
        self.iki_timer.timeout.connect(self.iki_move_frame)
        self.iki_x_pos = -145
        self.iki_timer.start(2)

        # Timer for ucframe
        self.uc_timer = QtCore.QTimer(self)
        self.uc_timer.timeout.connect(self.uc_move_frame)
        self.uc_x_pos = -145
        self.uc_timer.start(2)

        self.kad.setText(username)

        # Timer for dortframe
        self.current_frame = None
        self.target_frame = None
        self.dort_x_pos = 800
        self.dort_timer = QtCore.QTimer(self)
        self.dort_timer.timeout.connect(self.move_frames)

        self.show_initial_frame()

        self.load_friend_requests()
        self.load_friends()

    def show_initial_frame(self):
        self.dortframe_anasayfa.setGeometry(QtCore.QRect(160, 10, 621, 591))
        self.dortframe_ayarlar.setGeometry(QtCore.QRect(800, 10, 621, 591))
        self.dortframe_gruplar.setGeometry(QtCore.QRect(800, 10, 621, 591))
        self.dortframe_mesajlar.setGeometry(QtCore.QRect(800, 10, 621, 591))
        self.current_frame = self.dortframe_anasayfa

    def anasayfa_function(self):
        if self.current_frame != self.dortframe_anasayfa:
            self.target_frame = self.dortframe_anasayfa
            self.start_frame_transition()

    def ayarlar_function(self):
        if self.current_frame != self.dortframe_ayarlar:
            self.target_frame = self.dortframe_ayarlar
            self.start_frame_transition()

    def gruplar_function(self):
        if self.current_frame != self.dortframe_gruplar:
            self.target_frame = self.dortframe_gruplar
            self.start_frame_transition()

    def mesajlar_function(self):
        if self.current_frame != self.dortframe_mesajlar:
            self.target_frame = self.dortframe_mesajlar
            self.start_frame_transition()

    def start_frame_transition(self):
        # Başlangıç konumunu belirle
        if self.current_frame:
            self.dort_x_pos = 160  # Mevcut frame'yi geri hareket ettir
        else:
            self.dort_x_pos = 800  # Yeni frame'yi dışarıdan getirecek
        self.dort_timer.start(2)

    def move_frames(self):
        if self.current_frame:
            if self.dort_x_pos < 800:
                self.dort_x_pos += 5
                self.current_frame.setGeometry(QtCore.QRect(self.dort_x_pos, 10, 621, 591))
            else:
                self.dort_timer.stop()
                self.current_frame.setGeometry(QtCore.QRect(800, 10, 621, 591))
                self.current_frame = None
                self.dort_x_pos = 160
                self.start_frame_transition()  # Yeni frame için hareketi başlat
        else:
            if self.dort_x_pos > 160:
                self.dort_x_pos -= 5
                self.target_frame.setGeometry(QtCore.QRect(self.dort_x_pos, 10, 621, 591))
            else:
                self.dort_timer.stop()
                self.current_frame = self.target_frame
                self.target_frame = None
                self.dort_x_pos = 800
    def iki_move_frame(self):
        if self.iki_x_pos < 10:
            self.iki_x_pos += 1  # Movement in positive direction
            self.ikiframe.setGeometry(QtCore.QRect(self.iki_x_pos, 10, 141, 301))
        else:
            self.iki_timer.stop()

    def uc_move_frame(self):
        if self.uc_x_pos < 10:
            self.uc_x_pos += 1
            self.ucframe.setGeometry(QtCore.QRect(self.uc_x_pos, 320, 141, 281))
        else:
            self.uc_timer.stop()

    def send_friend_request(self, receiver_id):
        self.send_friend_requests(self.user_id, receiver_id)
        QtWidgets.QMessageBox.information(self, "Başarılı", "Arkadaşlık isteği gönderildi!")

    def send_friend_requests(self, sender_id, receiver_id):
        query = "INSERT INTO friend_requests (sender_id, receiver_id) VALUES (%s, %s)"
        cursor.execute(query, (sender_id, receiver_id))
        conn.commit()

    def load_friend_requests(self):
        self.requests_list.clear()
        query = "SELECT fr.id, u.username FROM friend_requests fr JOIN user u ON fr.sender_id = u.id WHERE fr.receiver_id = %s AND fr.status = 'pending'"
        cursor.execute(query, (self.user_id,))
        requests = cursor.fetchall()

        for request_id, sender_username in requests:
            item = QtWidgets.QListWidgetItem(sender_username)
            item.setData(QtCore.Qt.UserRole, request_id)
            self.requests_list.addItem(item)

        self.requests_list.itemClicked.connect(self.handle_request_click)

    def handle_request_click(self, item):
        request_id = item.data(QtCore.Qt.UserRole)
        response = QtWidgets.QMessageBox.question(self, "Arkadaşlık İsteği", f"{item.text()} adlı kullanıcının arkadaşlık isteğini kabul etmek istiyor musunuz?",
                                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if response == QtWidgets.QMessageBox.Yes:
            self.respond_to_friend_request(request_id, True)
            QtWidgets.QMessageBox.information(self, "Başarılı", "Arkadaşlık isteği kabul edildi!")
        else:
            self.respond_to_friend_request(request_id, False)
            QtWidgets.QMessageBox.information(self, "Reddedildi", "Arkadaşlık isteği reddedildi.")

    def load_friends(self):
        self.friend_list.clear()
        friends = self.get_friends(self.user_id)
        for friend in friends:
            self.friend_list.addItem(friend[0])

    def respond_to_friend_request(self, request_id, response):
        status = 'accepted' if response else 'rejected'
        query = "UPDATE friend_requests SET status = %s WHERE id = %s"
        cursor.execute(query, (status, request_id))
        conn.commit()

        if status == 'accepted':
            query = """
            INSERT INTO friends (user1_id, user2_id)
            SELECT sender_id, receiver_id FROM friend_requests WHERE id = %s
            """
            cursor.execute(query, (request_id,))
            conn.commit()

    def get_friends(self, user_id):
        query = """
        SELECT u.username FROM friends f
        JOIN user u ON (f.user1_id = u.id OR f.user2_id = u.id)
        WHERE (f.user1_id = %s OR f.user2_id = %s) AND u.id != %s
        """
        cursor.execute(query, (user_id, user_id, user_id))
        return cursor.fetchall()

    def update_labels(self, users):
        # Mevcut QLabel'leri temizle
        for widget_tuple in self.widgets:
            for widget in widget_tuple:
                widget.setParent(None)  # QWidget nesnelerini kaldır

        self.widgets = []

        y_offset = 0
        for user in users:
            kadname = QtWidgets.QLabel(self.ucframe)
            kadname.setText(user[1])
            kadname.setGeometry(10, y_offset, 101, 31)
            kadname.setStyleSheet("""
                                            color: rgb(0, 0, 0);
                                            font: 25 italic 10pt "Ubuntu";
                                        """)
            kadname.show()
            icon5 = QtGui.QIcon()
            icon5.addPixmap(QtGui.QPixmap(":/sent/img/sent-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            ekle = QtWidgets.QPushButton(self.ucframe)
            ekle.setIcon(icon5)
            ekle.clicked.connect(partial(self.send_friend_request, user[0]))
            ekle.setGeometry(110, y_offset, 31, 28)
            ekle.setStyleSheet("""
            QPushButton {
                background-color: rgb(54, 145, 171);
                border-style: outset;
                border-width: 2px;
                color: rgb(0, 0, 0);
                border: 1px solid black;
                border-radius: 10px;
            }

            QPushButton:hover {
                background-color: rgb(255, 255, 255);
                color: rgb(54, 145, 171);
                border-style: outset;
                border-width: 2px;
                border: 1px solid black;
                border-radius: 10px;
            }
            """)
            ekle.show()
            self.widgets.append((kadname, ekle))
            y_offset += 35

    def closeEvent(self, event):
        if self.update_thread.isRunning():
            self.update_thread.stop()  # Thread'in çalışmasını durdur
            self.update_thread.wait()  # Thread'in kapanmasını bekle# Pencere kapatıldığında UserUpdate çağırtry:

        user_update = backend.veri_guncelle.UserUpdate(username=self.username)
        user_update.verify_user()

        # Kapatma olayını kabul et
        event.accept()

class UpdateThread(QtCore.QThread):
    update_signal = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._running = True # Çalışma durumunu kontrol etmek için bir flag

    def run(self):
        while self._running:
            QtCore.QThread.sleep(1)  # Her 30 saniyede bir bekle# Burada MySQL sorgusunu çalıştır
            user_instance = backend.veri_listele.ListUser()
            users = user_instance.get_users()
            if users is not None:
                self.update_signal.emit(users)

    def stop(self):
        self._running = False# Thread'in durmasını sağla
def main():
    app = QtWidgets.QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
