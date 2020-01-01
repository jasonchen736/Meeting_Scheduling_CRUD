import json

from flask import jsonify, request
from flask.views import MethodView
from werkzeug.exceptions import BadRequest, NotFound

from meeting_scheduler.extensions import db
from meeting_scheduler.models.person import Person
from meeting_scheduler.utils.db import row_to_dict
from meeting_scheduler.utils.validation import format_valiation_errors, validate_person_request


class PersonView(MethodView):

    def __get_person_object(self, person_id, raise_error=True):
        person = Person.query.get(person_id)
        if not person and raise_error:
            raise NotFound(description='The person by that ID was not found') 
        return person

    def get(self, person_id):
        """Persons list or person detail
        """
        if person_id is None:
            # list
            persons = [row_to_dict(p) for p in Person.query.all()]
            return jsonify(persons), 200
        else:
            # detail
            person = self.__get_person_object(person_id)
            return jsonify(row_to_dict(person)), 200

    def post(self):
        """Add person
        """
        data = request.get_json()

        result = validate_person_request(data)
        if result.errors:
            message = format_valiation_errors(result.errors)
            raise BadRequest(description=message)

        person = Person(
            first_name=result.document.get('first_name'),
            last_name=result.document.get('last_name'),
        )
        db.session.add(person)
        db.session.commit()

        return jsonify(row_to_dict(person)), 200

    def put(self, person_id):
        """Add or update person to ID
        """
        person = self.__get_person_object(person_id, raise_error=False)

        data = request.get_json()

        result = validate_person_request(data)
        if result.errors:
            message = format_valiation_errors(result.errors)
            raise BadRequest(description=message)

        if not person:
            person = Person(
                id=person_id,
                first_name=result.document.get('first_name'),
                last_name=result.document.get('first_name'),
            )
            db.session.add(person)
        else:
            person.first_name = result.document.get('first_name')
            person.last_name = result.document.get('last_name')

        db.session.commit()

        return jsonify(row_to_dict(person)), 200

    def delete(self, person_id):
        """Delete person by ID
        """
        person = self.__get_person_object(person_id)
        db.session.delete(person)
        db.session.commit()
        return jsonify(row_to_dict(person)), 200
