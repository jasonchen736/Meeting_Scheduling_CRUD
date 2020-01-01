from meeting_scheduler.views.location_view import LocationView
from meeting_scheduler.views.meeting_view import MeetingView
from meeting_scheduler.views.person_view import PersonView


def add_urls(app):
    location_view = LocationView.as_view('location_view')
    app.add_url_rule('/locations/', defaults={'location_id': None}, view_func=location_view, methods=['GET'])
    app.add_url_rule('/locations/', view_func=location_view, methods=['POST'])
    app.add_url_rule('/locations/<int:location_id>', view_func=location_view, methods=['GET', 'PUT', 'DELETE'])

    meeting_view = MeetingView.as_view('meeting_view')
    app.add_url_rule('/meetings/', defaults={'meeting_id': None}, view_func=meeting_view, methods=['GET'])
    app.add_url_rule('/meetings/', view_func=meeting_view, methods=['POST'])
    app.add_url_rule('/meetings/<int:meeting_id>', view_func=meeting_view, methods=['GET', 'PUT', 'DELETE'])

    person_view = PersonView.as_view('person_view')
    app.add_url_rule('/persons/', defaults={'person_id': None}, view_func=person_view, methods=['GET'])
    app.add_url_rule('/persons/', view_func=person_view, methods=['POST'])
    app.add_url_rule('/persons/<int:person_id>', view_func=person_view, methods=['GET', 'PUT', 'DELETE'])
