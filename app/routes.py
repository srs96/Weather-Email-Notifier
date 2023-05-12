from app import app
from app.forms import DetailsForm
from flask import render_template, request, redirect, url_for, flash
from app.models import Users
from app.forms import DetailsForm
from app import db
import datetime
from app.email import send_email
from app.time_convert import convert_time
from app.geocode import lookup
import requests

def scheduled_task():
    with app.app_context():
        r = requests.get(url = 'https://simple-weather-7bta.onrender.com/')
        print(r.status_code)
        current_hour = datetime.datetime.now().hour
        current_minute = datetime.datetime.now().minute
        print('Time is', current_hour, current_minute)
        #all_u = Users.query.all()
        #for idx, i in enumerate(all_u):
        #    print(i, 'just checking database', idx)
        #Test below
        #users = Users.query.all()
        users = Users.query.filter(Users.mail_hour==current_hour, Users.mail_minute==current_minute).all()
        for idx, user in enumerate(users):
            with app.app_context():
                send_email('Today\'s Weather', user)
            print(user)
            print(idx)


app.apscheduler.add_job(func=scheduled_task, trigger='cron', minute='0, 10, 15, 20, 30, 40, 45, 60', id = str(1))

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        city = request.form['city']
        mail_time = request.form['time']
        temp_units = request.form['temp_options']
        latitude, longitude = lookup(city, app.config['GOOGLE_API_KEY'])
        mail_time = convert_time(latitude, longitude, int(mail_time))
        mail_time = mail_time.split(':')
        mail_hour = int(mail_time[0])
        mail_minute = int(mail_time[1])

        exists = Users.query.filter(Users.email == email).first()
        if not exists:
            u = Users(email=email, city=city, units=temp_units, mail_hour = mail_hour, mail_minute=mail_minute, latitude=latitude, longitude=longitude)
            db.session.add(u)
            db.session.commit()
            flash('You details were succesfully added.')
        else:
            exists.email=email
            exists.city = city
            exists.units = temp_units
            exists.mail_hour = mail_hour
            exists.mail_minute = mail_minute
            exists.latitude = latitude
            exists.longitude = longitude
            db.session.commit()
            flash('Your details were succesfully updated.')
    return render_template('index.html')

@app.route('/unsubbed')
def unsubbed():
    return render_template('unsubbed.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


@app.route('/unsub', methods = ['GET', 'POST'])
def unsub():
    if request.method == 'POST':
        email = request.form['email']
        Users.query.filter(Users.email==email).delete()
        db.session.commit()
        flash('Your details, if stored, were succesfully deleted.')
    return render_template('unsub.html')





