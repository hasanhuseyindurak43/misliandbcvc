from flask import Flask, url_for, render_template, redirect, request, session, Response, Blueprint
from flask_sitemapper import Sitemapper
from datetime import datetime, timedelta
import backend
import random
from decimal import Decimal
from datetime import datetime, timedelta

global event_names
event_names = {}

faiz_bp = Blueprint('faiz', __name__)
sitemapper = Sitemapper()

################################################ Faiz Sayfa Başlangıç #############################################################################

@sitemapper.include(lastmod="2022-02-08")
@faiz_bp.route('/faiz', methods=['GET', 'POST'])
def faiz():
    if 'user_id' in session:
        user_id = session['user_id']
        durums = backend.user.user_durum(None, user_id)
        durum = durums['user_statu']

        bakiye = backend.user.userbakiye(None, user_id)
        bakiye = bakiye['cuzdan_miktar']

        error = ''

        packet = backend.packets.checkingPackets(None)

        if request.method == 'POST':
            if request.form['hesap_adi'] == '':
                error = 'Hesap Adı alanını boş ıraktınız...!'
            elif request.form['tutar'] == '':
                error = 'Tutar alanını boş bıraktınız...!'
            elif request.form['vadetur'] == '':
                error = 'Vade Türünüzü belirtiniz...!'
            else:
                tutar = request.form['tutar'].replace(',', '.')
                vadetur = request.form['vadetur'].split()
                vadetutar_decimal = Decimal(tutar)
                vadeoran = vadetur[0]
                vadegun = vadetur[1]
                bugun = datetime.now()
                tarih = f"{bugun.year}-{bugun.month}-{bugun.day}"
                saat = f"{bugun.hour:02d}:{bugun.minute:02d}"
                tarihtwo = f"{bugun.year}-{bugun.month:02d}-{bugun.day:02d} {bugun.hour:02d}:{bugun.minute:02d}:{bugun.second:02d}"
                tarihtwo_datetime = datetime.strptime(tarihtwo, "%Y-%m-%d %H:%M:%S")

                try:
                    vadegun = int(vadegun)
                except ValueError:
                    vadegun = vadegun  # Veya başka bir değer

                bugun = datetime.now()

                gelecek_tarih = bugun + timedelta(days=vadegun)

                vade_s_tarih = f"{gelecek_tarih.year}-{gelecek_tarih.month:02d}-{gelecek_tarih.day:02d}"

                odeme_alinacak_tarih = bugun + timedelta(days=int(1))

                odeme_alinacak_tarih = f"{odeme_alinacak_tarih.year}-{odeme_alinacak_tarih.month:02d}-{odeme_alinacak_tarih.day:02d}"

                odeme_alinacak_tarih = datetime.strptime(odeme_alinacak_tarih, "%Y-%m-%d")

                try:
                    vadeoran = Decimal(vadeoran)
                    vadegun = int(vadegun)
                except ValueError:
                    # Hata durumunda bir değer atamalısınız veya kullanıcıya bir hata mesajı gösterebilirsiniz
                    vadeoran = float(vadeoran)
                    vadegun = int(vadegun)

                vade_s_tutar = vadetutar_decimal + ((vadetutar_decimal / 100) * (vadeoran / 365) * vadegun)

                result = backend.cuzdans.checkingcuzdanTutar(None, user=user_id, vadetutar=vadetutar_decimal)
                if result:
                    backend.cuzdans.cuzdanAzaltma(None, user=user_id, miktar=vadetutar_decimal, mrdate=tarihtwo_datetime, odate=odeme_alinacak_tarih)

                    backend.faizs.addfaiz(None, user=user_id, hesap_adi=request.form['hesap_adi'], tutar=vadetutar_decimal, vade_b_tarih=tarih, vade_b_saat=saat, vade_bitis_tarih=vade_s_tarih, vade_bitis_saat=saat, vade_s_tutar=vade_s_tutar)

                    return redirect(url_for('home'))

                else:
                    error = 'Girilen Miktar kadar cüzdanınızda bulunmamaktadır.'


        return render_template('views/faiz.html', error=error, durum=durum, bakiye=bakiye, packets=packet)

    else:
        return redirect(url_for('home'))

@sitemapper.include(lastmod="2022-02-08")
@faiz_bp.route('/faizKapat/<id>', methods=['GET', 'POST'])
def faizKapat(id):
    if 'user_id' in session:
        user_id = session['user_id']
        durums = backend.user.user_durum(None, user_id)
        durum = durums['user_statu']
        error = ''

        result = backend.faizs.changefaiz(None, user=user_id, faiz=id)

        if result == True:
            return redirect(url_for('home'))

        elif result == False:
            return redirect(url_for('home'))

    else:
        return redirect(url_for('home'))
