from app import app
from flask_mail import Message
from app import mail
from app.pull_data import get_data
from threading import Thread
from flask import url_for, render_template
from .decorators import async_func

def adj_temp(current_temperature, min_temperature, max_temperature, feels_like, units):
    if units == 'f':
        current_temperature =  (current_temperature * 9/5) + 32
        min_temperature = (min_temperature * 9/5) + 32
        max_temperature = (max_temperature * 9/5) + 32
        feels_like = (feels_like * 9/5) + 32
    return [round(x,1) for x in [current_temperature, min_temperature, max_temperature, feels_like]]

@async_func
def send_async_func_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, user):
    sender = app.config['MAIL_USERNAME']
    recipients = user.email
    city = user.city
    lat = user.latitude
    lng = user.longitude
    units = user.units
    unit_symbol = ''
    if units == 'f':
        unit_symbol = '°F'
    elif units == 'c':
        unit_symbol = '°C'
    msg = Message(subject, sender=sender, recipients=[recipients])
    description_current, description_day, current_temperature, feels_like, min_temperature, max_temperature, humidity = get_data(lat, lng, app.config['OWM_API_KEY'])
    current_temperature, min_temperature, max_temperature, feels_like = adj_temp(current_temperature, min_temperature, max_temperature, feels_like, units)
    unsub_url = app.config['HOSTED_URL'] + '/unsub'
    darksky_url = 'https://darksky.net/poweredby/'
    text_body = (
        f'Hello, here\'s your weather update for today in {city}.\n'
        f'Today\'s Weather Overview - {description_day.capitalize()}.\n'
        f'The current temperature is {current_temperature}{unit_symbol} and it feels like {feels_like}{unit_symbol}.\n'
        f'The maximum temperautre for today is {max_temperature}{unit_symbol}.\n'
        f'The minimum temperautre for today is {min_temperature}{unit_symbol}.\n'
        f'The humidity for today is {humidity}.\n\n\n\n'
        f' Go here to unsubscribe - {unsub_url}'
        )

    msg.body = text_body
    msg.html = render_template('email.html', city=city, min_temperature=min_temperature, current_temperature=current_temperature, feels_like=feels_like,
                                        max_temperature=max_temperature, unit_symbol=unit_symbol, description_current=description_current.capitalize(),
                                        description_day=description_day.capitalize(), unsub_url=unsub_url, darksky_url=darksky_url, humidity=humidity)
    send_async_func_email(app, msg)


