from meeting_scheduler.extensions import db


class Location(db.Model):
    __tablename__ = 'location'

    id = db.Column(db.Integer, primary_key=True)
    locality = db.Column(db.String, nullable=False)
    line_1 = db.Column(db.String, nullable=False)
    line_2 = db.Column(db.String)
    postal = db.Column(db.String, nullable=False)
    region = db.Column(db.String, nullable=False)
