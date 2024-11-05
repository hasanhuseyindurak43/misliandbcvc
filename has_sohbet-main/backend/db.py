import mysql.connector

global conn
# MySQL bağlantısı oluştur
conn = mysql.connector.connect(
    host="localhost",        # MySQL sunucusu
    user="barron4335",    # MySQL kullanıcı adı
    password="1968Hram",# MySQL şifresi
    database="has_kazanc" # Bağlanmak istediğiniz veritabanı
)

global cursor
# Cursor oluştur
cursor = conn.cursor()