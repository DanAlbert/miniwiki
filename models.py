from google.appengine.ext import db


class Page(db.Model):
    title = db.StringProperty()
    text = db.TextProperty()
    last_edited = db.DateTimeProperty(auto_now=True)
