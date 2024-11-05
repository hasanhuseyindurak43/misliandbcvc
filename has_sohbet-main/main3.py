import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget, QListWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
import mysql.connector

# MySQL bağlantısı (Veritabanı bilgilerinizi buraya girin)
connection = mysql.connector.connect(
    host="localhost",
    user="barron4335",
    password="1968Hram",
    database="has_kazanc"
)
cursor = connection.cursor()

class FriendSystem(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Arkadaşlık Sistemi')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Arkadaşlık isteklerini gönderme
        self.send_request_button = QPushButton("Arkadaşlık İsteği Gönder", self)
        self.send_request_button.clicked.connect(self.send_friend_request)
        layout.addWidget(self.send_request_button)

        # Gelen arkadaşlık isteklerini gösterme
        self.friend_requests_label = QLabel("Gelen Arkadaşlık İstekleri:", self)
        layout.addWidget(self.friend_requests_label)

        self.requests_list = QListWidget(self)
        layout.addWidget(self.requests_list)

        # Arkadaş listesini gösterme
        self.friend_list_label = QLabel("Arkadaşlarınız:", self)
        layout.addWidget(self.friend_list_label)

        self.friend_list = QListWidget(self)
        layout.addWidget(self.friend_list)

        self.setLayout(layout)
        self.load_friend_requests()
        self.load_friends()

    def send_friend_request(self):
        # Arkadaşlık isteği göndermek için bir kullanıcı ID'si girmek gerekiyor (örneğin, 2. kullanıcıya isteği gönderiyoruz)
        receiver_id = 1  # Bu örnekte, 2 numaralı kullanıcıya istek gönderiyoruz.
        send_friend_request(self.user_id, receiver_id)
        QMessageBox.information(self, "Başarılı", "Arkadaşlık isteği gönderildi!")

    def load_friend_requests(self):
        self.requests_list.clear()
        query = "SELECT fr.id, u.username FROM friend_requests fr JOIN user u ON fr.sender_id = u.id WHERE fr.receiver_id = %s AND fr.status = 'pending'"
        cursor.execute(query, (self.user_id,))
        requests = cursor.fetchall()

        for request_id, sender_username in requests:
            item = QListWidgetItem(sender_username)
            item.setData(Qt.UserRole, request_id)
            self.requests_list.addItem(item)

        self.requests_list.itemClicked.connect(self.handle_request_click)

    def handle_request_click(self, item):
        request_id = item.data(Qt.UserRole)
        response = QMessageBox.question(self, "Arkadaşlık İsteği", f"{item.text()} adlı kullanıcının arkadaşlık isteğini kabul etmek istiyor musunuz?",
                                        QMessageBox.Yes | QMessageBox.No)

        if response == QMessageBox.Yes:
            respond_to_friend_request(request_id, True)
            QMessageBox.information(self, "Başarılı", "Arkadaşlık isteği kabul edildi!")
        else:
            respond_to_friend_request(request_id, False)
            QMessageBox.information(self, "Reddedildi", "Arkadaşlık isteği reddedildi.")

        self.load_friend_requests()
        self.load_friends()

    def load_friends(self):
        self.friend_list.clear()
        friends = get_friends(self.user_id)
        for friend in friends:
            self.friend_list.addItem(friend[0])

def send_friend_request(sender_id, receiver_id):
    query = "INSERT INTO friend_requests (sender_id, receiver_id) VALUES (%s, %s)"
    cursor.execute(query, (sender_id, receiver_id))
    connection.commit()

def respond_to_friend_request(request_id, response):
    status = 'accepted' if response else 'rejected'
    query = "UPDATE friend_requests SET status = %s WHERE id = %s"
    cursor.execute(query, (status, request_id))
    connection.commit()

    if status == 'accepted':
        query = """
        INSERT INTO friends (user1_id, user2_id)
        SELECT sender_id, receiver_id FROM friend_requests WHERE id = %s
        """
        cursor.execute(query, (request_id,))
        connection.commit()

def get_friends(user_id):
    query = """
    SELECT u.username FROM friends f
    JOIN user u ON (f.user1_id = u.id OR f.user2_id = u.id)
    WHERE (f.user1_id = %s OR f.user2_id = %s) AND u.id != %s
    """
    cursor.execute(query, (user_id, user_id, user_id))
    return cursor.fetchall()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    user_id = 2  # Örnek kullanıcı ID'si (Giriş yapan kullanıcı)
    window = FriendSystem(user_id)
    window.show()
    sys.exit(app.exec_())