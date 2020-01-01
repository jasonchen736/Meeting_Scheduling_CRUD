from datetime import datetime, timedelta

from meeting_scheduler import app, db
from meeting_scheduler.extensions import db
from meeting_scheduler.models.location import Location
from meeting_scheduler.models.meeting import Meeting
from meeting_scheduler.models.meeting_to_person import MeetingToPerson
from meeting_scheduler.models.person import Person


with app.app_context():
    db.create_all()

    # init some locations
    locations = [
        {
        'locality': 'New York',
        'line_1': '123 Main St',
        'line_2': '5th Floor',
        'postal': '11111',
        'region': 'New York',
        },
        {
        'locality': 'New York',
        'line_1': '111 5th Ave',
        'postal': '22222',
        'region': 'New York',
        },
    ]
    for l in locations:
        location = Location(**l)
        db.session.add(location)

    # init some people
    persons = [
        {
        'first_name': 'Adam',
        'last_name': 'Smith',
        },
        {
        'first_name': 'Michael',
        'last_name': 'Jackson',
        },
        {
        'first_name': 'Mr',
        'last_name': 'Ed',
        },
    ]
    for p in persons:
        person = Person(**p)
        db.session.add(person)

    db.session.flush()

    # init some meetings
    meeting_1 = Meeting(
        start_time=datetime.now() + timedelta(hours=24),
        end_time=datetime.now() + timedelta(hours=25),
        location_id=1,
    )
    db.session.add(meeting_1)
    db.session.flush()
    person_1 = MeetingToPerson(
        meeting_id=meeting_1.id,
        person_id=1,
    )
    person_2 = MeetingToPerson(
        meeting_id=meeting_1.id,
        person_id=2,
    )
    meeting_1.meeting_to_persons.append(person_1)
    meeting_1.meeting_to_persons.append(person_2)

    meeting_2 = Meeting(
        start_time=datetime.now() + timedelta(hours=24),
        end_time=datetime.now() + timedelta(hours=25),
        location_id=1,
    )
    db.session.add(meeting_2)
    db.session.flush()
    person_1 = MeetingToPerson(
        meeting_id=meeting_2.id,
        person_id=1,
    )
    person_2 = MeetingToPerson(
        meeting_id=meeting_2.id,
        person_id=2,
    )
    person_3 = MeetingToPerson(
        meeting_id=meeting_2.id,
        person_id=3,
    )
    meeting_2.meeting_to_persons.append(person_1)
    meeting_2.meeting_to_persons.append(person_2)
    meeting_2.meeting_to_persons.append(person_3)

    db.session.commit()
