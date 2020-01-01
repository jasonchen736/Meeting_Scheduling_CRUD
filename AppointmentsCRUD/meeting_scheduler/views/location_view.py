import json

from flask import jsonify, request
from flask.views import MethodView
from werkzeug.exceptions import BadRequest, NotFound

from meeting_scheduler.extensions import db
from meeting_scheduler.models.location import Location
from meeting_scheduler.utils.db import row_to_dict
from meeting_scheduler.utils.validation import format_valiation_errors, validate_location_request


class LocationView(MethodView):

    def __get_location_object(self, location_id, raise_error=True):
        location = Location.query.get(location_id)
        if not location and raise_error:
            raise NotFound(description='The location by that ID was not found') 
        return location

    def get(self, location_id):
        """Locations list or location detail
        """
        if location_id is None:
            # list
            locations = [row_to_dict(l) for l in Location.query.all()]
            return jsonify(locations), 200
        else:
            # detail
            location = self.__get_location_object(location_id)
            return jsonify(row_to_dict(location)), 200

    def post(self):
        """Add location
        """
        data = request.get_json()

        result = validate_location_request(data)
        if result.errors:
            message = format_valiation_errors(result.errors)
            raise BadRequest(description=message)

        location = Location(
            locality=result.document.get('locality'),
            line_1=result.document.get('line_1'),
            line_2=result.document.get('line_2'),
            postal=result.document.get('postal'),
            region=result.document.get('region'),
        )
        db.session.add(location)
        db.session.commit()

        return jsonify(row_to_dict(location)), 200

    def put(self, location_id):
        """Add or update location to ID
        """
        location = self.__get_location_object(location_id, raise_error=False)

        data = request.get_json()

        result = validate_location_request(data)
        if result.errors:
            message = format_valiation_errors(result.errors)
            raise BadRequest(description=message)

        if not location:
            location = Location(
                id=location_id,
                locality=result.document.get('locality'),
                line_1=result.document.get('line_1'),
                line_2=result.document.get('line_2'),
                postal=result.document.get('postal'),
                region=result.document.get('region'),
            )
            db.session.add(location)
        else:
            location.locality = result.document.get('locality')
            location.line_1 = result.document.get('line_1')
            location.line_2 = result.document.get('line_2')
            location.postal = result.document.get('postal')
            location.region = result.document.get('region')

        db.session.commit()

        return jsonify(row_to_dict(location)), 200

    def delete(self, location_id):
        """Delete location by ID
        """
        location = self.__get_location_object(location_id)
        db.session.delete(location)
        db.session.commit()
        return jsonify(row_to_dict(location)), 200
