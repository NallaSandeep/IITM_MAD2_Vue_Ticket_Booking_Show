from flask import Flask
import os
from flask_restful import Api

from application.config import LocalDevelopmentConfig
from application.database import db
from flask_cors import CORS
from application import workers
from flask_sse import sse
from flask_mail import Mail

import logging

logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = None
rest_api = None
celery=None
mail = None
cache  = None


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder="static")
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    if os.getenv('ENV', "development") == "production":
        app.logger.info("Currently no production config is setup.")
        raise Exception("Currently no production config is setup.")
    else:
        app.logger.info("Staring Local Development.")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    from application.cache import init_cache
    init_cache(app)
    app.app_context().push()
    api = Api(app)
    app.app_context().push()
    celery = workers.celery
    celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"]
    )
    celery.Task = workers.ContextTask
    app.app_context().push()
    mail = Mail(app)
    app.app_context().push()
    app.logger.info("App setup complete")
    return app, api, celery, mail, cache


web_app, rest_api, celery, mail, cache = create_app()


# Importing REST API controllers
from application.api import TheatresApi, TheatrePagesApi, TheatreReportApi, TheatreApi
from application.api import ShowsApi, ShowPagesApi, UserShowsApi, UserShowsPageApi, ShowApi
from application.api import BookingsApi, BookingPagesApi, BookingApi, ShowBookingsApi, ShowBookingsPageApi, ShowBookingsReportApi


rest_api.add_resource(TheatreApi, '/api/<int:user_id>/theatre', '/api/<int:user_id>/theatre/<int:theatre_id>')
rest_api.add_resource(TheatresApi, '/api/<int:user_id>/theatres')
rest_api.add_resource(TheatrePagesApi, '/api/<int:user_id>/theatres/pages')
rest_api.add_resource(TheatreReportApi, '/api/<int:user_id>/theatre/<int:theatre_id>/report')
rest_api.add_resource(ShowApi, '/api/<int:user_id>/theatre/<int:theatre_id>/show', '/api/<int:user_id>/theatre/<int:theatre_id>/show/<int:show_id>')
rest_api.add_resource(UserShowsApi, '/api/<int:user_id>/theatre/<int:theatre_id>/shows')
rest_api.add_resource(UserShowsPageApi, '/api/<int:user_id>/theatre/<int:theatre_id>/shows/pages')
rest_api.add_resource(ShowsApi, '/api/shows')
rest_api.add_resource(ShowPagesApi, '/api/shows/pages')
rest_api.add_resource(BookingApi, '/api/<int:user_id>/theatre/<int:theatre_id>/show/<int:show_id>/booking')
rest_api.add_resource(ShowBookingsApi, '/api/<int:user_id>/theatre/<int:theatre_id>/show/<int:show_id>/bookings')
rest_api.add_resource(ShowBookingsPageApi, '/api/<int:user_id>/theatre/<int:theatre_id>/show/<int:show_id>/bookings/pages')
rest_api.add_resource(ShowBookingsReportApi, '/api/<int:user_id>/theatre/<int:theatre_id>/show/<int:show_id>/bookings/report')
rest_api.add_resource(BookingsApi, '/api/<int:user_id>/bookings')
rest_api.add_resource(BookingPagesApi, '/api/<int:user_id>/bookings/pages')

if __name__ == '__main__':
    web_app.run(host='0.0.0.0', port=5000)
