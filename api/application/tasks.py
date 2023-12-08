from application.workers import celery
from datetime import datetime, timedelta
from celery.schedules import crontab
from .database import db
from .models import User, Theatres, Shows, Bookings
import requests
from flask import current_app as app, render_template
from flask_mail import Mail, Message
import csv
import uuid
from io import StringIO

# Read mail from application context
mail = app.extensions['mail']

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # For testing
    # sender.add_periodic_task(crontab(minute="*"), emailable_report.s(), name="Scheduled for every minute")
    # Daily reminder job
    sender.add_periodic_task(crontab(minute=0, hour=17), reminder_job.s(), name="Scheduled for every day at 5PM")
    # Monthly emailable report job
    sender.add_periodic_task(crontab(day_of_month=1, hour=10, minute=0), monthly_emailable_report.s(), name="Scheduled for every month")


@celery.task()
def reminder_job():
    # Get the current date
    current_date = datetime.now().date()
    users_without_bookings = db.session.query(User, Bookings).outerjoin(
            Bookings, User.id == Bookings.userId).filter(
            Bookings.userId.is_(None) | (Bookings.createdOn != current_date)).with_entities(
            User.email, User.username).distinct().all()
    
    # The URL you want to make a POST request to
    url = 'https://chat.googleapis.com/v1/spaces/AAAAIKCiR8g/messages?key=' + app.config['WEBHOOK_KEY']
    # The data you want to send in the POST request (as a dictionary)
    # Prepare the message to list users
    headers = {'Content-Type': 'application/json'}
    userNames = ""
    
    # Append the text to each element in each tuple and join with commas
    result = [f"{user[1]}[{user[0]}]" for user in users_without_bookings]

    # Join the elements with commas
    userList = ", ".join(result)
    data = {
        'cards': [
            {
                'header': {
                    'title': 'Reminder: Book Your Show Tickets 🎟️',
                },
                'sections': [
                    {
                        'widgets': [
                            {
                                "textParagraph": {
                                    "text": 'Hi ' + userList + ','
                                }
                            },
                            {
                                'textParagraph': {
                                    'text': 'This is a friendly reminder that tickets for the upcoming show are available for booking.'
                                }
                            },
                            {
                                'textParagraph': {
                                    'text': 'To book your tickets, simply click on the link below and follow the easy steps:'
                                }
                            },
                            {
                                'buttons': [
                                    {
                                        'textButton': {
                                            'text': 'Book Tickets',
                                            'onClick': {
                                                'openLink': {
                                                    'url': 'http://localhost:8080/shows'
                                                }
                                            }
                                        }
                                    }
                                ]
                            },
                            {
                                'textParagraph': {
                                    'text': 'If you have any questions or need assistance with the booking process, please feel free to reach out to our support team.'
                                }
                            },
                            {
                                'textParagraph': {
                                    'text': 'We look forward to seeing you at the show! It\'s going to be an unforgettable experience.'
                                }
                            },
                            {
                                'textParagraph': {
                                    'text': 'Happy booking!'
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }

    # Make the POST request
    request = requests.Request('POST', url, headers=headers, json=data)
        # Prepare the request for sending
    prepared_request = request.prepare()

    # Send the request (if needed)
    response = requests.Session().send(prepared_request)

    # Check the response status code
    if response.status_code == 200:
        print("Message sent successfully to Google Chat!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")

@celery.task()
def monthly_emailable_report():
    # Get the current date
    today = datetime.now()
    # Calculate the first day of the current month
    first_day_of_current_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    # Calculate the last day of the previous month
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    # Calculate the first day of the previous month
    first_day_of_previous_month = last_day_of_previous_month.replace(day=1)
    users = db.session.query(User).all()
    monthName = first_day_of_previous_month.strftime("%B")
    for user in users:
        booking_shows = db.session.query(Shows.name, Shows.startTime, Shows.rating, Shows.price,
             db.func.sum(Bookings.count)).join(Shows, Bookings.showId == Shows.showId).filter(
                Bookings.userId == user.id).filter(
                Bookings.createdOn >= first_day_of_previous_month).filter(
                Bookings.createdOn < first_day_of_current_month).group_by(
                Shows.name, Shows.startTime, Shows.rating, Shows.price).all()
        report = render_template('monthly_report.html', monthName=monthName, user=user, booking_shows=booking_shows)
        message = Message(monthName + ' - Monthly Entertainment Report', recipients=[user.email])
        message.html = report
        mail.send(message)

@celery.task
def generate_theatre_report(user_id, theatre_id, startTime, endTime):
    user = db.session.query(User).filter(User.id == user_id).first()
    theatre = db.session.query(Theatres).filter(Theatres.theatreId == theatre_id).first()
    theatre_report_data = db.session.query(Shows.name, Shows.startTime, Shows.rating, Shows.price, db.func.sum(Bookings.count)).join(
            Shows, Bookings.showId == Shows.showId).filter(Bookings.userId == user_id).filter(
                Bookings.theatreId == theatre_id).filter(Shows.startTime >= startTime).filter(
                Shows.startTime < endTime).group_by(Shows.name, Shows.startTime, Shows.rating, Shows.price).all()
    csv_buffer = StringIO()
    fieldnames = ['Show name', 'Timing', 'Rating', 'Capacity', '#Bookings', 'Earning']
    csv_writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
    csv_writer.writeheader()
    noRecords = True
    for showName, showStartTime, showRating, showPrice, bookingCount in theatre_report_data:
        db_show_start_time_format = '%Y-%m-%d %H:%M'
        report_time_format = "%B %d, %Y  %I:%M %p"
        showTime = datetime.strptime(showStartTime, db_show_start_time_format).strftime(report_time_format)
        row = {'Show name': showName, 'Timing': showTime, 'Rating': showRating, 'Capacity': theatre.capacity,'#Bookings': bookingCount, 'Earning': showPrice * bookingCount}
        csv_writer.writerow(row)
        noRecords = False
    report = render_template('theatre_export_report.html', startTime=startTime, endTime=endTime, noRecords=noRecords)
    message = Message(theatre.name + ' - Theatre Report', recipients=[user.email])
    message.html = report
    if (not noRecords):
        message.attach(theatre.name + " - Theatre Report" + str(uuid.uuid4()) + ".csv", 'text/csv', csv_buffer.getvalue())
    mail.send(message)

@celery.task
def generate_show_bookings_report(user_id, theatre_id, show_id):
    user = db.session.query(User).filter(User.id == user_id).first()
    theatre = db.session.query(Theatres).filter(Theatres.theatreId == theatre_id).first()
    show = db.session.query(Shows).filter(Shows.theatreId == theatre_id).filter(Shows.showId == show_id).first()
    show_booking_report_data = db.session.query(Shows.name, Shows.startTime, Shows.rating,
            Bookings.createdOn, Bookings.count, Shows.price).join(Shows, Bookings.showId == Shows.showId).filter(
            Bookings.theatreId == theatre_id).filter(Bookings.showId == show_id).all()
    csv_buffer = StringIO()
    fieldnames = ['Show name', 'Timing', 'Rating', 'Booking On', '#Bookings', 'Amount']
    csv_writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
    csv_writer.writeheader()
    noRecords = True
    for showName, showStartTime, showRating, bookedOn, bookingCount, showPrice in show_booking_report_data:
        db_show_start_time_format = '%Y-%m-%d %H:%M'
        db_show_booked_on_format = '%Y-%m-%d %H:%M:%S.%f'
        report_time_format = "%B %d, %Y  %I:%M %p"
        showTime = datetime.strptime(showStartTime, db_show_start_time_format).strftime(report_time_format)
        showBookedOn = datetime.strptime(bookedOn, db_show_booked_on_format).strftime(report_time_format)
        row = {'Show name': showName, 'Timing': showTime, 'Rating': showRating, 'Booking On': showBookedOn,'#Bookings': bookingCount, 'Amount': showPrice * bookingCount}
        csv_writer.writerow(row)
        noRecords = False
    report = render_template('show_bookings_export_report.html', noRecords=noRecords, showStartTime=show.startTime)
    message = Message(theatre.name + ' - ' + show.name + ' - Show Booking Report', recipients=[user.email])
    message.html = report
    if (not noRecords):
        message.attach(theatre.name + ' - ' + show.name + " - Show Booking Report" + str(uuid.uuid4()) + ".csv", 'text/csv', csv_buffer.getvalue())
    mail.send(message)