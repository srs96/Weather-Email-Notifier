from app import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    city = db.Column(db.String(120), index=True)
    latitude = db.Column(db.Float, index=True)
    longitude = db.Column(db.Float, index=True)
    units = db.Column(db.String(1), index=True)
    mail_hour = db.Column(db.Integer, index=True)
    mail_minute = db.Column(db.Integer, index=True)

    def __repr__(self):
        return f'{self.email}, {self.city}, {self.units}, {self.mail_hour}, {self.mail_minute}, {self.latitude}, {self.longitude}'
