from decimal import Decimal
from datetime import datetime, timedelta, time, date
import backend
import mysql.connector
from crypto import *

global db
db = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="barron4335",
    password="1968Hram",
    database="hasmobile"
)

global cursor
cursor = db.cursor(dictionary=True)

class register():
    def hasusername(self, username):
        sql = "SELECT * FROM users WHERE username= %s"
        cursor.execute(sql, (str(username), ))
        username = cursor.fetchall()
        if username:
            return True
        else:
            return False

    def hasusereposta(self, usereposta):
        sql = "SELECT * FROM users WHERE usereposta= %s"
        cursor.execute(sql, (str(usereposta), ))
        username = cursor.fetchall()
        if username:
            return True
        else:
            return False

    def hasuseriban(self, useriban):
        sql = "SELECT * FROM usersiban WHERE user_iban= %s"
        cursor.execute(sql, (str(useriban), ))
        username = cursor.fetchall()
        if username:
            return True
        else:
            return False

    def registerUser(self, username, usereposta, userpassword, user_giris, user_statu, user_r_date, user_u_date):
        sql = "INSERT INTO users SET username = %s, usereposta = %s, userpassword = %s, user_giris = %s, user_statu = %s, user_r_date = %s, user_u_date = %s "
        cursor.execute(sql, (username, usereposta, userpassword, user_giris, user_statu, user_r_date, user_u_date, ))
        db.commit()

    def registerIban(self, username, userfirstname, userlastname, useriban, user_iban_r_date, user_iban_u_date):
        sql = "INSERT INTO usersiban SET username = %s, user_g_adi = %s, user_g_soyadi = %s, user_iban = %s, user_iban_r_date = %s, user_iban_u_date = %s"
        cursor.execute(sql, (username, userfirstname, userlastname, useriban, user_iban_r_date, user_iban_u_date, ))
        db.commit()

    def registerCuzdan(self, username, cmiktar, crdate, ordate):
        sql = "INSERT INTO cuzdan SET username = %s, cuzdan_miktar = %s, cuzdan_r_date = %s, odeme_tarihi = %s"
        cursor.execute(sql, (username, cmiktar, crdate, ordate))
        db.commit()

class user():
    def user_durum(self, user):
        sql = "SELECT user_statu FROM users WHERE uid = %s"
        cursor.execute(sql, (user,))
        durums = cursor.fetchone()
        return durums

    def logout_update(self, sayi, user):
        sql = "UPDATE users SET user_giris = %s WHERE uid = %s"
        cursor.execute(sql, (sayi, user,))
        db.commit()

    def event_start(self, eventname, user):
        sql = f"CREATE EVENT `{eventname}`ON SCHEDULE AT CURRENT_TIMESTAMP + INTERVAL 15 MINUTE ON COMPLETION NOT PRESERVE DO UPDATE `users`SET `user_giris` = 0 WHERE `uid` = %s;"
        cursor.execute(sql, (user,))
        db.commit()

    def event_update(self, eventname):
        sql = f"DROP EVENT IF EXISTS `{eventname}`;"
        cursor.execute(sql)
        db.commit()

    def login_update(self, tarih, sayi, user):
        sql = "UPDATE users SET user_u_date = %s,  user_giris = %s WHERE uid = %s"
        cursor.execute(sql, (tarih, sayi, user, ))
        db.commit()

    def login(self, email, user, password):
        sql = "SELECT * FROM users WHERE (usereposta = %s AND userpassword = %s) OR (username = %s AND userpassword = %s)"
        cursor.execute(sql, (email, password, user, password, ))
        user = cursor.fetchone()
        return user

    def userbakiye(self, user):
        sql = "SELECT cuzdan_miktar FROM cuzdan WHERE username = %s"
        cursor.execute(sql, (user,))
        bakiyes = cursor.fetchone()
        return bakiyes

    def useriban(self, user):
        sql = "SELECT * FROM usersiban WHERE username = %s"
        cursor.execute(sql, (user,))
        ibans = cursor.fetchall()
        return ibans

class packets():
    def checkingPackets(self):
        sql = "SELECT * FROM packets"
        cursor.execute(sql)
        packets = cursor.fetchall()
        return packets

