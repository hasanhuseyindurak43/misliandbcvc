from flask import Flask, url_for, render_template, redirect, request, session, Response, Blueprint
from flask_sitemapper import Sitemapper
from datetime import datetime, timedelta
import backend
import random
global event_names
event_names = {}

login_bp = Blueprint('login', __name__)
sitemapper = Sitemapper()
################################################ Login Sayfa Başlangıç #############################################################################

@sitemapper.include(lastmod="2022-02-08")
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))

    error = ''
    durum = 3

    if request.method == 'POST':
        if request.form['username'] == '':
            error = 'Kullanıcı adı veya E-posta adresinizi belirtin.'
        elif request.form['password'] == '':
            error = 'Şifrenizi belirtin.'
        else:

            encusername = f"{backend.ucdencrypt(request.form['username'], backend.key)}"

            encsifre = f"{backend.ucdencrypt(request.form['password'], backend.key)}"

            user = backend.user.login(None, encusername, encusername, encsifre)
            if user:
                giris = user['user_giris']

                if giris == 0:
                    host = request.remote_addr
                    bugun = datetime.now()
                    tarih = f"{bugun.year}-{bugun.month}-{bugun.day} {bugun.hour}:{bugun.minute}:{bugun.second}"

                    backend.user.login_update(None, tarih, "1", user['uid'])

                    session['user_id'] = user['uid']

                    rand_num = random.randint(1000, 9999)
                    event_name = f"cikis_etkinligi_{rand_num}"
                    event_names[session['user_id']] = event_name
                    session['last_activity_{user_id}'] = datetime.now()

                    backend.user.event_start(None, event_name, user['uid'])

                    session.permanent = True
                    return redirect(url_for('home'))
                elif giris == 1:
                    error = 'Bu kullanıcı zaten giriş yapmıştır.'
            else:
                error = 'Girdiğiniz bilgilere ait kullanıcı bulunamadı.'

    return render_template('views/login.html', error=error, durum=durum)

################################################ Login Sayfa Bitiş #############################################################################

@sitemapper.include(lastmod="2022-02-08")
@login_bp.route('/logout/<id>')
def logout(id):
    backend.user.logout_update(None,"0", id)
    event_name = event_names.pop(int(id), None)
    if event_name:
        backend.user.event_update(None, event_name)
    session.permanent = False
    session.clear()
    return redirect(url_for('home'))

