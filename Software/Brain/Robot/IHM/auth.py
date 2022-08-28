from flask import Blueprint, render_template, request, flash
from time import sleep
from .interface import mode as MW

auth = Blueprint('auth', __name__)

@auth.route('/auto', methods=['GET', 'POST'])

def auto():
    MW.mode_wanted.Set_AUTO()
    #while (not MW.Is_Auto()):
        #sleep(1)
    
    return render_template("auto.html", boolean=True)

@auth.route('/manual', methods=['GET', 'POST'])

def manual():
    MW.mode_wanted.Set_MANUAL()
    #while (MW.Is_Auto()):
        #sleep(1)

    if request.method == 'POST':
        MW.command.Convert_Button_to_order(request.form)

    return render_template("manual.html", boolean=True)

@auth.route('/sign-up', methods=['GET', 'POST'])

def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if len(email) < 4:
            flash('Email mus be greater than 3 characters', category='error')
        elif len(firstName) <3:
            flash('First Name mus be greater than 2 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash ('Password must be at least 7 characters', category = 'error')
        else:
            flash('Account created!', category = 'success')
    return render_template("sign_up.html")