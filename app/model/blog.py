from app import db
from app.model import blog
from datetime import datetime

class Blog(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    slug = db.Column(db.String(250), index=True, nullable=False, unique=True)
    title = db.Column(db.String(250), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    views = db.Column(db.Integer, nullable=False, default=0)
    image_file = db.Column(db.String(100), nullable=False, default='default.jpg')
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Blog('{self.title}','{self.date_posted}')"