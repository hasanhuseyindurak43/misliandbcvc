print(f"{ 1000 + ((1000 / 100) * (34.22 / 360) * 32):.2f} TL")

from datetime import datetime, timedelta

bugun = datetime.now()
vadegun = 32

# 32 gün ekleyerek tarihi hesapla
gelecek_tarih = bugun + timedelta(days=vadegun)

# Yıl, ay ve gün bilgisini alarak tarihi oluştur
tarih = f"{gelecek_tarih.year}-{gelecek_tarih.month:02d}-{gelecek_tarih.day:02d} {gelecek_tarih.hour:02d}:{gelecek_tarih.minute:02d}:{gelecek_tarih.second:02d}"

print(tarih)

from backend import *
from datetime import datetime, timedelta

try:
    faizler = backend.faizs.faizcontrol(None)
    for row in faizler:
        fid = row['fid']
        username = row['username']
        vade_s_tarih = row['vade_bitis_tarih']
        vade_s_tutar = row['vade_s_tutar']
        bugun = datetime.now()
        tarih = f"{bugun.year}-{bugun.month:02d}-{bugun.day:02d} {bugun.hour:02d}:{bugun.minute:02d}:{bugun.second:02d}"

        if vade_s_tarih == bugun:

            # Cüzdana vade sonu tutarı ekleme bölümü
            sql = "SELECT * FROM cuzdan WHERE username = %s"
            params = (user,)  # Parametreleri bir tuple içinde sağladık
            cursor.execute(sql, params)
            cuzdans = cursor.fetchone()

            if cuzdans:
                cuzdanmiktari = cuzdans['cuzdan_miktar']
                miktar = cuzdanmiktari + vade_s_tutar
                sql = "UPDATE cuzdan SET cuzdan_miktar = %s, cuzdan_r_date = %s WHERE username = %s"
                cursor.execute(sql, (miktar, tarih, username,))
                db.commit()

            # Vade sonu açılan hesabı kapatma bölümü
            sql = "DELETE FROM faiz WHERE username = %s AND fid = %s"
            cursor.execute(sql, (username, fid,))
            db.commit()

except Exception as e:
    print(f"HATA: {e}")