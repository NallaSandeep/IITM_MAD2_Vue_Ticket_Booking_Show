from datetime import datetime

from flask import request, jsonify
from flask_restful import Resource, fields, marshal_with, reqparse
from .models import User, Theatres, Shows, Bookings
from .database import db
from .validation import BusinessValidationError, InputValidationError
from .validation import handle_business_validation_error, handle_input_validation_error
from application import tasks
from sqlalchemy import desc
from .auth import token_required
from flask import current_app as app
from .cache import cache

theatre_fields = {
    'userId': fields.Integer,
    'theatreId': fields.Integer,
    'status': fields.String,
    'name': fields.String,
    'area': fields.String,
    'city': fields.String,
    'capacity': fields.Integer
}

show_fields = {
    'userId': fields.Integer,
    'theatreId': fields.Integer,
    'theatreName': fields.String,
    'city': fields.String,
    'showId': fields.Integer,
    'status': fields.String,
    'name': fields.String,
    'rating': fields.Integer,
    'startTime': fields.String,
    'endTime': fields.String,
    'tags': fields.String,
    'price': fields.Integer,
    'availableSeats': fields.Integer
}

booking_fields = {
    'bookingId': fields.Integer,
    'theatreId': fields.Integer,
    'theatreName': fields.String,
    'theatreArea': fields.String,
    'theatreCity': fields.String,
    'showId': fields.Integer,
    'showStartTime': fields.String,
    'count': fields.Integer
}

page_fields = {
    'itemCount': fields.Integer,
    'pageCount': fields.Integer
}

create_theatre_parser = reqparse.RequestParser()
create_theatre_parser.add_argument('name')
create_theatre_parser.add_argument('area')
create_theatre_parser.add_argument('city')
create_theatre_parser.add_argument('capacity')

update_theatre_parser = reqparse.RequestParser()
update_theatre_parser.add_argument('name')
update_theatre_parser.add_argument('area')
update_theatre_parser.add_argument('city')
update_theatre_parser.add_argument('capacity')

create_show_parser = reqparse.RequestParser()
create_show_parser.add_argument('name')
create_show_parser.add_argument('rating')
create_show_parser.add_argument('startTime')
create_show_parser.add_argument('endTime')
create_show_parser.add_argument('tags')
create_show_parser.add_argument('price')

update_show_parser = reqparse.RequestParser()
update_show_parser.add_argument('name')
update_show_parser.add_argument('rating')
update_show_parser.add_argument('startTime')
update_show_parser.add_argument('endTime')
update_show_parser.add_argument('tags')
update_show_parser.add_argument('price')

create_booking_parser = reqparse.RequestParser()
create_booking_parser.add_argument('count')


class Page:
    def __init__(self):
        self.pageCount = 0
        self.itemCount = 0

class TheatresApi(Resource):

    @marshal_with(theatre_fields)
    @token_required("admin")
    def get(current_user, self, user_id):
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('size', 8))
        if page < 1:
            raise BusinessValidationError(400, 'TRA01', 'page should be either null or greater than 0')
        if page_size < 2:
            raise BusinessValidationError(400, 'TRA02', 'page size should be either null or at least 1')
        start = (page -1) * page_size
        theatres = db.session.query(Theatres).filter(Theatres.userId == user_id).filter(Theatres.status == 'ACTIVE').order_by(
            Theatres.updatedOn.desc()).offset(start).limit(page_size).all()
        return theatres

class TheatrePagesApi(Resource):

    @marshal_with(page_fields)
    @token_required("admin")
    def get(current_user, self, user_id):
        page_size = int(request.args.get('size', 8))
        if page_size < 2:
            raise BusinessValidationError(400, 'TRA02', 'page size should be either null or at least 1')
        theatresCount = db.session.query(Theatres).filter(Theatres.userId == user_id).filter(Theatres.status == 'ACTIVE').count()
        import math
        pageCount = math.ceil(theatresCount/page_size)
        page = Page()
        page.pageCount = pageCount
        page.itemCount = theatresCount
        return page

class TheatreReportApi(Resource):

    @token_required("admin")
    def post(current_user, self, user_id, theatre_id):
        startTime = request.args.get('startTime')
        endTime = request.args.get('endTime')
        tasks.generate_theatre_report.apply_async(args=[user_id, theatre_id, startTime, endTime])
        return jsonify({'message': 'Report generation started. Check your email once it is done.'})
        
