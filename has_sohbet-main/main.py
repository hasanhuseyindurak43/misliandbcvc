import sys
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import QThreadPool, QRunnable, pyqtSlot
import backend.veri_listele
import icon_rc  # Resource dosyasını import edin
import os
from datetime import datetime, timedelta
from backend import *

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
                self.load = LoadWindow(username)
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
    def __init__(self, username):
        super(LoadWindow, self).__init__()
        uic.loadUi('uis/load.ui', self)

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
                self.dashboard = DashboardWindow(username=self.username)
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
    def __init__(self, username):
        super(DashboardWindow, self).__init__()
        uic.loadUi('uis/dashboard.ui', self)

        self.username = username

        self.anasayfa.clicked.connect(self.anasayfa_function)
        self.ayarlar.clicked.connect(self.ayarlar_function)
        self.gruplar.clicked.connect(self.gruplar_function)
        self.mesajlar.clicked.connect(self.mesajlar_function)

        self.labels = []  # QLabel nesnelerini saklamak için bir liste oluştur# Başlangıçta UpdateThread'i başlatın
        self.update_thread = UpdateThread(self)
        self.update_thread.update_signal.connect(self.update_labels)
        self.update_thread.start()

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

            # user_instance = backend.veri_listele.ListUser()
            # users = user_instance.get_users()
            #
            # if users:
            #     y_offset = 0
            #     self.labels = []  # QLabel nesnelerini saklamak için bir liste oluştur
            #     for user in users:
            #         self.kadname = QtWidgets.QLabel(self.ucframe)  # QLabel nesnesini her seferinde farklı bir değişkene tanımla
            #         self.kadname.setText(user[1])
            #         self.kadname.setGeometry(10, y_offset, 101, 31)
            #
            #         # QLabel'ın stilini ayarlayın
            #         self.kadname.setStyleSheet("""
            #                             color: rgb(0, 0, 0);
            #                             font: 25 italic 10pt "Ubuntu";
            #                         """)
            #
            #         self.kadname.show()  # QLabel'ı açıkça görünür yap
            #         self.labels.append(self.kadname)  # QLabel nesnelerini listeye ekle
            #         y_offset += 35  # Sonraki QLabel için y konumunu artır
        else:
            self.uc_timer.stop()

    def closeEvent(self, event):
        if self.update_thread.isRunning():
            self.update_thread.stop()  # Thread'in çalışmasını durdur
            self.update_thread.wait()  # Thread'in kapanmasını bekle# Pencere kapatıldığında UserUpdate çağırtry:

        user_update = backend.veri_guncelle.UserUpdate(username=self.username)
        user_update.verify_user()

        # Kapatma olayını kabul et
        event.accept()

    def update_labels(self, users):
        # Mevcut QLabel'leri temizle
        for label in self.labels:
            label.setParent(None)  # QLabel nesnelerini kaldır
        self.labels = []  # Listeyi sıfırla
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
            self.labels.append(kadname)  # QLabel nesnelerini listeye ekle
            y_offset += 35

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
