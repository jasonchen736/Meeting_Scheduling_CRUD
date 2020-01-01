import json

from flask import jsonify, request
from flask.views import MethodView
from werkzeug.exceptions import BadRequest, NotFound

from meeting_scheduler.extensions import db
from meeting_scheduler.models.meeting import Meeting
from meeting_scheduler.models.meeting_to_person import MeetingToPerson
from meeting_scheduler.utils.db import row_to_dict
from meeting_scheduler.utils.validation import format_valiation_errors, validate_meeting_request


class MeetingView(MethodView):

    def __get_meeting_object(self, meeting_id, raise_error=True):
        """Query for meeting by ID, optionally raise 404
        """
        meeting = Meeting.query.get(meeting_id)
        if not meeting and raise_error:
            raise NotFound(description='The meeting by that ID was not found') 
        return meeting

    def __get_meeting_dict(self, meeting):
        """Convert meeting object and associations to dict
        """
        meeting_dict = row_to_dict(meeting)
        del(meeting_dict['location_id'])
        meeting_dict['location'] = row_to_dict(meeting.location)
        meeting_dict['people'] = [row_to_dict(l.person) for l in meeting.meeting_to_persons]
        return meeting_dict

    def get(self, meeting_id):
        """Meetings list or meeting detail
        """
        if meeting_id is None:
            # list
            meetings = [self.__get_meeting_dict(m) for m in Meeting.query.all()]
            return jsonify(meetings), 200
        else:
            # detail
            meeting = self.__get_meeting_object(meeting_id)
            return jsonify(self.__get_meeting_dict(meeting)), 200

    def post(self):
        """Add meeting
        """
        data = request.get_json()

        result = validate_meeting_request(data)
        if result.errors:
            message = format_valiation_errors(result.errors)
            raise BadRequest(description=message)

        meeting = Meeting(
            start_time=result.document.get('start_time'),
            end_time=result.document.get('end_time'),
            location_id=result.document.get('location_id'),
        )
        db.session.add(meeting)
        db.session.flush()

        for person_id in result.document.get('people'):
            link = MeetingToPerson(
                meeting_id=meeting.id,
                person_id=person_id,
            )
            meeting.meeting_to_persons.append(link)

        db.session.commit()

        return jsonify(self.__get_meeting_dict(meeting)), 200

    def put(self, meeting_id):
        """Add or update meeting to ID
        """
        meeting = self.__get_meeting_object(meeting_id, raise_error=False)

        data = request.get_json()

        result = validate_meeting_request(data)
        if result.errors:
            message = format_valiation_errors(result.errors)
            raise BadRequest(description=message)

        if not meeting:
            meeting = Meeting(
                id=meeting_id,
                start_time=result.document.get('start_time'),
                end_time=result.document.get('end_time'),
                location_id=result.document.get('location_id'),
            )
            db.session.add(meeting)
            db.session.flush()

            for person_id in result.document.get('people'):
                link = MeetingToPerson(
                    meeting_id=meeting.id,
                    person_id=person_id,
                )
                meeting.meeting_to_persons.append(link)
        else:
            meeting.start_time = result.document.get('start_time')
            meeting.end_time = result.document.get('end_time')
            meeting.location_id = result.document.get('location_id')

            for link in meeting.meeting_to_persons:
                db.session.delete(link)

            db.session.flush()

            for person_id in data.get('people'):
                link = MeetingToPerson(
                    meeting_id=meeting.id,
                    person_id=person_id,
                )
                meeting.meeting_to_persons.append(link)

        db.session.commit()

        return jsonify(self.__get_meeting_dict(meeting)), 200

    def delete(self, meeting_id):
        """Delete meeting by ID
        """
        meeting = self.__get_meeting_object(meeting_id)
        response = self.__get_meeting_dict(meeting)
        db.session.delete(meeting)
        db.session.commit()
        return jsonify(response), 200