class TheatreApi(Resource):

    @marshal_with(theatre_fields)
    @token_required("admin", "user")
    def get(current_user, self, user_id, theatre_id):
        theatre = db.session.query(Theatres).filter(Theatres.theatreId == theatre_id).first()
        if theatre:
            return theatre
        else:
            raise InputValidationError(404, 'Theatre not found')

    @marshal_with(theatre_fields)
    @token_required("admin")
    def put(current_user, self, user_id, theatre_id):
        args = update_theatre_parser.parse_args()
        name = args.get('name', None)
        area = args.get('area', None)
        city = args.get('city', None)
        capacity = args.get('capacity', None)
        updatedOn = datetime.now()
        if name is None:
            raise BusinessValidationError(400, 'TRU01', 'Theatre name is required')
        if area is None:
            raise BusinessValidationError(400, 'TRU02', 'Theatre Area is required')
        if city is None:
            raise BusinessValidationError(400, 'TRU03', 'Theatre City is required')
        if capacity is None:
            raise BusinessValidationError(400, 'TRU04', 'Theatre Capacity is required')
        theatre = db.session.query(Theatres).filter(Theatres.userId == user_id).filter(Theatres.theatreId == theatre_id).first()
        if theatre is None:
            raise InputValidationError(404, 'Theatre not found')
        theatre.name = name
        theatre.area = area
        theatre.city = city
        theatre.capacity = capacity
        theatre.updatedOn = updatedOn
        db.session.add(theatre)
        db.session.commit()
        return theatre, 200

    @token_required("admin")
    def delete(current_user, self, user_id, theatre_id):
        theatre = db.session.query(Theatres).filter(Theatres.userId == user_id).filter(
            Theatres.theatreId == theatre_id).filter(Theatres.status == 'ACTIVE').first()
        if theatre:
            theatre.status = 'DELETED'
            db.session.add(theatre)
            db.session.commit()
        else:
            raise InputValidationError(404, 'Theatre is not found')
        return "Successfully Deleted", 200

    @marshal_with(theatre_fields)
    @token_required("admin")
    def post(current_user, self, user_id):
        args = create_theatre_parser.parse_args()
        name = args.get('name', None)
        area = args.get('area', None)
        city = args.get('city', None)
        capacity = args.get('capacity', None)
        status = "ACTIVE"
        createdOn = datetime.now()
        updatedOn = createdOn
        if name is None:
            raise BusinessValidationError(400, 'TRC01', 'Theatre name is required')
        if area is None:
            raise BusinessValidationError(400, 'TRC02', 'Theatre Area is required')
        if city is None:
            raise BusinessValidationError(400, 'TRC03', 'Theatre City is required')
        if capacity is None:
            raise BusinessValidationError(400, 'TRC04', 'Theatre Capacity is required')
        new_theatre = Theatres(name=name, area=area, city=city,
         capacity=capacity,status=status,createdOn=createdOn,updatedOn=updatedOn,userId=user_id)
        db.session.add(new_theatre)
        db.session.commit()
        return new_theatre, 201

class ShowsApi(Resource):

    @marshal_with(show_fields)
    @token_required("admin", "user")
    def get(current_user, self):
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('size', 8))
        startTime = request.args.get('startTime', None)
        endTime = request.args.get('endTime', None)
        if page < 1:
            raise BusinessValidationError(400, 'SHA01', 'page should be either null or greater than 0')
        if page_size < 2:
            raise BusinessValidationError(400, 'SHA02', 'page size should be either null or at least 1')
        start = (page -1) * page_size
        @cache.memoize(timeout=100)
        def getShowsData(startTime, endTime, start, page_size):
            if(startTime is not None and endTime is not None):
                if(startTime > endTime):
                    raise BusinessValidationError(400, 'SHA03', 'startTime can\'t be greater than endTime')
                shows = db.session.query(Shows).filter(Shows.status == 'ACTIVE').filter(
                    Shows.startTime >= startTime).filter(Shows.startTime < endTime).order_by(
                    Shows.updatedOn.desc()).offset(start).limit(page_size).all()
            else:
                shows = db.session.query(Shows).filter(Shows.status == 'ACTIVE').order_by(
                    Shows.updatedOn.desc()).offset(start).limit(page_size).all()
            return shows
        return getShowsData(startTime, endTime, start, page_size)


