from flask import url_for, render_template, redirect, request, session, Blueprint
from datetime import datetime
import backend
from decimal import Decimal
from .onselenium import go_to_tranfertion

global event_names
event_names = {}

global odeme_names
odeme_names = {}

para_bp = Blueprint('para', __name__)

@para_bp.route('/paraYatir', methods=['GET', 'POST'])
def paraYatir():
    if 'user_id' in session:
        user_id = session['user_id']
        durums = backend.user.user_durum(None, user_id)
        durum = durums['user_statu']
        para = 1

        return render_template('views/para.html', durum=durum, para=para)

    else:
        return redirect(url_for('home'))

@para_bp.route('/paraCek', methods=['GET', 'POST'])
def paraCek():
    if 'user_id' in session:
        user_id = session['user_id']
        durums = backend.user.user_durum(None, user_id)
        durum = durums['user_statu']
        para = 2

        error = ''

        bakiye = backend.user.userbakiye(None, user_id)
        bakiye = bakiye['cuzdan_miktar']

        bugun = datetime.now()

        tarihtwo = f"{bugun.year}-{bugun.month:02d}-{bugun.day:02d} {bugun.hour:02d}:{bugun.minute:02d}:{bugun.second:02d}"

        tarihtwo_datetime = datetime.strptime(tarihtwo, "%Y-%m-%d %H:%M:%S")

        if request.method == 'POST':

            if request.form['tutar'] == '':
                error = 'Çekmek istediğiniz tutarı belirtmediniz...!'

            else:
                tutar = request.form['tutar'].replace(',', '.')
                vadetutar_decimal = Decimal(tutar)

                result = backend.cuzdans.checkingcuzdanTutar(None, user=user_id, vadetutar=vadetutar_decimal)
                if result:
                    # Kullanıcı adına göre veritabanından bir satır çek
                    sql = "SELECT * FROM cuzdan WHERE username = %s"
                    backend.cursor.execute(sql, (user_id,))
                    cuzdans = backend.cursor.fetchone()

                    # Eğer veri bulunmuşsa devam et
                    if cuzdans:
                        # 'odeme_tarihi' değerini çek
                        odeme_alinacak_tarih = cuzdans['odeme_tarihi']

                        # 'odeme_tarihi' değerini datetime nesnesine dönüştür
                        odeme_alinacak_tarih = datetime.strptime(str(odeme_alinacak_tarih), "%Y-%m-%d")

                        resulttwo = backend.cuzdans.checkingcuzdanTarih(None, tarih=odeme_alinacak_tarih)
                        if resulttwo:
                            iban = backend.user.useriban(None, user_id)
                            for row in iban:
                                kad = f"{backend.ucddecrypt(eval(str(row['user_g_adi'])), backend.key)}"
                                kad = kad.lower()
                                ksad = f"{backend.ucddecrypt(eval(str(row['user_g_soyadi'])), backend.key)}"
                                ksad = ksad.lower()
                                kiban = f"{backend.ucddecrypt(eval(str(row['user_iban'])), backend.key)}"

                                backend.cuzdans.cuzdanAzaltma(None, user=user_id, miktar=vadetutar_decimal, mrdate=tarihtwo_datetime, odate=odeme_alinacak_tarih)

                                backend.payment_taleb.register_payment_taleb(None, user=user_id, ptalep_isim=kad, ptalep_soyisim=ksad, ptalep_iban=kiban, ptalep_tutar=vadetutar_decimal, ptalep_onay="0", ptalep_r_date=tarihtwo_datetime)

                                return redirect(url_for('home'))

                        else:
                            error = 'Cüzdanınızdan para çekmek için belirlenen günü beklemelisiniz..!'
                else:
                    error = 'Girilen Miktar kadar cüzdanınızda bulunmamaktadır...!'

        return render_template('views/para.html', durum=durum, bakiye=bakiye, error=error, para=para)

    else:
        return redirect(url_for('home'))

@para_bp.route('/paraCekTwo/<id>', methods=['GET', 'POST'])
def paraCekTwo(id):
    if 'user_id' in session:
        user_id = session['user_id']
        durums = backend.user.user_durum(None, user_id)
        durum = durums['user_statu']

        if request.method == 'GET':
            if odeme_names:
                return redirect(url_for('home'))
            else:
                sql = "SELECT * FROM ptalep WHERE pid = %s"
                backend.cursor.execute(sql, (id, ))
                ptalep = backend.cursor.fetchall()
                if ptalep:
                    pid = ptalep[0]['pid']
                    ptalepOnay = ptalep[0]['ptalep_onay']
                    if ptalepOnay == 1:
                        ptalepIsim = ptalep[0]['ptalep_isim']
                        ptalepSoyIsim = ptalep[0]['ptalep_soyisim']
                        ptalepIban = ptalep[0]['ptalep_iban']
                        ptalepMiktar = ptalep[0]['ptalep_tutar']

                        odeme_names[session['user_id']] = "selenium"

                        if (go_to_tranfertion.go_on_mobile(None,kad=ptalepIsim, ksoyad=ptalepSoyIsim, kiban=ptalepIban, kcmiktar=ptalepMiktar) == True):

                            backend.payment_taleb.delete_payment_taleb(None, user=user_id, ptalepID=pid)
                            odeme_names.clear()
                            
                            return redirect(url_for('home'))
                        else:
                            odeme_names.clear()
                            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))