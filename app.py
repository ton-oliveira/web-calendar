import sys
import datetime
from flask import Flask
from sqlalchemy import or_
from models import WebCalendar
from flask_restful import Api, Resource, inputs, reqparse, marshal_with, fields, abort

app = Flask(__name__)
api = Api(app)

TODOS = {"message": "The event has been added!",
         "event": "????",
         "date": "????"
         }

parser = reqparse.RequestParser()

resource_fields = {
    'id': fields.Integer,
    'event': fields.String,
    'date': fields.String
}

parser.add_argument(
    "event",
    type=str,
    help="The event name is required!",
    required=True
)

parser.add_argument(
    'date',
    type=inputs.date,
    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
    required=True
)

parser.add_argument(
    'start_time',
    type=inputs.date,
    required=False
)

parser.add_argument(
    'end_time',
    type=inputs.date,
    required=False
)


class EventAdd(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = parser.parse_args()
        calendar = WebCalendar(event=args['event'], date=args['date'].date())
        calendar.save()

        success = {"message": "The event has been added!",
                   "event": args['event'],
                   "date": str(args['date'].date())
                   }
        return success, 200

    def get(self):
        args = parser.parse_args()
        if args['start_time'] is not None or args['end_time'] is not None:
            query = WebCalendar.query.filter(or_(WebCalendar.date.like(args['start_time'].date()),
                                                 WebCalendar.date.like(args['end_time'].date())))

            response = [{'id': var.id, 'event': var.event, 'date': str(var.date)} for var in query]
            return response
        else:
            event = WebCalendar.query.all()
            response = [{'id': var.id, 'event': var.event, 'date': str(var.date)} for var in event]

            return response


class EventsToday(Resource):
    @marshal_with(resource_fields)
    def get(self):
        event = WebCalendar.query.filter_by(date=datetime.date.today())
        response = [{'id': var.id, 'event': var.event, 'date': str(var.date)} for var in event]

        return response


class IdEvents(Resource):
    @marshal_with(resource_fields)
    def get(self, event_id):
        try:
            query = WebCalendar.query.filter(WebCalendar.id.like(event_id)).first()
            if query is None:
                abort(404, "The event doesn't exist!")
            response = {
                'id': query.id,
                'event': query.event,
                'date': str(query.date)
            }
            return response
        except AttributeError:
            return {
                "message": "The event doesn't exist!"
            }

    def delete(self, event_id):
        try:
            query = WebCalendar.query.filter(WebCalendar.id.like(event_id)).first()
            query.delete()
            return {
                "message": "The event has been deleted!"
            }
        except AttributeError:
            return {
                "message": "The event doesn't exist!"
            }


api.add_resource(IdEvents, '/event/<int:id>')
api.add_resource(EventAdd, '/event')
api.add_resource(EventsToday, '/event/today')

# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run(debug=True)
