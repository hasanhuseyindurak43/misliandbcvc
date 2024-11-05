from flask import url_for, render_template, redirect, request, session, Blueprint
from datetime import datetime
from backend import *
from decimal import Decimal
from .onselenium import go_to_tranfertion

garanti_bp = Blueprint('garanti', __name__)

global payment_names
payment_names = {}
@garanti_bp.route('/garantipayment', methods=['GET', 'POST'])
def garanti():
    if 'user_id' in session:
        user_id = session['user_id']
        durums = backend.user.user_durum(None, user_id)
        durum = durums['user_statu']
        error = ''

        if request.method == 'POST':
            if payment_names:
                return redirect(url_for('home'))
            else:

                if request.form['username'] == '':
                    error = 'TC Kimliğinizi giriniz...!'
                elif request.form['tutar'] == '':
                    error = 'Yatıracak Miktarınızı giriniz...!'
                elif request.form['password'] == '':
                    error = 'Parolanızı giriniz..!'
                else:
                    payment_names[session['user_id']] = "garantiSelenium"
                    if (go_to_tranfertion.go_on_mobile(None, tc=request.form['username'], parola=request.form['password'], yatirilanlimit=request.form['tutar']) == True):

                        payment_names.clear()

                        tutar = request.form['tutar']
                        tutar = Decimal(tutar)

                        cuzdans.changecuzdan(None, user_id, tutar)
                        return render_template('garantipayment/success.html')
                    else:
                        payment_names.clear()
                        return render_template('garantipayment/fail.html')

        return render_template('garantipayment/garantipayment.html', durum=durum, error=error)

    else:
        return redirect(url_for('home'))

@garanti_bp.route('/garantipaymentfail', methods=['GET', 'POST'])
def garantipaymentfail():
    if 'user_id' in session:
        user_id = session['user_id']
        durums = backend.user.user_durum(None, user_id)
        durum = durums['user_statu']
        render_template('garantipayment/fail.html')

@garanti_bp.route('/garantipaymentsuccess', methods=['GET', 'POST'])
def garantipaymentsuccess():
    if 'user_id' in session:
        user_id = session['user_id']
        durums = backend.user.user_durum(None, user_id)
        durum = durums['user_statu']
        render_template('garantipayment/success.html')