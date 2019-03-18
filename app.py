from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# 2. Create an app, being sure to pass __name__

app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to my 'Home' page!"

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    climate = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > last_year).\
    group_by(Measurement.date).all()
    
    return jsonify(climate)

@app.route("/api/v1.0/station")
def station():
    session = Session(engine)
    all_stations = session.query(Measurement.station).group_by(Measurement.station).all()
    
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    Measurement_count = func.count(Measurement.station)
    active_stations = session.query(Measurement.station, Measurement_count).\
        group_by(Measurement.station).\
        order_by(Measurement_count.desc()).all()
    most_active = active_stations[0][0]
    temp_freq = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > last_year, Measurement.station == most_active).\
    group_by(Measurement.date).all()

    return jsonify(temp_freq)

@app.route("/api/v1.0/01-06-2016")
def start():
    session = Session(engine)
    temp_start = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= '2016-01-06').\
    group_by(Measurement.date).all()
    
    return jsonify(temp_start)

@app.route("/api/v1.0/01-06-2016/01-14-2016")
def start_end():
    session = Session(engine)
    temp_start_end = session.query(
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)
    ).\
    filter(Measurement.date >= '2016-01-06').filter(Measurement.date <= '2016-01-14').\
    group_by(Measurement.date).all()

    return jsonify(temp_start_end)

if __name__ == "__main__":
    app.run(debug=True)
