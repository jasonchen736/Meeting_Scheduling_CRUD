from meeting_scheduler.extensions import db
from meeting_scheduler.models.meeting_to_person import MeetingToPerson
from meeting_scheduler.models.person import Person


class Meeting(db.Model):
    __tablename__ = 'meeting'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))

    location = db.relationship('Location')
    meeting_to_persons = db.relationship('MeetingToPerson', cascade='all, delete, delete-orphan')

    @property
    def people(self):
        people = []
        for link in self.meeting_to_persons:
            people.append(link.person)
        return people
