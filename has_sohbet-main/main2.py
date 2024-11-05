
from PyQt5 import QtWidgets, uic, QtCore
import icon_rc  # Resource dosyasını import edin
import os
import sys

class LoadWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoadWindow, self).__init__()

        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        ui_file = os.path.join(base_path, 'uis/load.ui')

        uic.loadUi(ui_file, self)

        # 2 dakika (120000 ms) sonra işlemi başlat
        QtCore.QTimer.singleShot(110, self.start_progress)

        # Başlangıç değerleri
        self.counter = -1
        self.max_value = 100

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

            if self.counter == 100:
                self.dashboard = LoginWindow()
                self.dashboard.show()
                self.close()

        else:
            # Eğer 100'e ulaştıysa timer'ı durdur
            self.timer.stop()

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        ui_file = os.path.join(base_path, 'uis/loginpanel.ui')
        uic.loadUi(ui_file, self)

        # Timer for ikiframe
        self.iki_timer = QtCore.QTimer(self)
        self.iki_timer.timeout.connect(self.iki_move_frame)
        self.iki_x_pos = -204
        self.iki_timer.start(10)

    def iki_move_frame(self):
        if self.iki_x_pos < 80:
            self.iki_x_pos += 1  # Movement in positive direction
            self.ikiframe.setGeometry(QtCore.QRect(130, self.iki_x_pos, 301, 191))
        else:
            self.iki_timer.stop()

    def logincontrol(self):
        username = self.kad.text()
        password = self.kparola.text()
        # Bilgileri kontrol et (örnek olarak sadece konsola yazdırıyoruz)
        print(f"Kullanıcı Adı: {username}")
        print(f"Parola: {password}")

        # Giriş bilgileri doğruysa dashboard'u aç
        if username == "admin" and password == "1234":  # Örnek doğrulama
            self.dashboard = DashboardWindow(username)
            self.dashboard.show()
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, 'Hatalı Giriş', 'Kullanıcı adı veya parola yanlış!')


class DashboardWindow(QtWidgets.QMainWindow):
    def __init__(self, username):
        super(DashboardWindow, self).__init__()
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        ui_file = os.path.join(base_path, 'uis/dashboard.ui')
        uic.loadUi(ui_file, self)

        self.anasayfa.clicked.connect(self.anasayfa_function)
        self.ayarlar.clicked.connect(self.ayarlar_function)

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
        self.current_frame = self.dortframe_anasayfa

    def anasayfa_function(self):
        if self.current_frame != self.dortframe_anasayfa:
            self.target_frame = self.dortframe_anasayfa
            self.start_frame_transition()

    def ayarlar_function(self):
        if self.current_frame != self.dortframe_ayarlar:
            self.target_frame = self.dortframe_ayarlar
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
                self.dort_x_pos += 1
                self.current_frame.setGeometry(QtCore.QRect(self.dort_x_pos, 10, 621, 591))
            else:
                self.dort_timer.stop()
                self.current_frame.setGeometry(QtCore.QRect(800, 10, 621, 591))
                self.current_frame = None
                self.dort_x_pos = 160
                self.start_frame_transition()  # Yeni frame için hareketi başlat
        else:
            if self.dort_x_pos > 160:
                self.dort_x_pos -= 1
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

    def ayar_guncelle(self):
        print("Ayarları Güncelleme")
def main():
    app = QtWidgets.QApplication(sys.argv)
    login_window = LoadWindow()
    login_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
