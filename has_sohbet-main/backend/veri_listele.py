from .db import *
global conn
global cursor
class CheckUser():
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def verify_user(self):
        # Kullanıcı adını kontrol et
        sql = "SELECT password FROM user WHERE username = %s"
        cursor.execute(sql, (self.username,))
        result = cursor.fetchone()

        if result:
            stored_password = result[0]
            # Parolayı kontrol et
            if self.password == stored_password:
                return True
            else:
                return False
        else:
            # Kullanıcı adı bulunamadıysa False döndür
            return False

class CheckUserDetay():
    def __init__(self, username):
        self.username = username

    def verify_user(self):
        # Kullanıcı adını kontrol et
        sql = "SELECT * FROM user WHERE username = %s"
        cursor.execute(sql, (self.username,))
        result = cursor.fetchall()

        if result:
            return result
        else:
            # Kullanıcı adı bulunamadıysa False döndür
            return False

class CheckUserStatu():
    def __init__(self, username):
        self.username = username

    def verify_user(self):
        # Kullanıcı adını kontrol et
        sql = "SELECT statu FROM user WHERE username = %s"
        cursor.execute(sql, (self.username,))
        result = cursor.fetchone()

        if result:
            statu = result[0]
            # Parolayı kontrol et
            return statu
        else:
            # Kullanıcı adı bulunamadıysa False döndür
            return False

class ListUser():
    def __init__(self):
        pass
    def get_users(self):

        conn = mysql.connector.connect(
            host="localhost",  # MySQL sunucusu
            user="barron4335",  # MySQL kullanıcı adı
            password="1968Hram",  # MySQL şifresi
            database="has_kazanc"  # Bağlanmak istediğiniz veritabanı
        )
        cursor = conn.cursor()

        # Sadece 5 aktif kullanıcıyı çek
        sql = "SELECT * FROM user WHERE statu = 'aktif' LIMIT 5"
        cursor.execute(sql)
        results = cursor.fetchall()  # Fetch only 5 users
        if results:
            return results
            conn.close()
        else:
            return None