class ShowPagesApi(Resource):

    @marshal_with(page_fields)
    @token_required("admin", "user")
    def get(current_user, self):
        page_size = int(request.args.get('size', 8))
        startTime = request.args.get('startTime', None)
        endTime = request.args.get('endTime', None)
        if page_size < 2:
            raise BusinessValidationError(400, 'TRA02', 'page size should be either null or at least 1')
        if(startTime is not None and endTime is not None):
            if(startTime > endTime):
                raise BusinessValidationError(400, 'SHA03', 'startTime can\'t be greater than endTime')
            showCount = db.session.query(Shows).filter(Shows.status == 'ACTIVE').filter(
                Shows.startTime >= startTime).filter(Shows.startTime < endTime).count()
        else:
            showCount = db.session.query(Shows).filter(Shows.status == 'ACTIVE').count()
        import math
        pageCount = math.ceil(showCount/page_size)
        page = Page()
        page.pageCount = pageCount
        page.itemCount = showCount
        return page
        
class UserShowsApi(Resource):

    @marshal_with(show_fields)
    @token_required("admin")
    def get(current_user, self, user_id, theatre_id):
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('size', 8))
        startTime = request.args.get('startTime', None)
        endTime = request.args.get('endTime', None)
        if page < 1:
            raise BusinessValidationError(400, 'SHA01', 'page should be either null or greater than 0')
        if page_size < 2:
            raise BusinessValidationError(400, 'SHA02', 'page size should be either null or at least 1')
        start = (page -1) * page_size
        if(startTime is not None and endTime is not None):
            if(startTime > endTime):
                raise BusinessValidationError(400, 'SHA03', 'startTime can\'t be greater than endTime')
            shows = db.session.query(Shows).filter(Shows.userId == user_id).filter(
                Shows.theatreId == theatre_id).filter(Shows.status == 'ACTIVE').filter(
                Shows.startTime >= startTime).filter(Shows.startTime < endTime).order_by(
                Shows.updatedOn.desc()).offset(start).limit(page_size).all()
                
        else:
            shows = db.session.query(Shows).filter(Shows.userId == user_id).filter(
                Shows.theatreId == theatre_id).filter(Shows.status == 'ACTIVE').order_by(
                Shows.updatedOn.desc()).offset(start).limit(page_size).all()
        return shows

class UserShowsPageApi(Resource):

    @marshal_with(page_fields)
    @token_required("admin")
    def get(current_user, self, user_id, theatre_id):
        page_size = int(request.args.get('size', 8))
        startTime = request.args.get('startTime', None)
        endTime = request.args.get('endTime', None)
        if page_size < 2:
            raise BusinessValidationError(400, 'SHA02', 'page size should be either null or at least 1')
        if(startTime is not None and endTime is not None):
            if(startTime > endTime):
                raise BusinessValidationError(400, 'SHA03', 'startTime can\'t be greater than endTime')
            showCount = db.session.query(Shows).filter(Shows.userId == user_id).filter(
                Shows.theatreId == theatre_id).filter(Shows.status == 'ACTIVE').filter(
                Shows.startTime >= startTime).filter(Shows.startTime < endTime).count()
        else:
            showCount = db.session.query(Shows).filter(Shows.userId == user_id).filter(
                Shows.theatreId == theatre_id).filter(Shows.status == 'ACTIVE').count()
        import math
        pageCount = math.ceil(showCount/page_size)
        page = Page()
        page.pageCount = pageCount
        page.itemCount = showCount
        return page

