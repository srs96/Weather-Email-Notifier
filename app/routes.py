from app import app
from app.forms import DetailsForm
from flask import render_template, request, redirect, url_for, flash
from app.models import User
from app.forms import DetailsForm
from app import db
import datetime
from app.email import send_email
from app.time_convert import convert_time



def scheduled_task():
    current_hour = datetime.datetime.now().hour
    current_minute = datetime.datetime.now().minute
    print('Time is', current_hour, current_minute)
    all_u = User.query.all()
    for i in all_u:
        print(i)
    #users = User.query.all()
    users = User.query.filter(User.mail_hour==current_hour, User.mail_minute==current_minute).all()
    for idx, user in enumerate(users):
        with app.test_request_context():
            send_email('Today\'s Weather', app.config['ADMINS'][0], user, url_for('unsub', _external=True))
        print(idx)


app.apscheduler.add_job(func=scheduled_task, trigger='cron', minute='0, 15, 30, 45', id = str(1))
#app.apscheduler.add_job(func=scheduled_task, trigger='cron', second='0, 10, 20, 30, 40, 50', id = str(1))

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        city = request.form['city']
        mail_time = request.form['time']
        temp_units = request.form['temp_options']
        mail_time = convert_time(city, int(mail_time))
        mail_time = mail_time.split(':')
        mail_hour = int(mail_time[0])
        mail_minute = int(mail_time[1])
        exists = User.query.filter(User.email == email).first()
        if not exists:
            u = User(email=email, city=city, units=temp_units, mail_hour = mail_hour, mail_minute=mail_minute)
            db.session.add(u)
            db.session.commit()
            flash('You details were succesfully added.')
        else:
            exists.email=email
            exists.city = city
            exists.units = temp_units
            exists.mail_hour = mail_hour
            exists.mail_minute = mail_minute
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
        User.query.filter(User.email==email).delete()
        db.session.commit()
        flash('Your details, if stored, were succesfully deleted.')
    return render_template('unsub.html')





