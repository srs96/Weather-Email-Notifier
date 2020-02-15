from app import app
from flask_mail import Message
from app import mail
from app.pull_data import get_data
from threading import Thread
from flask import url_for, render_template
from .decorators import async

def adj_temp(current_temperature, min_temperature, max_temperature, feels_like, units):
    current_temperature -= 273
    min_temperature -= 273
    max_temperature -= 273
    feels_like -= 273
    if units == 'f':
        current_temperature =  (current_temperature * 9/5) + 32
        min_temperature = (min_temperature * 9/5) + 32
        max_temperature = (max_temperature * 9/5) + 32
        feels_like = (feels_like * 9/5) + 32
    return [round(x,1) for x in [current_temperature, min_temperature, max_temperature, feels_like]]

@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, user):
    recipients = user.email
    city = user.city
    units = user.units
    unit_symbol = ''
    if units == 'f':
        unit_symbol = '°F'
    elif units == 'c':
        unit_symbol = '°C'
    msg = Message(subject, sender=sender, recipients=[recipients])
    if get_data(city):
        description, current_temperature, min_temperature, max_temperature, feels_like = get_data(city)
        current_temperature, min_temperature, max_temperature, feels_like = adj_temp(current_temperature, min_temperature, max_temperature, feels_like, units)
        text_body = (
            f'Hello, here\'s your weather update for today in {city}.\n'
            f'Weather Overview - {description.capitalize()}.\n'
            f'The current temperature is {current_temperature}{unit_symbol} and it feels like {feels_like}{unit_symbol}.\n'
            f'The maximum temperautre for today is {max_temperature}{unit_symbol}.\n'
            f'The minimum temperautre for today is {min_temperature}{unit_symbol}.\n\n\n\n'
            f' Go here to unsubscribe - https://calm-fortress-35099.herokuapp.com/unsub'
            )

        msg.body = text_body
        msg.html = render_template('email.html', city=city, min_temperature=min_temperature, current_temperature=current_temperature, feels_like=feels_like,
                                            max_temperature=max_temperature, unit_symbol=unit_symbol, description=description.capitalize())
        send_async_email(app, msg)


