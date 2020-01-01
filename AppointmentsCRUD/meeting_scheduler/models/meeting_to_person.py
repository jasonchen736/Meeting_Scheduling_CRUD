from meeting_scheduler.extensions import db


class MeetingToPerson(db.Model):
    __tablename__ = 'meeting_to_person'
    __table_args__ = (db.UniqueConstraint('meeting_id', 'person_id'),)

    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    meeting = db.relationship('Meeting')
    person = db.relationship('Person')
