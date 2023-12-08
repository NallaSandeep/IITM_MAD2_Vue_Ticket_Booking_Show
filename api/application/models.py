from .database import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    is_admin = db.Column(db.Integer, nullable=False, default=False)
    theatres = db.relationship('Theatres', backref='user', lazy=True)

class Theatres(db.Model):
    __tablename__ = 'theatres'
    theatreId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    area = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String)
    createdOn = db.Column(db.String, nullable=False)
    updatedOn = db.Column(db.String, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shows = db.relationship('Shows', backref='theatres', lazy=True)

class Shows(db.Model):
    __tablename__ = 'shows'
    showId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    startTime = db.Column(db.String, nullable=False)
    endTime = db.Column(db.String, nullable=False)
    tags = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    availableSeats = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String)
    theatreName = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    createdOn = db.Column(db.String, nullable=False)
    updatedOn = db.Column(db.String, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    theatreId = db.Column(db.Integer, db.ForeignKey('theatres.theatreId'), nullable=False)
    bookings = db.relationship('Bookings', backref='shows', lazy="subquery")

class Bookings(db.Model):
    __tablename__ = 'bookings'
    bookingId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    count = db.Column(db.Integer, nullable=False)
    createdOn = db.Column(db.String, nullable=False)
    updatedOn = db.Column(db.String, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    theatreId = db.Column(db.Integer, db.ForeignKey('theatres.theatreId'), nullable=False)
    showId = db.Column(db.Integer, db.ForeignKey('shows.showId'), nullable=False)