from .db import *

class UserUpdate():
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
            if statu == 'pasif':
                sql = "UPDATE user SET statu = 'aktif' WHERE username = %s"
                cursor.execute(sql, (self.username,))
                conn.commit()
            elif statu == 'aktif':
                sql = "UPDATE user SET statu = 'pasif' WHERE username = %s"
                cursor.execute(sql, (self.username,))
                conn.commit()
        else:
            # Kullanıcı adı bulunamadıysa False döndür
            return False