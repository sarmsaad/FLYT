# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 16:01:18 2017

@author: Colleen
"""
"""
# App settings - change
export DATABASE_URL=postgres://someuser:withsomepassword@localhost:5432/appointments
export SECRET_KEY=asupersecr3tkeyshouldgo
export CELERY_URL=redis://localhost:6379

# Twilio settings - change
export TWILIO_ACCOUNT_SID=ACXXXXXXXXXXXXXXXXX
export TWILIO_AUTH_TOKEN=YYYYYYYYYYYYYYYYYY
export TWILIO_NUMBER=+###########
"""
import json
from flask import Flask, request, Response
from rwilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
#from twilio.twiml.voice_response import VoiceResponse

class Application(object):
    def __init__(self, routes, config, debug=True):
        self.fask_app = flask.Flask(__name__)
        self.routes = routes
        self.debug = debug
        self._configure_app(config)
        self._set_routes()
    
    def celery(self):
        app = self.flask_app
        celery = Celery(app.import_name, broker=app.config[
                        'CELERY_BROKER_URL'])
        celery.conf.update(app.config)

        TaskBase = celery.Task

        class ContextTask(TaskBase):
            abstract = True

            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return TaskBase.__call__(self, *args, **kwargs)
        celery.Task = ContextTask

        return celery

    def _set_routes(self):
        for route in self.routes:
            app_view = route.resource.as_view(route.route_name)
            self.flask_app.add_url_rule(route.url, view_func=app_view)

    def _configure_app(self, env):
        celery_url = env.get('CELERY_URL')

        self.flask_app.config[
            'SQLALCHEMY_DATABASE_URI'] = env.get('DATABASE_URL')

        self.flask_app.config['CELERY_BROKER_URL'] = env.get(
            'REDIS_URL', celery_url)
        self.flask_app.config['CELERY_RESULT_BACKEND'] = env.get(
            'REDIS_URL', celery_url)

        self.flask_app.config['TWILIO_ACCOUNT_SID'] = env.get(
            'TWILIO_ACCOUNT_SID')
        self.flask_app.config['TWILIO_AUTH_TOKEN'] = env.get(
            'TWILIO_AUTH_TOKEN')
        self.flask_app.config['TWILIO_NUMBER'] = env.get('TWILIO_NUMBER')

        self.flask_app.secret_key = env.get('SECRET_KEY')

        self.db = flask.ext.sqlalchemy.SQLAlchemy(self.flask_app)

    def start_app(self):
        self.flask_app.run(debug=self.debug)

Base = declarative_base()

class flightReminder(Base):
    __tablename__ = 'flightReminders'
    
    id = Column(Integer, primary_key=True)
    #Are we still doing names? Or nah?
    phoneNumber = Column(string(50), nullable=False)
    depTime = Column(DateTime, nullable=False)
    timezone = Column(String(50), nullable=False)
    buffTime = Column(Integer, nullable=False)
    reminder = Column(Integer, nullable=True)
    
    def __init__(self, phoneNumber, depTime, timezone, buffTime):
        self.phoneNumber = phoneNumber
        self.depTime = depTime
        self.timezone = timezone
        #for now assume that waitTime arrives in an array
        self.buffTime = int(sum(buffTime))
        #change to 0 later for first menu
        self.reminder = 0
        
    def __repr__(self):
        return '<flightReminder %r>' % self.name
    
    def get_notification_time1(self):
        flightTime = arrow.get(self.depTime)
        leaveTime = flightTime.replace(minutes=-self.buffTime)
        notTime = leaveTime.replace(minutes=-1)
        return notTime
    
    def get_notification_time2(self):
        flightTime = arrow.get(self.depTime)
        leaveTime = flightTime.replace(minutes=-self.buffTime)
        notTime = leaveTime.replace(seconds=-30)
        return leaveTime
    
    def get_notification_time3(self):
        flightTime = arrow.get(self.depTime)
        leaveTime = flightTime.replace(minutes=-self.buffTime)
        return leaveTime
    
    def get_notification_time4(self):
        flightTime = arrow.get(self.depTime)
        leaveTime = flightTime.replace(minutes=+30)
        return leaveTime

class ReminderResourceCreate(MethodView):
    
    def post(self):
        form = NewReminderResourceCreate(request.form)
        
        if form.validate():
            from tasks import send_sms_reminder
            
            flight = flightReminder(**form.data)
            flight.time = arrow.get(flight.time, flight.timezone).to('utc').naive
            
            reminders.db.session.add(appt)
            reminders.db.session.commit()
            # Weclome Message
            
            # First Reminder
            send_sms_reminder.apply_async(
                    args=[flight.id], eta=appt.get_notification_time1())
            # Second Reminder
            send_sms_reminder.apply_async(
                    args=[flight.id], eta=appt.get_notification_time2())
            # Call
            send_sms_reminder.apply_async(
                    args=[flight.id], eta=appt.get_notification_time3())
            # Should have left message
            send_sms_reminder.apply_async(
                    args=[flight.id], eta=appt.get_notification_time4())
            # Have a nice flight message
            send_sms_reminder.apply_async(
                    args=[flight.id], eta=appt.depTime())
            return redirect(url_for('flightReminder.index'), code=303)
        else:
            return render_template('flightReminder/new.html', form=form),400

TSID = "ACd3d6e4fed0307c74bd8db2d07d9f4e3b"
TTOKEN = "5d19e13da333c40b5919746f06169ecd"
#TNUMBER?

tclient = Client(TSID,TTOKEN)

@celery.task()
def send_sms_reminder(flightReminder_id):
    #Set up
    try:
        flightReminder = db.session.query(
                flightReminder).filter_by(id=flightReminder_id).one()
    except NoResultFound:
        return
    
    time = arrow.get(flightReminder.time).to(flightReminder.timezone)
    
    #Send welcome and menu list
    if flightReminder.reminder() == 0:
        body = "Weclome to Flyt! You're getting this message because you signed up to be reminded of a flight on {0}. If this was not you, or you would like to cancel your reminder, send #CANCEL".format(flightReminder.depTime)
        flightReminder.reminder += 1
    #add case for when we recieve #CANCEL
    
    #Send reminder 1 minute beforehand
    elif flightReminder.reminder == 1:
        body = "You have a flight at {0}, and need to leave in 1 minute.".format(flightReminder.depTime)
        flightReminder.reminder += 1
    
    #Send reminder 30 seconds beforehand
    elif flightReminder.reminder == 2:
        body = "You have a flight at {0}, and need to leave in 30 seconds.".format(flightReminder.deptTime)
        flightReminder.reminder += 2
    """
    #Call at time to leave the house
    call = tclient.api.account.calls.create(
            to=flightReminder.phoneNumber,
            from_=twilio_number,
            url="https://ear-tube-zkn.c9users.io/say?words={}".format(words))
    """
    #Send a tex that you really should have left
    elif flightReminder.reminder == 4:
        body = "You have a flight at {0}, and should have left 15 minutes ago.".format(flightReminder.deptTime)
        flightReminder.reminder += 1
    
    #Send a text saying have a nice flight
    else:
        body = "Have a nice flight!"
        
    to = flightReminder.phoneNumber,
    client.messages.create(
            to,
            from_=twilio_number,
            body=body)
