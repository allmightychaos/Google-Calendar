from icalendar import Calendar, Event
from datetime import datetime, timedelta, time
import pytz
from flask import Flask, Response

app = Flask(__name__)

def generate_ical():
    WORKOUTS = [
        ("Legs", "wisteria"), 
        ("Push", "sage"), 
        ("Pull", "peacock"), 
        ("Rest", "graphite"), 
        ("Legs + Abs", "wisteria"), 
        ("Chest + Back", "peacock"), 
        ("Shoulder + Arms", "sage"), 
        ("Rest", "graphite")
    ]
    
    cal = Calendar()
    cal.add('prodid', '-//My Workout Calendar//mxm.dk//')
    cal.add('version', '2.0')

    # Get the current date and find the upcoming Sunday
    today = datetime.now().date()
    days_until_sunday = (6 - today.weekday()) % 7
    start_date = today + timedelta(days=days_until_sunday)

    # Define the time zone and event start/end times
    tz = pytz.timezone('Europe/Berlin')
    event_start_time = time(5, 30)
    event_end_time = time(7, 30)

    # Add workout events
    for i, (workout, color) in enumerate(WORKOUTS):
        event = Event()
        event.add('summary', workout)
        event.add('categories', [color])
        event_start = tz.localize(datetime.combine(start_date + timedelta(days=i), event_start_time))
        event_end = tz.localize(datetime.combine(start_date + timedelta(days=i), event_end_time))
        event.add('dtstart', event_start)
        event.add('dtend', event_end)
        cal.add_component(event)

    return cal.to_ical()

@app.route('/api/workout_schedule')
def workout_schedule():
    ical_data = generate_ical()
    return Response(ical_data, mimetype='text/calendar', headers={'Content-Disposition': 'attachment; filename="workout_schedule.ics"'})

