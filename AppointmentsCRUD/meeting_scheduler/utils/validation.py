from datetime import datetime
from cerberus import Validator

from meeting_scheduler.models.location import Location
from meeting_scheduler.models.person import Person


to_datetime = lambda s: datetime.strptime(s, '%Y-%m-%d %H:%M:%S')

class MeetingValidator(Validator):

    def _validate_location_exists(self, location_exists, field, value):
        """ Validate location exists

        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
        """
        found = Location.query.get(value)
        if location_exists and not found:
            self._error(field, 'Must be an existing location')

    def _validate_people_exist(self, people_exist, field, value):
        """ Validate people exist

        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
        """
        found = Person.query.filter(Person.id.in_(value)).all()
        if people_exist and len(found) != len(value):
            self._error(field, 'One or more person does not exist')


def format_valiation_errors(errors):
    """ Format validation errors into readable string
    """
    return "; ".join(['{}: {}'.format(k, ', '.join(v)) for k, v in errors.items()])

def validate_location_request(data):
    """ Validate location request fields
    """
    schema = {
        'locality': {'type': 'string', 'required': True},
        'line_1': {'type': 'string', 'required': True},
        'line_2': {'type': 'string'},
        'postal': {'type': 'string', 'required': True},
        'region': {'type': 'string', 'required': True},
    }
    validator = Validator()
    validator.validate(data, schema)
    return validator

def validate_meeting_request(data):
    """ Validate meeting request fields
    """
    schema = {
        'start_time': {'type': 'datetime', 'coerce': to_datetime, 'required': True},
        'end_time': {'type': 'datetime', 'coerce': to_datetime, 'required': True},
        'location_id': {'type': 'integer', 'location_exists': True, 'required': True},
        'people': {'type': 'list', 'schema': {'type': 'integer'}, 'people_exist': True, 'minlength': 2, 'required': True},
    }
    validator = MeetingValidator()
    validator.validate(data, schema)
    return validator

def validate_person_request(data):
    """ Validate person request fields
    """
    schema = {
        'first_name': {'type': 'string'},
        'last_name': {'type': 'string'},
    }
    validator = Validator(require_all=True)
    validator.validate(data, schema)
    return validator
