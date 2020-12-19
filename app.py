
import datetime as dt
import numpy as np
import pandas as pd
#Add the SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
# import flask
from flask import Flask,jsonify

# create engine
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect database into our classes
Base = automap_base()
Base.prepare(engine,reflect=True)

# class variables
Measurement=Base.classes.measurement
Station=Base.classes.station
# create session link
session = Session(engine)


# create flask instance called app
app = Flask(__name__)
# create root route
@app.route('/')
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017,8,23)-dt.timedelta(days=365)
    precipitation = session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date>= prev_year).all()
    info={date:prcp for date,prcp in precipitation}
    
    return jsonify(info) 

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)


@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
            filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))

    return jsonify(temps=temps)

    
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start = None, end = None):
    sels= [func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sels).\
            filter(Measurement.date >= start).\
                filter (Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sels).\
        filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
    temps=list(np.ravel(results))
    return jsonify(temps=temps)