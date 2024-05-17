from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz
from flask import Flask, Response

app = Flask(__name__)

def generate_ical():
    WORKOUTS = [
        "Legs", "Push", "Pull", "Rest", 
        "Legs", "Chest Back", "Shoulder Arms", "Rest"
    ]
    
    cal = Calendar()
    cal.add('prodid', '-//My Workout Calendar//mxm.dk//')
    cal.add('version', '2.0')

    # Get the current date and find the upcoming Sunday
    today = datetime.now().date()
    days_until_sunday = (6 - today.weekday()) % 7
    start_date = today + timedelta(days=days_until_sunday)

    # Add workout events
    for i, workout in enumerate(WORKOUTS):
        event = Event()
        event.add('summary', workout)
        event_start = datetime.combine(start_date + timedelta(days=i), datetime.min.time(), pytz.UTC)
        event.add('dtstart', event_start)
        event.add('dtend', event_start + timedelta(hours=1))
        cal.add_component(event)

    return cal.to_ical()

@app.route('/api/main')
def workout_schedule():
    ical_data = generate_ical()
    return Response(ical_data, mimetype='text/calendar', headers={'Content-Disposition': 'attachment; filename="workout.ics"'})

if __name__ == "__main__":
    app.run()
