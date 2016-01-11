from database import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    access_keys = db.relationship('AccessKey',backref='owner',lazy='dynamic')
    
class AccessKey(db.Model):
    __tablename__ = 'accesskeys'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String)
    owner_id = db.Column(db.Integer,db.ForeignKey('users.id'))