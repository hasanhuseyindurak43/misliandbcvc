# IMPORT BACKEND
import time

import backend
from backend import *

# IMPORT CRYPTO

# IMPORT FLASK
from flask import Flask, request, render_template, Response, session, send_from_directory, make_response, redirect, url_for
from flask_sitemapper import Sitemapper
from flask_apscheduler import APScheduler

# IMPORT TİMEAGO
import timeago

# IMPORT TİME AND DATETİME
from datetime import datetime, timedelta
import time

# LOGİN VE REGİSTER
from loginandregister.login import login_bp
from loginandregister.register import register_bp

# VİEWS
from views.faiz import faiz_bp
from views.para import para_bp

# VİEWS / GARANTİ PAYMENT
from views.garantipayment.garanti import garanti_bp

import sys

sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__

def categories():
    sql = "SELECT * FROM categories ORDER BY category_name ASC"
    cursor.execute(sql)
    cats = cursor.fetchall()
    return cats

def timeAgo(date):
    return timeago.format(date, datetime.now(), 'tr')

class Config:
    SCHEDULER_API_ENABLED = True

sitemapper = Sitemapper()
app = Flask(__name__)
app.secret_key = b',\xbd\x0b\xa6qr\x8f\xb95*Z\xe9+w\x9c\xfb'
app.jinja_env.globals.update(categories=categories)
app.jinja_env.filters['timeAgo'] = timeAgo
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)
app.config['SESSION_PERMANENT'] = False
sitemapper.init_app(app)

app.config.from_object(Config())

# initialize scheduler
scheduler = APScheduler()
scheduler.init_app(app)

app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(faiz_bp)
app.register_blueprint(para_bp)
app.register_blueprint(garanti_bp)

event_names = {}
odeme_names = {}

@sitemapper.include(lastmod="2022-02-08")
@app.route('/', methods=['GET', 'POST'])
def home():
    if 'user_id' in session:
        user_id = session['user_id']
        durums = backend.user.user_durum(None, user_id)
        durum = durums['user_statu']

        packet = backend.packets.checkingPackets(None)

        cuzdan = backend.cuzdans.checkingcuzdan(None, user_id)

        faiz = backend.faizs.checkingfaiz(None, user_id)

        ptalep = backend.payment_taleb.checking_payment(None, user_id)

        if durum == 1:
            return render_template('administrator/index.html', durum=durum)
        elif durum == 2:
            return render_template('views/index.html', durum=durum, packets=packet, cuzdans=cuzdan, faizs=faiz, ptaleps=ptalep)
    else:
        packet = backend.packets.checkingPackets(None)
        durum = 3
        return render_template('views/index.html', durum=durum, packets=packet)

################################################ Crontab Sayfa Başlangıç #############################################################################
@scheduler.task('interval', id='do_job_1', minutes=1)
def my_scheduled_job():
    global db
    global cursor

    # FAİZ CROP
    try:
        faizler = backend.faizs.faizcontrol(None)
        if faizler:
            fid = faizler[0]['fid']
            username = faizler[0]['username']
            vade_s_tutar = faizler[0]['vade_s_tutar']
            bugun = datetime.now()
            tarihtwo = f"{bugun.year}-{bugun.month:02d}-{bugun.day:02d} {bugun.hour:02d}:{bugun.minute:02d}:{bugun.second:02d}"
            tarihtwo_datetime = datetime.strptime(tarihtwo, "%Y-%m-%d %H:%M:%S")

            odeme_alinacak_tarih = bugun + timedelta(days=int(1))
            odeme_alinacak_tarih = f"{odeme_alinacak_tarih.year}-{odeme_alinacak_tarih.month:02d}-{odeme_alinacak_tarih.day:02d}"
            odeme_alinacak_tarih = datetime.strptime(odeme_alinacak_tarih, "%Y-%m-%d")

            db = backend.db
            cursor = db.cursor(dictionary=True)

            # Cüzdana vade sonu tutarı ekleme bölümü
            sql = "SELECT * FROM cuzdan WHERE username = %s"
            params = (username,)  # Parametreleri bir tuple içinde sağladık
            cursor.execute(sql, params)
            cuzdans = cursor.fetchone()
            if cuzdans:
                cuzdanmiktari = cuzdans['cuzdan_miktar']
                miktar = cuzdanmiktari + vade_s_tutar
                sql = "UPDATE cuzdan SET cuzdan_miktar = %s, cuzdan_r_date = %s, odeme_tarihi = %s WHERE username = %s"
                cursor.execute(sql, (miktar, tarihtwo_datetime, odeme_alinacak_tarih, username,))
                db.commit()
                cursor.close()

                db = backend.db
                cursor = db.cursor(dictionary=True)

                # Vade sonu açılan hesabı kapatma bölümü
                sql = "DELETE FROM faiz WHERE username = %s AND fid = %s"
                cursor.execute(sql, (username, fid,))
                db.commit()
                cursor.close()

                db = backend.db
                cursor = db.cursor(dictionary=True)

                time.sleep(20)

    except Exception as e:
        print(e)


    # PAYMENT CROP
    try:
        payment_list = backend.payment_taleb.payment_list(None)

        if payment_list:
            username = payment_list[0]['username']
            ponay = 1
            bugun = datetime.now()

            tarihtwo = f"{bugun.year}-{bugun.month:02d}-{bugun.day:02d} {bugun.hour:02d}:{bugun.minute:02d}:{bugun.second:02d}"

            tarihtwo_datetime = datetime.strptime(tarihtwo, "%Y-%m-%d %H:%M:%S")

            db = backend.db
            cursor = db.cursor(dictionary=True)
            sql = "UPDATE ptalep SET ptalep_onay = %s, ptalep_r_date = %s WHERE username = %s"
            backend.cursor.execute(sql, (ponay, tarihtwo_datetime, username))
            backend.db.commit()
            cursor.close()

            db = backend.db
            cursor = db.cursor(dictionary=True)

            time.sleep(20)
    except Exception as e:
        print(e)

@scheduler.task('interval', id='do_job_2', minutes=1)
def my_payment_jop():
    global db
    global cursor


################################################ Crontab Sayfa Bitiş #############################################################################

################################################ Hatalı Sayfa Başlangıç #############################################################################

@app.errorhandler(404)
def page_not_found(error):
    if 'user_id' in session:
        user_id = session['user_id']
        durums = backend.user.user_durum(None, user_id)
        durum = durums['user_statu']

        return render_template('not-found.html', durum=durum), 404
    else:
        return render_template('not-found.html'), 404

################################################ Hatalı Sayfa Bitiş #############################################################################


########################### ROBOTS TEXT #################################
@app.route('/robots.txt')
def robots():
    r = Response(response="""# robots.txt İHS Telekom tarafından oluşturuldu\n
User-agent: Googlebot\n
Disallow: /adminpanel\n
User-agent: googlebot-image\n
Disallow: /adminpanel\n
User-agent: googlebot-mobile\n
Disallow: /adminpanel\n
User-agent: Slurp\n
Disallow: /adminpanel\n
User-agent: Teoma\n
Disallow: /adminpanel\n
User-agent: yahoo-mmcrawler\n
Disallow: /adminpanel\n
User-agent: *\n
Disallow: /adminpanel\n
Crawl-delay: 120\n
Disallow: /adminpanel\n
Sitemap: http://78.186.138.86/sitemap.xml\n
""", status=200, mimetype="text/plain")
    r.headers["Content-Type"] = "text/plain; charset=utf-8"
    return r

@app.route("/sitemap.xml")
def sitemap():
  return sitemapper.generate()

scheduler.start()

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)