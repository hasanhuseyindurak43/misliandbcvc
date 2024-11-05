from flask import Flask, url_for, render_template, redirect, request, session, Response, Blueprint
from flask_sitemapper import Sitemapper
from flask_sitemapper import Sitemapper
import hashlib
from backend import *
from datetime import datetime, timedelta, timezone

register_bp = Blueprint('register', __name__)
sitemapper = Sitemapper()

################################################ Register Sayfa Başlangıç #############################################################################

@sitemapper.include(lastmod="2022-02-08")
@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    error = ''
    durum=3
    if request.method == 'POST':
        encusername = f"{backend.ucdencrypt(request.form['kuladi'], backend.key)}"

        enciban = f"{backend.ucdencrypt(request.form['kullbankanumara'], backend.key)}"

        encemail = f"{backend.ucdencrypt(request.form['kuleposta'], backend.key)}"

        if request.form['firstname'] == '':
            error = 'Adınızı giriniz..!'
        elif request.form['lastname'] == '':
            error = 'Soyadınızı giriniz..!'
        elif request.form['kuladi'] == '':
            error = 'Kullanıcı Adınızı giriniz..!'
        elif backend.register.hasusername(None, encusername):
            error = 'Bu Kullanıcı Adı ile birisi zaten kayıtlı, başka bir tane deneyin'
        elif request.form['kuleposta'] == '':
            error = 'Kullanıcı Postanızı giriniz..!'
        elif backend.register.hasusereposta(None, encemail):
            error = 'Bu Kullanıcı Eposta ile birisi zaten kayıtlı, başka bir tane deneyin'
        elif request.form['kullbankanumara'] == '':
            error = 'Kullanıcı İban Numaranızı giriniz..!'
        elif backend.register.hasuseriban(None, enciban):
            error = 'Bu Kullanıcı İban ile birisi zaten kayıtlı, başka bir tane deneyin'
        elif request.form['kulsifre'] == '' or request.form['kulsifretwo'] == '':
            error = 'Şifrenizi belirtin.'
        elif request.form['kulsifre'] != request.form['kulsifretwo']:
            error = 'Girdiğiniz şifreler birbiriyle uyuşmuyor'
        else:

            encusername = f"{backend.ucdencrypt(request.form['kuladi'], backend.key)}"

            encfirstname = f"{backend.ucdencrypt(request.form['firstname'], backend.key)}"

            enclastname = f"{backend.ucdencrypt(request.form['lastname'], backend.key)}"

            enciban= f"{backend.ucdencrypt(request.form['kullbankanumara'], backend.key)}"

            encemail = f"{backend.ucdencrypt(request.form['kuleposta'], backend.key)}"

            encsifre = f"{backend.ucdencrypt(request.form['kulsifre'], backend.key)}"

            user_statu = 2
            user_giris = 0
            bugun = datetime.now()
            tarih = f"{bugun.year}-{bugun.month:02d}-{bugun.day:02d} {bugun.hour:02d}:{bugun.minute:02d}:{bugun.second:02d}"

            tarihtwo = f"{bugun.year}-{bugun.month:02d}-{bugun.day:02d}"
            tarihtwo_datetime = datetime.strptime(tarihtwo, "%Y-%m-%d")

            backend.register.registerUser(None, username=encusername, usereposta=encemail, userpassword=encsifre, user_giris=user_giris, user_statu=user_statu, user_r_date=tarih, user_u_date=tarih)
            last_inserted_uid = backend.cursor.lastrowid

            backend.register.registerIban(None, username=last_inserted_uid, userfirstname=encfirstname, userlastname=enclastname, useriban=enciban, user_iban_r_date=tarih, user_iban_u_date=tarih)

            cmiktar = 00.00
            backend.register.registerCuzdan(None, username=last_inserted_uid, cmiktar=cmiktar, crdate=tarih, ordate=tarihtwo_datetime)

            if backend.cursor.rowcount:
                session['user_id'] = last_inserted_uid
                return redirect(url_for('home'))
            else:
                error = 'Teknik bir problemden dolayı kaydınız oluşturulamadı'

    return render_template('views/register.html', error=error, durum=durum)

################################################ Register Sayfa Bitiş #############################################################################