class cuzdans():

    def checkingcuzdan(self, user):
        sql = "SELECT * FROM cuzdan WHERE username = %s"
        cursor.execute(sql, (user, ))
        cuzdans = cursor.fetchall()
        return cuzdans

    def cuzdanAzaltma(self, user, miktar, mrdate, odate):
        sql = "SELECT * FROM cuzdan WHERE username = %s"
        params = (user,)  # Parametreleri bir tuple içinde sağladık
        cursor.execute(sql, params)
        cuzdans = cursor.fetchone()

        if cuzdans:
            cuzdanmiktari = cuzdans['cuzdan_miktar']
            miktar = cuzdanmiktari - miktar
            sql = "UPDATE cuzdan SET cuzdan_miktar = %s, cuzdan_r_date = %s, odeme_tarihi = %s WHERE username = %s"
            cursor.execute(sql, (miktar, mrdate, odate, user, ))
            db.commit()

    def checkingcuzdanTutar(self, user, vadetutar):

        sql = "SELECT * FROM cuzdan WHERE username = %s"
        params = (user,)  # Parametreleri bir tuple içinde sağladık
        cursor.execute(sql, params)
        cuzdans = cursor.fetchone()

        if cuzdans:
            cuzdanmiktari = cuzdans['cuzdan_miktar']
            if isinstance(cuzdanmiktari, Decimal) and vadetutar <= cuzdanmiktari:
                return True
            elif isinstance(cuzdanmiktari, Decimal) and vadetutar > cuzdanmiktari:
                return False
        else:
            return False

    def checkingcuzdanTarih(self, tarih):
        bugun = datetime.now()
        tarihtwo = f"{bugun.year}-{bugun.month:02d}-{bugun.day:02d}"
        tarihtwo = datetime.strptime(tarihtwo, "%Y-%m-%d")
        if tarih == tarihtwo:
            return True
        else:
            return False


    def changecuzdan(self, user, miktar):
        bugun = datetime.now()
        tarih = f"{bugun.year}-{bugun.month}-{bugun.day} {bugun.hour}:{bugun.minute}:{bugun.second}"

        odeme_alinacak_tarih = bugun + timedelta(days=int(1))

        odeme_alinacak_tarih = f"{odeme_alinacak_tarih.year}-{odeme_alinacak_tarih.month:02d}-{odeme_alinacak_tarih.day:02d}"

        odeme_alinacak_tarih = datetime.strptime(odeme_alinacak_tarih, "%Y-%m-%d")

        sql = "SELECT * FROM cuzdan WHERE username = %s"
        params = (user,)  # Parametreleri bir tuple içinde sağladık
        cursor.execute(sql, params)
        cuzdans = cursor.fetchone()

        if cuzdans:
            cuzdanmiktari = cuzdans['cuzdan_miktar']
            miktar = cuzdanmiktari + miktar
            sql = "UPDATE cuzdan SET cuzdan_miktar = %s, cuzdan_r_date = %s, odeme_tarihi = %s WHERE username = %s"
            cursor.execute(sql, (miktar, tarih, odeme_alinacak_tarih, user,))
            db.commit()