class ShowApi(Resource):

    @marshal_with(show_fields)
    @token_required("admin", "user")
    def get(current_user, self, user_id, theatre_id, show_id):
        show = db.session.query(Shows).filter(
            Shows.theatreId == theatre_id).filter(Shows.showId == show_id).first()
        if show:
            return show
        else:
            raise InputValidationError(404, 'Show not found')

    @marshal_with(show_fields)
    @token_required("admin")
    def put(current_user, self, user_id, theatre_id, show_id):
        theatre = db.session.query(Theatres).filter(Theatres.userId == user_id).filter(Theatres.theatreId == theatre_id).first()
        if theatre is None:
            raise InputValidationError(404, 'Theatre not found')
        args = update_show_parser.parse_args()
        name = args.get('name', None)
        rating = args.get('rating', None)
        startTime = args.get('startTime', None)
        endTime = args.get('endTime', None)
        tags = args.get('tags', None)
        price = args.get('price', None)
        updatedOn = datetime.now()
        if name is None:
            raise BusinessValidationError(400, 'SHU01', 'Show name is required')
        if rating is None:
            raise BusinessValidationError(400, 'SHU02', 'Show Rating is required')
        if startTime is None:
            raise BusinessValidationError(400, 'SHU03', 'Show Start time is required')
        if endTime is None:
            raise BusinessValidationError(400, 'SHU04', 'Show End time is required')
        if tags is None:
            raise BusinessValidationError(400, 'SHU05', 'Show Tags are required')
        if price is None:
            raise BusinessValidationError(400, 'SHU06', 'Show Price is required')    
        show = db.session.query(Shows).filter(Shows.userId == user_id).filter(
            Shows.theatreId == theatre_id).filter(Shows.showId == show_id).first()
        if show is None:
            raise InputValidationError(404, 'Show not found')
        show.name = name
        show.rating = rating
        show.startTime = startTime
        show.endTime = endTime
        show.tags = tags
        show.price = price
        show.theatreName = theatre.name
        show.city = theatre.city
        show.availableSeats = theatre.capacity
        show.updatedOn = updatedOn
        db.session.add(show)
        db.session.commit()
        return show, 200

    @token_required("admin")
    def delete(current_user, self, user_id, theatre_id, show_id):
        show = db.session.query(Shows).filter(Shows.userId == user_id).filter(
            Shows.theatreId == theatre_id).filter(Shows.showId == show_id).filter(
                Shows.status == 'ACTIVE').first()
        if show:
            show.status = 'DELETED'
            db.session.add(show)
            db.session.commit()
        else:
            raise InputValidationError(404, 'Show is not found')
        return "Successfully Deleted", 200

    @marshal_with(show_fields)
    @token_required("admin")
    def post(current_user, self, user_id, theatre_id):
        theatre = db.session.query(Theatres).filter(Theatres.userId == user_id).filter(Theatres.theatreId == theatre_id).first()
        if theatre is None:
            raise InputValidationError(404, 'Theatre not found')
        args = create_show_parser.parse_args()
        name = args.get('name', None)
        rating = args.get('rating', None)
        startTime = args.get('startTime', None)
        endTime = args.get('endTime', None)
        tags = args.get('tags', None)
        price = args.get('price', None)
        status = "ACTIVE"
        createdOn = datetime.now()
        updatedOn = createdOn
        if name is None:
            raise BusinessValidationError(400, 'SHC01', 'Show name is required')
        if rating is None:
            raise BusinessValidationError(400, 'SHC02', 'Show Rating is required')
        if startTime is None:
            raise BusinessValidationError(400, 'SHC03', 'Show Start Time is required')
        if endTime is None:
            raise BusinessValidationError(400, 'SHC04', 'Show End Time is required')
        if tags is None:
            raise BusinessValidationError(400, 'SHC05', 'Show Tags are required')
        if price is None:
            raise BusinessValidationError(400, 'SHC06', 'Show Price is required')
        new_show = Shows(name=name, rating=rating, startTime=startTime,endTime=endTime,
         tags=tags, price=price,status=status, createdOn=createdOn,updatedOn=updatedOn,userId=user_id, theatreId=theatre_id)
        new_show.availableSeats = theatre.capacity
        new_show.theatreName = theatre.name
        new_show.city = theatre.city
        db.session.add(new_show)
        db.session.commit()
        return new_show, 201

class BookingsApi(Resource):

    @token_required("admin", "user")
    def get(current_user, self, user_id):
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('size', 8))
        if page < 1:
            raise BusinessValidationError(400, 'SHA01', 'page should be either null or greater than 0')
        if page_size < 2:
            raise BusinessValidationError(400, 'SHA02', 'page size should be either null or at least 1')
        start = (page -1) * page_size
        bookings_with_theatres_and_shows = db.session.query(Bookings, Theatres, Shows).join(
            Theatres, Bookings.theatreId == Theatres.theatreId).join(
                Shows, Bookings.showId == Shows.showId).filter(Bookings.userId == user_id).order_by(
            Bookings.updatedOn.desc()).offset(start).limit(page_size).all()
        # Convert the results to a list of dictionaries for JSON response
        results = []
        for booking, theatre, show in bookings_with_theatres_and_shows:
            results.append({
                'bookingId': booking.bookingId,
                'theatreId': booking.theatreId,
                'theatreName': theatre.name,
                'theatreArea': theatre.area,
                'theatreCity': theatre.city,
                'showId': booking.showId,
                'showName': show.name,
                'showStartTime': show.startTime,
                'showPrice': show.price,
                'count': booking.count,
                'bookedOn' : booking.createdOn
            })

        return jsonify(results)


