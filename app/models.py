from app import db, login
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), index=True, unique=True)
    email = db.Column(db.String(30), index=True, unique=True)
    password = db.Column(db.String(25))
    lists = db.relationship('List', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        return self.password == password

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def get_lists(self):
        return List.query.filter(List.user_id == self.id).order_by(List.id).all()


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    listname = db.Column(db.String(30), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('Item', backref='dir', lazy='dynamic')

    def __repr__(self):
        return '<List {}>'.format(self.listname)

    def get_items(self):
        return Item.query.filter(Item.list_id == self.id).order_by(Item.id).all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itemname = db.Column(db.String(30), index=True)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))

    def __repr__(self):
        return '<Item {}>'.format(self.itemname)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
