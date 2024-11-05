from backend import *
from datetime import datetime, timedelta
from flask import Flask
from flask_apscheduler import APScheduler


# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True

# create app
app = Flask(__name__)
app.config.from_object(Config())

# initialize scheduler
scheduler = APScheduler()
scheduler.init_app(app)

# interval example
@scheduler.task('interval', id='do_job_1', seconds=5)
def my_scheduled_job():
    print("Cron çalışıyor.")
    faizler = backend.faizs.faizcontrol(None)
    print(faizler)
    for row in faizler:
        fid = row['fid']
        username = row['username']
        vade_s_tarih = row['vade_bitis_tarih']
        vade_s_tutar = row['vade_s_tutar']
        bugun = datetime.now()
        tarih = f"{bugun.year}-{bugun.month:02d}-{bugun.day:02d}"
        tarih_datetime = datetime.strptime(tarih, "%Y-%m-%d").date()
        tarihtwo = f"{bugun.year}-{bugun.month:02d}-{bugun.day:02d} {bugun.hour:02d}:{bugun.minute:02d}:{bugun.second:02d}"
        tarihtwo_datetime = datetime.strptime(tarihtwo, "%Y-%m-%d %H:%M:%S")

        if vade_s_tarih == tarih_datetime:
            # Cüzdana vade sonu tutarı ekleme bölümü
            sql = "SELECT * FROM cuzdan WHERE username = %s"
            params = (username,)  # Parametreleri bir tuple içinde sağladık
            cursor.execute(sql, params)
            cuzdans = cursor.fetchone()
            if cuzdans:
                cuzdanmiktari = cuzdans['cuzdan_miktar']
                miktar = cuzdanmiktari + vade_s_tutar
                sql = "UPDATE cuzdan SET cuzdan_miktar = %s, cuzdan_r_date = %s WHERE username = %s"
                cursor.execute(sql, (miktar, tarihtwo_datetime, username,))
                db.commit()

                # Vade sonu açılan hesabı kapatma bölümü
                sql = "DELETE FROM faiz WHERE username = %s AND fid = %s"
                cursor.execute(sql, (username, fid,))
                db.commit()

scheduler.start()

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)