class BookingPagesApi(Resource):

    @marshal_with(page_fields)
    @token_required("admin", "user")
    def get(current_user, self, user_id):
        page_size = int(request.args.get('size', 8))
        if page_size < 2:
            raise BusinessValidationError(400, 'TRA02', 'page size should be either null or at least 1')
        bookingCount = db.session.query(Bookings).filter(Bookings.userId == user_id).count()
        import math
        pageCount = math.ceil(bookingCount/page_size)
        page = Page()
        page.pageCount = pageCount
        page.itemCount = bookingCount
        return page

class BookingApi(Resource):

    @marshal_with(booking_fields)
    @token_required("admin", "user")
    def post(current_user, self, user_id, theatre_id, show_id):
        show = db.session.query(Shows).filter(
            Shows.theatreId == theatre_id).filter(Shows.showId == show_id).first()
        if show is None:
            raise InputValidationError(404, 'Show not found')
        if (show.availableSeats <= 0):
            raise BusinessValidationError(400, 'BKC02', 'Houseful!')
        args = create_booking_parser.parse_args()
        count = args.get('count', None)
        createdOn = datetime.now()
        updatedOn = createdOn
        if count is None:
            raise BusinessValidationError(400, 'BKC01', 'Booking count is required')
        if (show.availableSeats < int(count)):
            raise BusinessValidationError(400, 'BKC03', 'Sorry, the requested number of tickets not Available')
        new_booking = Bookings(count=count, createdOn=createdOn,updatedOn=updatedOn,userId=user_id, theatreId=theatre_id, showId=show_id)
        show.availableSeats = show.availableSeats - int(count)
        show.updatedOn = updatedOn
        db.session.add(show)
        db.session.add(new_booking)
        db.session.commit()
        return new_booking, 201

class ShowBookingsApi(Resource):

    @token_required("admin")
    def get(current_user, self, user_id, theatre_id, show_id):
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('size', 8))
        if page < 1:
            raise BusinessValidationError(400, 'SHA01', 'page should be either null or greater than 0')
        if page_size < 2:
            raise BusinessValidationError(400, 'SHA02', 'page size should be either null or at least 1')
        start = (page -1) * page_size
        
        bookings_with_theatres_and_shows = db.session.query(Bookings, Theatres, Shows).join(
            Theatres, Bookings.theatreId == Theatres.theatreId).join(
            Shows, Bookings.showId == Shows.showId).filter(Bookings.theatreId == theatre_id).filter(
            Bookings.showId == show_id).order_by(
            Bookings.updatedOn.desc()).offset(start).limit(page_size).all()

        # Convert the results to a list of dictionaries for JSON response
        results = []
        for booking, theatre, show in bookings_with_theatres_and_shows:
            results.append({
                'bookingId': booking.bookingId,
                'theatreId': booking.theatreId,
                'theatreName': theatre.name,
                'theatreArea': theatre.area,
                'theatreCity': theatre.city,
                'showId': booking.showId,
                'showName': show.name,
                'showStartTime': show.startTime,
                'showPrice': show.price,
                'count': booking.count,
                'bookedOn' : booking.createdOn
            })

        return jsonify(results)

class ShowBookingsPageApi(Resource):

    @marshal_with(page_fields)
    @token_required("admin")
    def get(current_user, self, user_id, theatre_id, show_id):
        page_size = int(request.args.get('size', 8))
        if page_size < 2:
            raise BusinessValidationError(400, 'SHA02', 'page size should be either null or at least 1')
        bookingCount = db.session.query(Bookings).filter(Bookings.theatreId == theatre_id).filter(Bookings.showId == show_id).count()
        import math
        pageCount = math.ceil(bookingCount/page_size)
        page = Page()
        page.pageCount = pageCount
        page.itemCount = bookingCount
        return page

class ShowBookingsReportApi(Resource):

    @token_required("admin")
    def post(current_user, self, user_id, theatre_id, show_id):
        tasks.generate_show_bookings_report.apply_async(args=[user_id, theatre_id, show_id])
        return jsonify({'message': 'Report generation started. Check your email once it is done.'})