class faizs():
    def checkingfaiz(self, user):
        sql = "SELECT * FROM faiz WHERE username = %s"
        cursor.execute(sql, (user, ))
        faizs = cursor.fetchall()
        return faizs

    def addfaiz(self, user, hesap_adi, tutar, vade_b_tarih, vade_b_saat, vade_bitis_tarih, vade_bitis_saat, vade_s_tutar):
        sql = "INSERT INTO faiz SET username = %s, hesap_adi = %s, tutar = %s,  vade_b_tarih = %s, vade_b_saat = %s, vade_bitis_tarih = %s, vade_bitis_saat = %s, vade_s_tutar = %s"
        cursor.execute(sql, (user, hesap_adi, tutar, vade_b_tarih, vade_b_saat, vade_bitis_tarih, vade_bitis_saat, vade_s_tutar))
        db.commit()

    def changefaiz(self, user, faiz):
        sql = "SELECT * FROM faiz WHERE username = %s and fid = %s"
        cursor.execute(sql, (user, faiz))
        faizs = cursor.fetchall()
        if faizs:
            for row in faizs:
                tutar = row['tutar']
                tutar = Decimal(tutar)
                try:
                    cuzdans.changecuzdan(None, user, tutar)
                    sql = "DELETE FROM faiz WHERE username = %s AND fid = %s"
                    cursor.execute(sql, (user, faiz, ))
                    db.commit()
                    return True
                except Exception as e:
                    return False

    def faizcontrol(self):
        global db
        global cursor
        bugun = datetime.now()
        tarih = f"{bugun.year}-{bugun.month:02d}-{bugun.day:02d}"
        tarih_datetime = datetime.strptime(tarih, "%Y-%m-%d").date()
        # SELECT * FROM faiz WHERE DATE(vade_bitis_tarih) = DATE('tarih');
        sql = "SELECT * FROM faiz WHERE DATE(vade_bitis_tarih) = DATE(%s)"
        backend.cursor.execute(sql, (str(tarih), ))
        faizs = backend.cursor.fetchall()
        backend.cursor.close()
        backend.db = backend.db
        backend.cursor = backend.db.cursor(dictionary=True)
        if faizs:
            # Gelen zaman verisi (time olarak)
            faizsaat = faizs[0]['vade_bitis_saat']

            now = datetime.now()

            # 5 dakika ekleyerek
            faizfivedko = now - timedelta(minutes=5)

            # 5 dakika çıkararak
            faizfivedks = now + timedelta(minutes=5)

            fid = faizs[0]['fid']

            sql = f"SELECT * FROM faiz WHERE fid = %s AND TIME(vade_bitis_saat) BETWEEN %s AND %s"
            backend.cursor.execute(sql, (str(fid), faizfivedko.time(), faizfivedks.time(), ))
            faizs = backend.cursor.fetchall()
            backend.cursor.close()
            backend.db = backend.db
            backend.cursor = backend.db.cursor(dictionary=True)
            if faizs:
                return faizs
        else:
            pass
class payment_taleb():

    def delete_payment_taleb(self, user, ptalepID):
        sql = "DELETE FROM ptalep WHERE username = %s AND pid = %s"
        cursor.execute(sql, (user, ptalepID, ))
        db.commit()

    def register_payment_taleb(self, user, ptalep_isim, ptalep_soyisim, ptalep_iban, ptalep_tutar, ptalep_onay, ptalep_r_date):
        sql = "INSERT INTO ptalep SET username = %s, ptalep_isim = %s, ptalep_soyisim = %s, ptalep_iban = %s, ptalep_tutar = %s, ptalep_onay = %s, ptalep_r_date = %s "
        cursor.execute(sql, (user, ptalep_isim, ptalep_soyisim, ptalep_iban, ptalep_tutar, ptalep_onay, ptalep_r_date, ))
        db.commit()

    def checking_payment(self, user):
        sql = "SELECT * FROM ptalep WHERE username = %s"
        cursor.execute(sql, (user,))
        ptaleps = cursor.fetchall()
        return ptaleps

    def payment_list(self):
        global db
        global cursor
        cursor.execute("SELECT * FROM ptalep WHERE ptalep_onay = 0")
        ptaleps = cursor.fetchall()
        backend.cursor.close()
        backend.db = backend.db
        backend.cursor = backend.db.cursor(dictionary=True)
        return ptaleps

class adimlar():
    def adim(self, user):
        today = datetime.now().date()
        cursor.execute("SELECT adim FROM adimlar WHERE username = %s AND DATE(tarih) = %s", (user, today))
        result = cursor.fetchone()
        return result

    def updateadim(self, user, new_steps):
        global db
        global cursor
        today = datetime.now().date()
        cursor.execute("UPDATE adimlar SET adim = %s WHERE username = %s AND DATE(tarih) = %s",
                           (new_steps, user, today))
        db.commit()
        backend.cursor.close()
        backend.db = backend.db
        backend.cursor = backend.db.cursor(dictionary=True)

    def insertadim(self, user, new_steps):
        global db
        global cursor
        today = datetime.now().date()
        cursor.execute("INSERT INTO adimlar (username, adim, tarih) VALUES (%s, %s, %s)",
                           (user, new_steps, today))
        db.commit()
        backend.cursor.close()
        backend.db = backend.db
        backend.cursor = backend.db.cursor(dictionary=True)